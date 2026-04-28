import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.bill_service import bill_service
from db.sqlite_helper import init_database

def test_add_and_get():
    init_database()
    bill_id = bill_service.add_bill({
        'amount': 28.0,
        'type': 'expense',
        'category': '餐饮',
        'source': 'text',
        'bill_time': '2026-04-28 12:35',
        'raw_text': '测试'
    })
    assert bill_id > 0
    bill = bill_service.get_bill_by_id(bill_id)
    assert bill['amount'] == 28.0

def test_today_bills():
    bills = bill_service.get_today_bills()
    assert isinstance(bills, list)

def test_category_stats():
    stats = bill_service.get_category_stats('month')
    assert isinstance(stats, dict)

def test_delete():
    init_database()
    bill_id = bill_service.add_bill({
        'amount': 28.0,
        'type': 'expense',
        'category': '餐饮',
        'source': 'text',
        'bill_time': '2026-04-28 12:35',
        'raw_text': '测试删除'
    })
    result = bill_service.delete_bill(bill_id)
    assert result == True

if __name__ == '__main__':
    test_add_and_get()
    test_today_bills()
    test_category_stats()
    test_delete()
    print('All tests passed!')
