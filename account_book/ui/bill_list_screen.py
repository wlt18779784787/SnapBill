from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from services.bill_service import bill_service
from utils.time_utils import format_time_for_display
from utils.ui_components import (
    BG_COLOR,
    ModernLabel,
    ChipButton,
    DangerButton,
    PrimaryButton,
    RoundedCard,
    SubtitleLabel,
    TitleLabel,
    bind_label_height,
    format_money,
)


class BillListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_range = "today"
        self.tab_buttons = {}
        self.list_container = None
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
        title = TitleLabel(text="\u67e5\u770b\u8d26\u5355", font_size="24sp", size_hint_x=1, halign="left", valign="middle")
        title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        header.add_widget(title)
        root.add_widget(header)

        tab_layout = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        ranges = [("today", "\u4eca\u65e5"), ("week", "\u672c\u5468"), ("month", "\u672c\u6708"), ("year", "\u672c\u5e74")]
        for range_key, range_name in ranges:
            btn = ChipButton(text=range_name)
            btn.bind(on_press=lambda _instance, k=range_key: self.set_range(k))
            tab_layout.add_widget(btn)
            self.tab_buttons[range_key] = btn
        root.add_widget(tab_layout)

        summary_card = RoundedCard(orientation="vertical", size_hint_y=None)
        summary_card.height = dp(70)
        summary_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        summary_card.shadow_color = (0, 0, 0, 0.035)
        summary_card.shadow_dy = dp(-1)
        self.summary_label = ModernLabel(
            text="",
            font_size="14sp",
            color=(0.38, 0.42, 0.48, 1),
            size_hint_y=None,
            halign="left",
            valign="middle",
        )
        bind_label_height(self.summary_label, padding=dp(10))
        summary_card.add_widget(self.summary_label)
        root.add_widget(summary_card)

        self.list_container = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        self.list_container.bind(minimum_height=self.list_container.setter("height"))
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.list_container)
        root.add_widget(scroll)

        self.add_widget(root)
        self.refresh_list()

    def _update_rect(self, *_args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self, *_args):
        self.refresh_list()

    def go_back(self):
        self.manager.current = "home"

    def set_range(self, range_type):
        self.current_range = range_type
        self.refresh_list()

    def _set_active_tab(self):
        for range_key, btn in self.tab_buttons.items():
            if range_key == self.current_range:
                btn.fill_color = (0.25, 0.44, 0.85, 1)
                btn.fill_color_down = (0.19, 0.34, 0.68, 1)
                btn.text_color = (1, 1, 1, 1)
                btn.border_color = (0.25, 0.44, 0.85, 1)
            else:
                btn.fill_color = (1, 1, 1, 1)
                btn.fill_color_down = (0.94, 0.95, 0.97, 1)
                btn.text_color = (0.48, 0.52, 0.58, 1)
                btn.border_color = (0.88, 0.90, 0.93, 1)
            btn._update_colors()

    def refresh_list(self):
        self.list_container.clear_widgets()
        self._set_active_tab()

        if self.current_range == "today":
            bills = bill_service.get_today_bills()
            range_label = "\u4eca\u65e5"
        elif self.current_range == "week":
            bills = bill_service.get_week_bills()
            range_label = "\u672c\u5468"
        elif self.current_range == "month":
            bills = bill_service.get_month_bills()
            range_label = "\u672c\u6708"
        elif self.current_range == "year":
            bills = bill_service.get_year_bills()
            range_label = "\u672c\u5e74"
        else:
            bills = []
            range_label = "\u5f53\u524d"

        self.summary_label.text = f"{range_label}\u5171 {len(bills)} \u7b14"

        if not bills:
            empty_card = RoundedCard(orientation="vertical", size_hint_y=None)
            empty_card.height = dp(120)
            empty_card.shadow_color = (0, 0, 0, 0.03)
            empty_card.shadow_dy = dp(-1)
            empty_label = ModernLabel(
                text="\u6682\u65e0\u8d26\u5355",
                font_size="16sp",
                bold=True,
                size_hint_y=None,
                height=dp(26),
                halign="center",
            )
            empty_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
            empty_subtitle = SubtitleLabel(
                text="\u5148\u53bb\u9996\u9875\u65b0\u589e\u4e00\u7b14\u5427\u3002",
                size_hint_y=None,
                height=dp(26),
                halign="center",
            )
            bind_label_height(empty_subtitle, padding=dp(10))
            empty_card.add_widget(empty_label)
            empty_card.add_widget(empty_subtitle)
            self.list_container.add_widget(empty_card)
            return

        for bill in bills:
            self.list_container.add_widget(self.create_bill_item(bill))

    def create_bill_item(self, bill):
        card = RoundedCard(orientation="horizontal", size_hint_y=None)
        card.height = dp(78)
        card.padding = [dp(14), dp(12), dp(14), dp(12)]
        card.spacing = dp(10)
        card.border_width = 0
        card.shadow_color = (0, 0, 0, 0.03)
        card.shadow_dy = dp(-1)

        left = BoxLayout(orientation="vertical", spacing=dp(4), size_hint_x=1)
        amount_prefix = "+" if bill["type"] == "income" else "-"
        amount_color = (0.20, 0.66, 0.36, 1) if bill["type"] == "income" else (0.89, 0.34, 0.29, 1)

        accent = RoundedCard(
            orientation="vertical",
            size_hint_x=None,
            width=dp(4),
            padding=[0, 0, 0, 0],
        )
        accent.radius = dp(4)
        accent.bg_color = amount_color
        accent.border_color = amount_color
        accent.border_width = 0
        accent.shadow_color = (0, 0, 0, 0)
        card.add_widget(accent)

        amount_label = ModernLabel(
            text=f"{amount_prefix}{format_money(bill['amount'])}  {bill['category']}",
            font_size="15sp",
            bold=True,
            color=amount_color,
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="middle",
        )
        amount_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        left.add_widget(amount_label)

        info_text = format_time_for_display(bill["bill_time"])
        if bill.get("note"):
            info_text = f"{info_text} \u00b7 {bill['note']}"
        info_label = SubtitleLabel(
            text=info_text,
            size_hint_y=None,
            height=dp(28),
            halign="left",
            valign="top",
        )
        bind_label_height(info_label, padding=dp(10))
        left.add_widget(info_label)
        card.add_widget(left)

        delete_btn = DangerButton(text="\u5220\u9664", size_hint_x=None, width=dp(68), height=dp(40), font_size="13sp")
        delete_btn.bind(on_press=lambda _instance, bid=bill["id"]: self.delete_bill(bid))
        card.add_widget(delete_btn)
        return card

    def delete_bill(self, bill_id):
        try:
            bill_service.delete_bill(bill_id)
            self.refresh_list()
        except Exception as exc:
            print(f"Delete bill failed: {exc}")
