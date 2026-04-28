"""
LLM 解析服务 - 将自然语言账单文本解析成结构化数据

当前使用 mock 实现，方便后续替换为真实 API
支持: DeepSeek / 豆包 / 通义千问
"""

import re
from utils.time_utils import get_current_time_str, parse_natural_time


class LLMParser:
    """LLM 解析器"""

    def __init__(self):
        self.provider = 'mock'  # 当前使用 mock，可改为 'deepseek', 'doubao', 'qwen'
        self._init_providers()

    def _init_providers(self):
        """初始化各提供商配置"""
        self.providers = {
            'mock': self._parse_mock,
            # 后续可添加:
            # 'deepseek': self._parse_deepseek,
            # 'doubao': self._parse_doubao,
            # 'qwen': self._parse_qwen,
        }

    def set_provider(self, provider):
        """设置解析提供商"""
        if provider in self.providers:
            self.provider = provider
            print(f"[LLMParser] Provider set to: {provider}")
        else:
            print(f"[LLMParser] Unknown provider: {provider}, keeping {self.provider}")

    def parse_bill_text(self, text):
        """
        解析账单文本

        Args:
            text: 自然语言账单文本，如 "今天中午12点35分吃饭花了28元"

        Returns:
            dict: 解析后的账单数据
            {
                "amount": 28.0,
                "type": "expense",
                "category": "餐饮",
                "merchant": "",
                "note": "吃饭",
                "bill_time": "2026-04-28 12:35",
                "source": "text",
                "raw_text": "原始文本"
            }
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        text = text.strip()
        parser = self.providers.get(self.provider, self._parse_mock)
        return parser(text)

    def _parse_mock(self, text):
        """
        Mock 解析实现
        使用规则解析，适用于简单场景
        """
        result = {
            'amount': 0,
            'type': 'expense',
            'category': '其他',
            'merchant': '',
            'note': '',
            'bill_time': get_current_time_str(),
            'source': 'text',
            'raw_text': text
        }

        # 提取金额
        # 匹配模式: 花了XX元, 消费XX元, XX元, 花了XX
        amount_patterns = [
            r'花了(\d+(?:\.\d+)?)元',
            r'消费(\d+(?:\.\d+)?)元',
            r'花费(\d+(?:\.\d+)?)元',
            r'(\d+(?:\.\d+)?)元',
            r'到账(\d+(?:\.\d+)?)',
            r'收入(\d+(?:\.\d+)?)',
        ]

        for pattern in amount_patterns:
            match = re.search(pattern, text)
            if match:
                result['amount'] = float(match.group(1))
                break

        # 判断收入/支出
        income_keywords = ['到账', '收入', '工资', '奖金', '退款', '返还', '回收']
        for keyword in income_keywords:
            if keyword in text:
                result['type'] = 'income'
                break

        # 提取分类
        category_keywords = {
            '餐饮': ['吃饭', '餐厅', '外卖', '小吃', '美食', '午餐', '晚餐', '早餐', '咖啡', '奶茶'],
            '交通': ['打车', '公交', '地铁', '出租车', '开车', '停车', '油费', '过路费'],
            '购物': ['购物', '买', '网购', '淘宝', '京东', '超市', '商场'],
            '娱乐': ['电影', 'KTV', '游戏', '娱乐', '旅游', '演出'],
            '医疗': ['医院', '药店', '买药', '医疗'],
            '教育': ['学费', '培训', '教育', '书', '课程'],
            '居住': ['房租', '水电', '物业', '住宿'],
            '通讯': ['话费', '流量', '宽带', '手机'],
            '工资': ['工资', '薪资', '薪水'],
            '投资': ['投资', '理财', '基金', '股票'],
        }

        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    result['category'] = category
                    break
            if result['category'] != '其他':
                break

        # 提取商家/备注
        note_patterns = [
            r'在(.+?)花了',
            r'在(.+?)消费',
            r'在(.+?)[花了消费]',
        ]
        for pattern in note_patterns:
            match = re.search(pattern, text)
            if match:
                result['merchant'] = match.group(1)
                break

        # 解析时间
        time_result = parse_natural_time(text)
        if time_result:
            result['bill_time'] = time_result

        return result

    def _call_api(self, provider, text):
        """
        调用外部 API 的基类方法
        后续实现具体 API 调用
        """
        # 占位实现
        raise NotImplementedError(f"{provider} API not implemented yet")


# 全局单例
llm_parser = LLMParser()