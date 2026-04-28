from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from services.bill_service import bill_service
from utils.ui_components import (
    BG_COLOR,
    CARD_COLOR,
    PRIMARY_COLOR,
    TEXT_COLOR,
    MetricValueLabel,
    ModernLabel,
    PrimaryButton,
    RoundedCard,
    SecondaryButton,
    ShortcutTile,
    SubtitleLabel,
    TitleLabel,
    bind_label_height,
    format_money,
)


class HomeMetricCard(RoundedCard):
    def __init__(self, title, value, accent_color=PRIMARY_COLOR, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("spacing", dp(8))
        super().__init__(**kwargs)
        self.bg_color = CARD_COLOR
        self.border_color = (0.91, 0.93, 0.96, 1)
        self.shadow_color = (0, 0, 0, 0.045)
        self.shadow_dy = dp(-2)
        self.padding = [dp(18), dp(18), dp(18), dp(18)]

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

        self.value_label = MetricValueLabel(
            text=value,
            color=accent_color,
            size_hint_y=None,
            height=dp(34),
            halign="left",
            valign="middle",
        )
        self.value_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        self.add_widget(self.value_label)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today_value_label = None
        self.month_value_label = None
        self.init_ui()

    def init_ui(self):
        with self.canvas.before:
            Color(rgba=BG_COLOR)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

        root = ScrollView(do_scroll_x=False)
        content = BoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(24), dp(20), dp(24)],
            spacing=dp(16),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))
        root.add_widget(content)

        hero_card = RoundedCard(orientation="vertical", size_hint_y=None, spacing=dp(8))
        hero_card.height = dp(112)
        hero_card.padding = [dp(18), dp(18), dp(18), dp(18)]
        hero_card.shadow_color = (0, 0, 0, 0.06)
        hero_card.shadow_dy = dp(-3)

        title = TitleLabel(
            text="SnapBill",
            font_size="30sp",
            size_hint_y=None,
            height=dp(40),
            color=TEXT_COLOR,
            halign="left",
            valign="middle",
        )
        title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        hero_card.add_widget(title)

        subtitle = SubtitleLabel(
            text="\u4e00\u53e5\u8bdd\uff0c\u4e00\u5f20\u56fe\uff0c\u8f7b\u677e\u8bb0\u8d26",
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="middle",
        )
        subtitle.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        hero_card.add_widget(subtitle)
        content.add_widget(hero_card)

        icon_card = RoundedCard(orientation="vertical", size_hint_y=None, spacing=dp(12))
        icon_card.height = dp(124)
        icon_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        icon_card.shadow_color = (0, 0, 0, 0.05)
        icon_card.shadow_dy = dp(-2)

        icon_title = ModernLabel(
            text="\u5feb\u6377\u56fe\u6807",
            font_size="16sp",
            bold=True,
            color=TEXT_COLOR,
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="middle",
        )
        icon_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        icon_card.add_widget(icon_title)

        icon_row = BoxLayout(size_hint_y=None, height=dp(84), spacing=dp(8))
        shortcuts = [
            ("\u8bb0", "\u6587\u5b57", PRIMARY_COLOR, lambda: self.go_to("add_text")),
            ("\u76f8", "\u56fe\u7247", (0.0, 0.72, 0.58, 1), lambda: self.go_to("add_image")),
            ("\u5355", "\u8d26\u5355", (1.0, 0.58, 0.0, 1), lambda: self.go_to_bill_list()),
            ("\u6790", "\u7edf\u8ba1", (0.62, 0.39, 1.0, 1), lambda: self.go_to("stats")),
        ]
        for symbol, title_text, accent_color, callback in shortcuts:
            icon_row.add_widget(
                ShortcutTile(
                    symbol=symbol,
                    title=title_text,
                    accent_color=accent_color,
                    callback=callback,
                )
            )
        icon_card.add_widget(icon_row)
        content.add_widget(icon_card)

        metrics_row = BoxLayout(size_hint_y=None, height=dp(128), spacing=dp(12))
        today_card = HomeMetricCard("\u4eca\u65e5\u652f\u51fa", "\uffe50.00")
        self.today_value_label = today_card.value_label
        metrics_row.add_widget(today_card)

        month_card = HomeMetricCard("\u672c\u6708\u652f\u51fa", "\uffe50.00")
        self.month_value_label = month_card.value_label
        metrics_row.add_widget(month_card)
        content.add_widget(metrics_row)

        quick_row = BoxLayout(size_hint_y=None, height=dp(66), spacing=dp(12))
        text_btn = PrimaryButton(text="\u6587\u5b57\u8bb0\u8d26")
        text_btn.bind(on_press=lambda *_args: self.go_to("add_text"))
        quick_row.add_widget(text_btn)

        image_btn = PrimaryButton(text="\u56fe\u7247\u8bb0\u8d26")
        image_btn.bind(on_press=lambda *_args: self.go_to("add_image"))
        quick_row.add_widget(image_btn)
        content.add_widget(quick_row)

        more_title = ModernLabel(
            text="\u5e38\u7528\u529f\u80fd",
            font_size="16sp",
            bold=True,
            color=TEXT_COLOR,
            size_hint_y=None,
            height=dp(26),
            halign="left",
            valign="middle",
        )
        more_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        content.add_widget(more_title)

        list_card = RoundedCard(orientation="vertical", spacing=dp(12), size_hint_y=None)
        list_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        list_card.height = dp(128)
        list_card.shadow_color = (0, 0, 0, 0.04)
        list_card.shadow_dy = dp(-2)

        bill_btn = SecondaryButton(text="\u67e5\u770b\u8d26\u5355", size_hint_y=None, height=dp(48))
        bill_btn.bind(on_press=lambda *_args: self.go_to_bill_list())
        list_card.add_widget(bill_btn)

        stats_btn = SecondaryButton(text="\u7edf\u8ba1\u5206\u6790", size_hint_y=None, height=dp(48))
        stats_btn.bind(on_press=lambda *_args: self.go_to("stats"))
        list_card.add_widget(stats_btn)
        content.add_widget(list_card)

        tip_card = RoundedCard(orientation="vertical", size_hint_y=None)
        tip_card.height = dp(92)
        tip_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        tip_card.shadow_color = (0, 0, 0, 0.04)
        tip_card.shadow_dy = dp(-2)
        tip_title = ModernLabel(
            text="\u4eca\u5929\u4e5f\u8bb0\u4e00\u7b14",
            font_size="15sp",
            bold=True,
            color=TEXT_COLOR,
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
        )
        tip_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        tip_body = SubtitleLabel(
            text="\u5148\u4ece\u6587\u5b57\u8bb0\u8d26\u5f00\u59cb\uff0c\u6216\u76f4\u63a5\u62cd\u7167\u8bc6\u522b\u7968\u636e\u3002",
            size_hint_y=None,
            height=dp(34),
            halign="left",
            valign="top",
        )
        bind_label_height(tip_body, padding=dp(12))
        tip_card.add_widget(tip_title)
        tip_card.add_widget(tip_body)
        content.add_widget(tip_card)

        self.add_widget(root)

    def _update_rect(self, *_args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self, *_args):
        self.refresh_metrics()

    def refresh_metrics(self):
        today_expense = sum(
            float(bill.get("amount", 0) or 0)
            for bill in bill_service.get_today_bills()
            if bill.get("type") == "expense"
        )
        month_expense = sum(
            float(bill.get("amount", 0) or 0)
            for bill in bill_service.get_month_bills()
            if bill.get("type") == "expense"
        )
        if self.today_value_label:
            self.today_value_label.text = format_money(today_expense)
        if self.month_value_label:
            self.month_value_label.text = format_money(month_expense)

    def go_to(self, screen_name):
        if self.manager:
            self.manager.current = screen_name

    def go_to_bill_list(self):
        if not self.manager:
            return
        bill_list_screen = self.manager.get_screen("bill_list")
        bill_list_screen.set_range("today")
        self.manager.current = "bill_list"
