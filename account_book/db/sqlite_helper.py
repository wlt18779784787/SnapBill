# Date: 2026-04-28
# Time: 14:35:00

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'bills.db')
DB_DIR = os.path.dirname(DB_PATH)


def get_connection():
    """获取数据库连接"""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """初始化数据库和表"""
    conn = get_connection()
    cursor = conn.cursor()

    # 创建账单表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            category TEXT NOT NULL DEFAULT '其他',
            merchant TEXT DEFAULT '',
            note TEXT DEFAULT '',
            source TEXT NOT NULL CHECK(source IN ('text', 'image')),
            raw_text TEXT DEFAULT '',
            bill_time TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M', 'now', 'localtime')),
            updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'))
        )
    ''')

    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bill_time ON bills(bill_time)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON bills(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON bills(type)')

    conn.commit()
    conn.close()
    print(f"[Database] Initialized at {DB_PATH}")


def row_to_dict(row):
    """将 Row 对象转换为字典"""
    if row is None:
        return None
    return dict(row)


def parse_time_local(time_str):
    """解析时间字符串，返回 YYYY-MM-DD HH:mm 格式"""
    if not time_str:
        return None
    # 移除任何多余空格
    time_str = time_str.strip()
    # 验证格式
    try:
        datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        return time_str
    except ValueError:
        return None


def get_current_time_str():
    """获取当前本地时间字符串，格式 YYYY-MM-DD HH:mm"""
    return datetime.now().strftime('%Y-%m-%d %H:%M')