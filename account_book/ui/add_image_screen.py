from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import Screen

from services.bill_service import bill_service
from services.llm_parser import llm_parser
from services.ocr_service import ocr_service
from utils.ui_components import (
    BG_COLOR,
    ModernLabel,
    ModernPopup,
    PrimaryButton,
    RoundedCard,
    SubtitleLabel,
    TitleLabel,
    bind_label_height,
)


class AddImageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_image = None
        self.ocr_result = None
        self.path_label = None
        self.ocr_label = None
        self.result_label = None
        self.init_ui()

    def init_ui(self):
        with self.canvas.before:
            Color(rgba=BG_COLOR)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(20), dp(20), dp(20)], spacing=dp(14))

        header = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(10))
        back_btn = PrimaryButton(text="\u8fd4\u56de\u9996\u9875", size_hint_x=None, width=dp(92), height=dp(46), font_size="14sp")
        back_btn.bind(on_press=lambda *_args: self.go_back())
        header.add_widget(back_btn)

        title = TitleLabel(
            text="\u56fe\u7247\u8bb0\u8d26",
            font_size="24sp",
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        header.add_widget(title)
        root.add_widget(header)

        hint_card = RoundedCard(orientation="vertical", size_hint_y=None)
        hint_card.height = dp(92)
        hint_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        hint_title = ModernLabel(
            text="\u9009\u62e9\u7968\u636e\u56fe\u7247",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height=dp(24),
            halign="left",
            valign="middle",
        )
        hint_title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        hint_body = SubtitleLabel(
            text="\u5148\u9009\u56fe\u7247\uff0c\u518d\u8bc6\u522b\u6587\u5b57\uff0c\u6700\u540e\u4e00\u952e\u4fdd\u5b58\u5230\u8d26\u5355\u3002",
            size_hint_y=None,
            height=dp(34),
            halign="left",
            valign="top",
        )
        bind_label_height(hint_body, padding=dp(10))
        hint_card.add_widget(hint_title)
        hint_card.add_widget(hint_body)
        root.add_widget(hint_card)

        select_btn = PrimaryButton(text="\u9009\u62e9\u56fe\u7247", size_hint_y=None, height=dp(56))
        select_btn.bind(on_press=lambda *_args: self.show_file_chooser())
        root.add_widget(select_btn)

        info_card = RoundedCard(orientation="vertical", size_hint_y=None)
        info_card.height = dp(76)
        info_card.padding = [dp(16), dp(16), dp(16), dp(16)]
        self.path_label = ModernLabel(
            text="\u672a\u9009\u62e9\u56fe\u7247",
            font_size="14sp",
            color=(0.45, 0.49, 0.55, 1),
            size_hint_y=None,
            halign="left",
            valign="middle",
        )
        bind_label_height(self.path_label, padding=dp(10))
        info_card.add_widget(self.path_label)
        root.add_widget(info_card)

        ocr_btn = PrimaryButton(text="\u8bc6\u522b\u56fe\u7247\u6587\u5b57", size_hint_y=None, height=dp(56))
        ocr_btn.bind(on_press=lambda *_args: self.recognize_image())
        root.add_widget(ocr_btn)

        self.ocr_label = self._build_result_card(root, "OCR \u7ed3\u679c")
        self.result_label = self._build_result_card(root, "\u4fdd\u5b58\u7ed3\u679c")

        save_btn = PrimaryButton(text="\u5206\u6790\u5e76\u4fdd\u5b58", size_hint_y=None, height=dp(56))
        save_btn.bind(on_press=lambda *_args: self.analyze_and_save())
        root.add_widget(save_btn)

        self.add_widget(root)

    def _build_result_card(self, root, title_text):
        card = RoundedCard(orientation="vertical", size_hint_y=None)
        card.padding = [dp(16), dp(16), dp(16), dp(16)]
        title = ModernLabel(
            text=title_text,
            font_size="15sp",
            bold=True,
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
        )
        title.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        label = ModernLabel(
            text="",
            font_size="14sp",
            color=(0.26, 0.29, 0.34, 1),
            size_hint_y=None,
            halign="left",
            valign="top",
        )
        bind_label_height(label, padding=dp(12))
        card.add_widget(title)
        card.add_widget(label)
        card.bind(minimum_height=card.setter("height"))
        root.add_widget(card)
        return label

    def _update_rect(self, *_args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_back(self):
        self.manager.current = "home"

    def show_file_chooser(self):
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=[dp(12), dp(12), dp(12), dp(12)])
        file_chooser = FileChooserIconView(path=".", filters=["*.png", "*.jpg", "*.jpeg", "*.gif"])
        content.add_widget(file_chooser)

        btn_layout = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(10))
        cancel_btn = PrimaryButton(text="\u53d6\u6d88", size_hint_x=1, height=dp(46), font_size="14sp")
        confirm_btn = PrimaryButton(text="\u786e\u5b9a", size_hint_x=1, height=dp(46), font_size="14sp")
        popup = ModernPopup(title="\u9009\u62e9\u56fe\u7247", content=content, size_hint=(0.92, 0.92))

        cancel_btn.bind(on_press=lambda *_args: popup.dismiss())

        def on_confirm(_instance):
            if file_chooser.selection:
                self.selected_image = file_chooser.selection[0]
                self.path_label.text = self.selected_image
            popup.dismiss()

        confirm_btn.bind(on_press=on_confirm)
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(confirm_btn)
        content.add_widget(btn_layout)
        popup.open()

    def recognize_image(self):
        if not self.selected_image:
            self.ocr_label.text = "\u8bf7\u5148\u9009\u62e9\u56fe\u7247\u3002"
            return

        try:
            self.ocr_result = ocr_service.recognize_image(self.selected_image)
            self.ocr_label.text = f"OCR \u8bc6\u522b\u7ed3\u679c\uff1a\n{self.ocr_result}"
        except Exception as exc:
            self.ocr_label.text = f"OCR \u8bc6\u522b\u5931\u8d25\uff1a{exc}"

    def analyze_and_save(self):
        if not self.ocr_result:
            self.result_label.text = "\u8bf7\u5148\u8bc6\u522b\u56fe\u7247\u3002"
            return

        try:
            result = llm_parser.parse_bill_text(self.ocr_result)
            result["source"] = "image"
            result["raw_text"] = self.ocr_result
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
            self.ocr_result = None
        except Exception as exc:
            self.result_label.text = f"\u89e3\u6790\u5931\u8d25\uff1a{exc}"
