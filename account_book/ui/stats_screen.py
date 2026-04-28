from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from services.bill_service import bill_service
from utils.ui_components import (
    BG_COLOR,
    CARD_COLOR,
    DANGER_COLOR,
    PRIMARY_COLOR,
    ModernLabel,
    PrimaryButton,
    RoundedCard,
    SubtitleLabel,
    TitleLabel,
    bind_label_height,
    format_money,
)


class StatCard(RoundedCard):
    def __init__(self, title, value, color=PRIMARY_COLOR, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("spacing", dp(6))
        super().__init__(**kwargs)
        self.bg_color = CARD_COLOR
        self.border_color = (0.91, 0.93, 0.96, 1)
        self.shadow_color = (0, 0, 0, 0.04)
        self.shadow_dy = dp(-2)
        self.padding = [dp(16), dp(16), dp(16), dp(16)]

        title_label = ModernLabel(
            text=title,
            font_size="14sp",
            color=(0.45, 0.49, 0.55, 1),
            size_hint_y=None,
            height=dp(20),
            halign="left",
            valign="middle",
        )
        title_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        self.add_widget(title_label)

        self.value_label = ModernLabel(
            text=value,
            font_size="22sp",
            bold=True,
            color=color,
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle",
        )
        self.value_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        self.add_widget(self.value_label)


class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stats_container = None
        self.total_income_label = None
        self.total_expense_label = None
        self.balance_label = None
        self.init_ui()

    def init_ui(self):
        with self.canvas.before:
            Color(rgba=BG_COLOR)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(20), dp(20), dp(20)], spacing=dp(12))

        header = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        back_btn = PrimaryButton(text="\u8fd4\u56de\u9996\u9875", size_hint_x=None, width=dp(92), height=dp(46), font_size="14sp")
        back_btn.bind(on_press=lambda *_args: self.go_back())
        header.add_widget(back_btn)
        title = TitleLabel(text="\u7edf\u8ba1\u5206\u6790", font_size="24sp", size_hint_x=1, halign="left", valign="middle")
        title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        header.add_widget(title)
        root.add_widget(header)

        subtitle = SubtitleLabel(
            text="\u672c\u6708\u6536\u652f\u6982\u89c8",
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
        )
        subtitle.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        root.add_widget(subtitle)

        hero_card = RoundedCard(orientation="vertical", size_hint_y=None, spacing=dp(10))
        hero_card.height = dp(118)
        hero_card.padding = [dp(18), dp(18), dp(18), dp(18)]
        hero_card.bg_color = (0.06, 0.46, 0.95, 1)
        hero_card.border_color = (0.06, 0.46, 0.95, 1)
        hero_card.shadow_color = (0, 0, 0, 0.08)
        hero_card.shadow_dy = dp(-3)
        hero_title = ModernLabel(
            text="\u672c\u6708\u6982\u89c8",
            font_size="14sp",
            color=(1, 1, 1, 0.88),
            size_hint_y=None,
            height=dp(20),
            halign="left",
            valign="middle",
        )
        hero_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        hero_value = ModernLabel(
            text="\u8fd9\u4e2a\u6708\u8fd8\u672a\u6709\u66f4\u591a\u7ed3\u6790",
            font_size="20sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(32),
            halign="left",
            valign="middle",
        )
        hero_value.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        hero_subtitle = SubtitleLabel(
            text="\u6240\u6709\u5355\u7b14\u4f1a\u5728\u4e0b\u65b9\u6309\u5206\u7c7b\u7edf\u8ba1\u3002",
            size_hint_y=None,
            height=dp(24),
            color=(1, 1, 1, 0.8),
            halign="left",
            valign="middle",
        )
        hero_subtitle.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        hero_card.add_widget(hero_title)
        hero_card.add_widget(hero_value)
        hero_card.add_widget(hero_subtitle)
        root.add_widget(hero_card)

        top_row = BoxLayout(size_hint_y=None, height=dp(92), spacing=dp(10))
        income_card = StatCard("\u6536\u5165\u603b\u8ba1", "\uffe50.00", color=(0.20, 0.66, 0.36, 1))
        expense_card = StatCard("\u652f\u51fa\u603b\u8ba1", "\uffe50.00", color=DANGER_COLOR)
        top_row.add_widget(income_card)
        top_row.add_widget(expense_card)
        self.total_income_label = income_card.value_label
        self.total_expense_label = expense_card.value_label
        root.add_widget(top_row)

        balance_card = RoundedCard(orientation="vertical", size_hint_y=None)
        balance_card.height = dp(86)
        balance_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        balance_card.shadow_color = (0, 0, 0, 0.04)
        balance_card.shadow_dy = dp(-2)
        balance_title = ModernLabel(
            text="\u7ed3\u4f59",
            font_size="14sp",
            color=(0.45, 0.49, 0.55, 1),
            size_hint_y=None,
            height=dp(20),
            halign="left",
            valign="middle",
        )
        balance_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        self.balance_label = ModernLabel(
            text="\uffe50.00",
            font_size="22sp",
            bold=True,
            color=PRIMARY_COLOR,
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle",
        )
        self.balance_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        balance_card.add_widget(balance_title)
        balance_card.add_widget(self.balance_label)
        root.add_widget(balance_card)

        list_title = ModernLabel(
            text="\u5206\u7c7b\u660e\u7ec6",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="middle",
        )
        list_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        root.add_widget(list_title)

        scroll = ScrollView(do_scroll_x=False)
        self.stats_container = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        self.stats_container.bind(minimum_height=self.stats_container.setter("height"))
        scroll.add_widget(self.stats_container)
        root.add_widget(scroll)

        self.add_widget(root)
        self.refresh_stats()

    def _update_rect(self, *_args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self, *_args):
        self.refresh_stats()

    def go_back(self):
        self.manager.current = "home"

    def refresh_stats(self):
        self.stats_container.clear_widgets()

        try:
            stats = bill_service.get_category_stats("month")
        except Exception as exc:
            error_card = RoundedCard(orientation="vertical", size_hint_y=None)
            error_card.height = dp(94)
            error_label = ModernLabel(
                text=f"\u83b7\u53d6\u7edf\u8ba1\u5931\u8d25\uff1a{exc}",
                font_size="14sp",
                size_hint_y=None,
                height=dp(46),
                halign="left",
                valign="middle",
            )
            bind_label_height(error_label, padding=dp(10))
            error_card.add_widget(error_label)
            self.stats_container.add_widget(error_card)
            return

        if not stats:
            empty_card = RoundedCard(orientation="vertical", size_hint_y=None)
            empty_card.height = dp(94)
            empty_card.shadow_color = (0, 0, 0, 0.03)
            empty_card.shadow_dy = dp(-1)
            empty_label = ModernLabel(
                text="\u6682\u65e0\u7edf\u8ba1\u6570\u636e",
                font_size="15sp",
                bold=True,
                size_hint_y=None,
                height=dp(24),
                halign="center",
                valign="middle",
            )
            empty_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
            empty_subtitle = SubtitleLabel(
                text="\u7b49\u6709\u8d26\u5355\u4e4b\u540e\uff0c\u8fd9\u91cc\u4f1a\u81ea\u52a8\u6c47\u603b\u3002",
                size_hint_y=None,
                height=dp(26),
                halign="center",
                valign="middle",
            )
            bind_label_height(empty_subtitle, padding=dp(10))
            empty_card.add_widget(empty_label)
            empty_card.add_widget(empty_subtitle)
            self.stats_container.add_widget(empty_card)
            return

        total_income = 0.0
        total_expense = 0.0
        category_totals = []

        for category, data in stats.items():
            cat_income = float(data.get("income", 0) or 0)
            cat_expense = float(data.get("expense", 0) or 0)
            total_income += cat_income
            total_expense += cat_expense
            category_totals.append((category, cat_income, cat_expense, cat_income + cat_expense))

        balance = total_income - total_expense
        self.total_income_label.text = format_money(total_income)
        self.total_expense_label.text = format_money(total_expense)
        self.balance_label.text = format_money(balance)

        category_totals.sort(key=lambda item: item[3], reverse=True)
        for category, cat_income, cat_expense, cat_total in category_totals:
            item_card = RoundedCard(orientation="vertical", size_hint_y=None)
            item_card.height = dp(78)
            item_card.padding = [dp(16), dp(14), dp(16), dp(14)]
            item_card.shadow_color = (0, 0, 0, 0.03)
            item_card.shadow_dy = dp(-1)
            main = ModernLabel(
                text=category,
                font_size="15sp",
                bold=True,
                size_hint_y=None,
                height=dp(22),
                halign="left",
                valign="middle",
            )
            main.bind(size=lambda instance, value: setattr(instance, "text_size", value))
            detail = SubtitleLabel(
                text=f"\u6536\u5165 {format_money(cat_income)}  \u00b7  \u652f\u51fa {format_money(cat_expense)}  \u00b7  \u5408\u8ba1 {format_money(cat_total)}",
                size_hint_y=None,
                height=dp(32),
                halign="left",
                valign="top",
            )
            bind_label_height(detail, padding=dp(10))
            item_card.add_widget(main)
            item_card.add_widget(detail)
            self.stats_container.add_widget(item_card)
