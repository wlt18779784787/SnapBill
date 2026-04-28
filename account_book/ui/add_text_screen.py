from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from services.bill_service import bill_service
from services.llm_parser import llm_parser
from utils.ui_components import (
    BG_COLOR,
    TEXT_COLOR,
    ModernLabel,
    ModernTextInput,
    PrimaryButton,
    RoundedCard,
    SubtitleLabel,
    TitleLabel,
    bind_label_height,
)


class AddTextScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_input = None
        self.result_label = None
        self.init_ui()

    def init_ui(self):
        with self.canvas.before:
            Color(rgba=BG_COLOR)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

        root = ScrollView(do_scroll_x=False)
        content = BoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(24)],
            spacing=dp(14),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))
        root.add_widget(content)

        header = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        back_btn = PrimaryButton(text="\u8fd4\u56de\u9996\u9875", size_hint_x=None, width=dp(92), height=dp(46), font_size="14sp")
        back_btn.bind(on_press=lambda *_args: self.go_back())
        header.add_widget(back_btn)

        header_title = TitleLabel(
            text="\u6587\u5b57\u8bb0\u8d26",
            font_size="24sp",
            size_hint_x=1,
            halign="left",
            valign="middle",
            color=TEXT_COLOR,
        )
        header_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        header.add_widget(header_title)
        content.add_widget(header)

        hint_card = RoundedCard(orientation="vertical", size_hint_y=None)
        hint_card.height = dp(88)
        hint_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        hint_title = ModernLabel(
            text="\u8f93\u5165\u8d26\u5355\u5185\u5bb9",
            font_size="16sp",
            bold=True,
            color=TEXT_COLOR,
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="middle",
        )
        hint_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        hint_body = SubtitleLabel(
            text="\u4f8b\u5982\uff1a\u4eca\u5929\u4e2d\u5348\u5403\u996d\u82b1\u4e8628\u5143\uff0c\u6216\u8005\u6536\u5230\u5de5\u8d445000\u5143\u3002",
            size_hint_y=None,
            height=dp(36),
            halign="left",
            valign="top",
        )
        bind_label_height(hint_body, padding=dp(10))
        hint_card.add_widget(hint_title)
        hint_card.add_widget(hint_body)
        content.add_widget(hint_card)

        input_card = RoundedCard(orientation="vertical", size_hint_y=None)
        input_card.height = dp(180)
        input_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        self.text_input = ModernTextInput(
            hint_text="\u8bf7\u8f93\u5165\u8d26\u5355\u5185\u5bb9\uff0e\uff0e\uff0e",
            size_hint_y=None,
            height=dp(148),
        )
        input_card.add_widget(self.text_input)
        content.add_widget(input_card)

        save_btn = PrimaryButton(text="\u5206\u6790\u5e76\u4fdd\u5b58", size_hint_y=None, height=dp(56))
        save_btn.bind(on_press=lambda *_args: self.analyze_and_save())
        content.add_widget(save_btn)

        result_card = RoundedCard(orientation="vertical", size_hint_y=None)
        result_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        result_card.bind(minimum_height=result_card.setter("height"))
        self.result_label = ModernLabel(
            text="",
            font_size="14sp",
            color=TEXT_COLOR,
            size_hint_y=None,
            halign="left",
            valign="top",
        )
        bind_label_height(self.result_label, padding=dp(12))
        result_card.add_widget(self.result_label)
        content.add_widget(result_card)

        self.add_widget(root)

    def _update_rect(self, *_args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_back(self):
        self.manager.current = "home"

    def analyze_and_save(self):
        text = self.text_input.text.strip()
        if not text:
            self.result_label.text = "\u8bf7\u5148\u8f93\u5165\u8d26\u5355\u5185\u5bb9\u3002"
            return

        try:
            result = llm_parser.parse_bill_text(text)
            result["source"] = "text"
            result["raw_text"] = text

            bill_id = bill_service.add_bill(result)
            type_name = "\u6536\u5165" if result["type"] == "income" else "\u652f\u51fa"
            note_text = result["note"] or "\u65e0"
            self.result_label.text = (
                "\u89e3\u6790\u7ed3\u679c\n"
                f"\u91d1\u989d\uff1a{result['amount']} \u5143\n"
                f"\u7c7b\u578b\uff1a{type_name}\n"
                f"\u5206\u7c7b\uff1a{result['category']}\n"
                f"\u65f6\u95f4\uff1a{result['bill_time']}\n"
                f"\u5907\u6ce8\uff1a{note_text}\n"
                f"\u4fdd\u5b58\u6210\u529f\uff0cID={bill_id}"
            )
            self.text_input.text = ""
        except Exception as exc:
            self.result_label.text = f"\u89e3\u6790\u5931\u8d25\uff1a{exc}"
