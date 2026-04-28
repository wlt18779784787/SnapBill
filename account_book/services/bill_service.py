"""
账单服务 - 提供账单的 CRUD 操作和统计功能
"""

from db.sqlite_helper import get_connection, row_to_dict, get_current_time_str
from datetime import datetime, timedelta


class BillService:
    """账单服务类"""

    def __init__(self):
        pass

    def add_bill(self, bill_data):
        """
        添加账单

        bill_data 字典包含:
        - amount: 金额 (必填)
        - type: 类型，income/expense (必填)
        - category: 分类 (默认 '其他')
        - merchant: 商家 (默认 '')
        - note: 备注 (默认 '')
        - source: 来源，text/image (必填)
        - raw_text: 原始文本 (默认 '')
        - bill_time: 账单时间 (必填，格式 YYYY-MM-DD HH:mm)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 验证必填字段
            required_fields = ['amount', 'type', 'source', 'bill_time']
            for field in required_fields:
                if field not in bill_data or bill_data[field] is None:
                    raise ValueError(f"Missing required field: {field}")

            # 构建插入语句
            cursor.execute('''
                INSERT INTO bills (
                    amount, type, category, merchant, note, source, raw_text, bill_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                bill_data['amount'],
                bill_data['type'],
                bill_data.get('category', '其他'),
                bill_data.get('merchant', ''),
                bill_data.get('note', ''),
                bill_data['source'],
                bill_data.get('raw_text', ''),
                bill_data['bill_time'],
            ))

            bill_id = cursor.lastrowid
            conn.commit()
            conn.close()

            print(f"[BillService] Added bill id={bill_id}")
            return bill_id

        except Exception as e:
            print(f"[BillService] Error adding bill: {e}")
            raise

    def get_bill_by_id(self, bill_id):
        """根据ID获取账单"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bills WHERE id = ?', (bill_id,))
        row = cursor.fetchone()
        conn.close()
        return row_to_dict(row) if row else None

    def _get_date_range(self, range_type):
        """获取日期范围"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if range_type == 'today':
            start = today_start
            end = now
        elif range_type == 'week':
            start = today_start - timedelta(days=now.weekday())
            end = now
        elif range_type == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif range_type == 'year':
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now
        else:
            start = today_start
            end = now

        return start.strftime('%Y-%m-%d %H:%M'), end.strftime('%Y-%m-%d %H:%M')

    def _query_bills(self, start_time, end_time):
        """查询指定时间范围内的账单"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM bills WHERE bill_time >= ? AND bill_time <= ? ORDER BY bill_time DESC',
            (start_time, end_time)
        )
        rows = cursor.fetchall()
        conn.close()
        return [row_to_dict(row) for row in rows]

    def get_today_bills(self):
        """获取今日账单"""
        start, end = self._get_date_range('today')
        return self._query_bills(start, end)

    def get_week_bills(self):
        """获取本周账单"""
        start, end = self._get_date_range('week')
        return self._query_bills(start, end)

    def get_month_bills(self):
        """获取本月账单"""
        start, end = self._get_date_range('month')
        return self._query_bills(start, end)

    def get_year_bills(self):
        """获取本年账单"""
        start, end = self._get_date_range('year')
        return self._query_bills(start, end)

    def get_all_bills(self, limit=100):
        """获取所有账单（分页）"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bills ORDER BY bill_time DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [row_to_dict(row) for row in rows]

    def get_category_stats(self, range_type='month'):
        """获取分类统计"""
        start, end = self._get_date_range(range_type)

        conn = get_connection()
        cursor = conn.cursor()

        # 按分类和类型统计
        cursor.execute('''
            SELECT category, type, SUM(amount) as total
            FROM bills
            WHERE bill_time >= ? AND bill_time <= ?
            GROUP BY category, type
            ORDER BY total DESC
        ''', (start, end))

        rows = cursor.fetchall()
        conn.close()

        stats = {}
        for row in rows:
            category = row['category']
            if category not in stats:
                stats[category] = {'income': 0, 'expense': 0}
            stats[category][row['type']] = row['total']

        return stats

    def delete_bill(self, bill_id):
        """删除账单"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bills WHERE id = ?', (bill_id,))
            affected = cursor.rowcount
            conn.commit()
            conn.close()

            print(f"[BillService] Deleted bill id={bill_id}, affected={affected}")
            return affected > 0

        except Exception as e:
            print(f"[BillService] Error deleting bill: {e}")
            raise


# 全局单例
bill_service = BillService()