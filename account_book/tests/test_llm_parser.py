import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_parser import LLMParser

def test_expense_parsing():
    parser = LLMParser()
    result = parser.parse_bill_text('今天中午12点35分吃饭花了28元')
    assert result['amount'] == 28.0
    assert result['type'] == 'expense'
    assert result['category'] == '餐饮'
    assert '2026' in result['bill_time']  # 时间格式 YYYY-MM-DD HH:mm

def test_income_parsing():
    parser = LLMParser()
    result = parser.parse_bill_text('工资到账5000元')
    assert result['type'] == 'income'
    assert result['amount'] == 5000.0

def test_time_parsing():
    parser = LLMParser()
    result = parser.parse_bill_text('昨天20:10打车43元')
    assert '20:10' in result['bill_time']

if __name__ == '__main__':
    test_expense_parsing()
    test_income_parsing()
    test_time_parsing()
    print('All tests passed!')
