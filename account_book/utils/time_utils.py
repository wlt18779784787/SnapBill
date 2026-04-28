"""时间工具函数"""

from datetime import datetime, timedelta


def get_current_time_str():
    """获取当前本地时间字符串，格式 YYYY-MM-DD HH:mm"""
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def parse_time(time_str):
    """
    解析时间字符串，支持多种格式
    返回 YYYY-MM-DD HH:mm 格式
    """
    if not time_str:
        return get_current_time_str()

    time_str = time_str.strip()

    # 尝试多种格式
    formats = [
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
        '%Y年%m月%d日 %H:%M',
        '%m-%d %H:%M',
        '%m/%d %H:%M',
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            return dt.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            continue

    # 如果解析失败，返回当前时间
    return get_current_time_str()


def parse_natural_time(text):
    """
    从自然语言解析时间
    例如：
    - "今天中午12点35分" -> 2026-04-28 12:35
    - "昨天晚上8点10分" -> 2026-04-27 20:10
    - "今天15:30" -> 2026-04-28 15:30
    """
    now = datetime.now()
    result = now

    text = text.replace(' ', '')

    # 今天
    if '今天' in text:
        result = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # 昨天
    if '昨天' in text:
        result = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 前天
    if '前天' in text:
        result = (now - timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 匹配时间模式: 12点35分, 12:35, 12点35
    import re

    # 模式1: XX点XX分 或 XX点XX
    pattern1 = re.compile(r'(\d{1,2})点(\d{1,2})分?')
    match = pattern1.search(text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        result = result.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # 模式2: HH:MM
    pattern2 = re.compile(r'(\d{1,2}):(\d{2})')
    match = pattern2.search(text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        result = result.replace(hour=hour, minute=minute, second=0, microsecond=0)

    return result.strftime('%Y-%m-%d %H:%M')


def format_time_for_display(time_str):
    """格式化时间用于显示"""
    if not time_str:
        return ''
    try:
        dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        return dt.strftime('%m-%d %H:%M')
    except ValueError:
        return time_str