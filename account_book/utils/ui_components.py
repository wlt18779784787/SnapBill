from __future__ import annotations

from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from utils.font_utils import FONT_NAME


BG_COLOR = (0.96, 0.97, 0.98, 1)
CARD_COLOR = (1, 1, 1, 1)
PRIMARY_COLOR = (0.0, 0.48, 1.0, 1)
PRIMARY_DARK = (0.0, 0.38, 0.86, 1)
PRIMARY_LIGHT = (0.86, 0.93, 1, 1)
TEXT_COLOR = (0.12, 0.15, 0.19, 1)
MUTED_COLOR = (0.48, 0.52, 0.58, 1)
BORDER_COLOR = (0.88, 0.90, 0.93, 1)
DANGER_COLOR = (0.91, 0.32, 0.27, 1)
DANGER_DARK = (0.78, 0.23, 0.19, 1)


def format_money(amount):
    try:
        value = float(amount or 0)
    except (TypeError, ValueError):
        value = 0.0
    return f"\uffe5{value:.2f}"


def bind_label_height(label, padding=dp(12)):
    def _sync(*_args):
        label.text_size = (max(label.width - padding, dp(1)), None)

    def _sync_height(_instance, texture_size):
        label.height = texture_size[1] + padding

    label.bind(size=_sync, texture_size=_sync_height)
    _sync()
    return label


class RoundedCard(BoxLayout):
    bg_color = ListProperty(CARD_COLOR)
    border_color = ListProperty(BORDER_COLOR)
    shadow_color = ListProperty((0, 0, 0, 0))
    radius = NumericProperty(dp(22))
    border_width = NumericProperty(1)
    shadow_dx = NumericProperty(dp(0))
    shadow_dy = NumericProperty(dp(-1))
    shadow_blur = NumericProperty(dp(0))

    def __init__(self, **kwargs):
        kwargs.setdefault("padding", [dp(16), dp(16), dp(16), dp(16)])
        super().__init__(**kwargs)
        with self.canvas.before:
            self._shadow_color = Color(rgba=self.shadow_color)
            self._shadow = RoundedRectangle(
                pos=(self.x + self.shadow_dx, self.y + self.shadow_dy),
                size=self.size,
                radius=[self.radius],
            )
            self._bg_color = Color(rgba=self.bg_color)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            self._border_color = Color(rgba=self.border_color)
            self._border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius),
                                width=max(self.border_width, 0.01))
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            bg_color=self._update_colors,
            border_color=self._update_colors,
            shadow_color=self._update_colors,
            radius=self._update_canvas,
            border_width=self._update_canvas,
            shadow_dx=self._update_canvas,
            shadow_dy=self._update_canvas,
        )

    def _update_colors(self, *_args):
        self._shadow_color.rgba = self.shadow_color
        self._bg_color.rgba = self.bg_color
        if self.border_width <= 0:
            self._border_color.rgba = (
                self.border_color[0],
                self.border_color[1],
                self.border_color[2],
                0,
            )
        else:
            self._border_color.rgba = self.border_color

    def _update_canvas(self, *_args):
        self._shadow.pos = (self.x + self.shadow_dx, self.y + self.shadow_dy)
        self._shadow.size = self.size
        self._shadow.radius = [self.radius]
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._bg.radius = [self.radius]
        self._border.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)
        self._border.width = max(self.border_width, 0.01)


class PressableCard(ButtonBehavior, RoundedCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ShortcutTile(PressableCard):
    def __init__(self, symbol, title, accent_color=PRIMARY_COLOR, callback=None, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(88))
        kwargs.setdefault("spacing", dp(8))
        kwargs.setdefault("padding", [dp(12), dp(12), dp(12), dp(12)])
        super().__init__(**kwargs)
        self.bg_color = CARD_COLOR
        self.border_color = (0.91, 0.93, 0.96, 1)
        self.shadow_color = (0, 0, 0, 0.04)
        self.shadow_dy = dp(-2)
        self.radius = dp(20)
        self._callback = callback

        icon_circle = RoundedCard(
            orientation="vertical",
            size_hint_y=None,
            height=dp(36),
            padding=[0, 0, 0, 0],
        )
        icon_circle.radius = dp(18)
        icon_circle.bg_color = accent_color
        icon_circle.border_color = accent_color
        icon_circle.border_width = 0
        icon_circle.size_hint_x = None
        icon_circle.width = dp(36)
        icon_circle.add_widget(
            ModernLabel(
                text=symbol,
                font_size="18sp",
                bold=True,
                color=(1, 1, 1, 1),
                halign="center",
                valign="middle",
            )
        )
        icon_circle.children[0].bind(size=lambda instance, value: setattr(instance, "text_size", value))
        self.add_widget(icon_circle)

        title_label = ModernLabel(
            text=title,
            font_size="13sp",
            bold=True,
            color=TEXT_COLOR,
            size_hint_y=None,
            height=dp(18),
            halign="center",
            valign="middle",
        )
        title_label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
        self.add_widget(title_label)

    def on_release(self):
        if callable(self._callback):
            self._callback()


class ModernLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_name", FONT_NAME)
        kwargs.setdefault("color", TEXT_COLOR)
        super().__init__(**kwargs)


class TitleLabel(ModernLabel):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_size", "26sp")
        kwargs.setdefault("bold", True)
        kwargs.setdefault("color", TEXT_COLOR)
        super().__init__(**kwargs)


class SubtitleLabel(ModernLabel):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_size", "15sp")
        kwargs.setdefault("color", MUTED_COLOR)
        super().__init__(**kwargs)


class MetricValueLabel(ModernLabel):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_size", "24sp")
        kwargs.setdefault("bold", True)
        kwargs.setdefault("color", TEXT_COLOR)
        super().__init__(**kwargs)


class ModernButton(Button):
    fill_color = ListProperty(PRIMARY_COLOR)
    fill_color_down = ListProperty(PRIMARY_DARK)
    text_color = ListProperty([1, 1, 1, 1])
    border_color = ListProperty(PRIMARY_COLOR)
    radius = NumericProperty(dp(20))
    border_width = NumericProperty(0)

    def __init__(self, **kwargs):
        kwargs.setdefault("font_name", FONT_NAME)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color", kwargs.get("text_color", (1, 1, 1, 1)))
        kwargs.setdefault("size_hint_y", None)
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_color = Color(rgba=self.fill_color)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            self._outline_color = Color(rgba=self.border_color)
            self._outline = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius),
                                 width=max(self.border_width, 0.01))
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            state=self._update_state,
            text_color=self._update_text_color,
            fill_color=self._update_colors,
            fill_color_down=self._update_colors,
            border_color=self._update_colors,
            radius=self._update_canvas,
            border_width=self._update_canvas,
        )
        self._update_state()

    def _update_text_color(self, *_args):
        self.color = self.text_color

    def _update_colors(self, *_args):
        self._bg_color.rgba = self.fill_color_down if self.state == "down" else self.fill_color
        if self.border_width <= 0:
            self._outline_color.rgba = (
                self.border_color[0],
                self.border_color[1],
                self.border_color[2],
                0,
            )
        else:
            self._outline_color.rgba = self.border_color

    def _update_canvas(self, *_args):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._bg.radius = [self.radius]
        self._outline.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)
        self._outline.width = max(self.border_width, 0.01)

    def _update_state(self, *_args):
        self.color = self.text_color
        self._update_colors()


class PrimaryButton(ModernButton):
    def __init__(self, **kwargs):
        kwargs.setdefault("fill_color", PRIMARY_COLOR)
        kwargs.setdefault("fill_color_down", PRIMARY_DARK)
        kwargs.setdefault("text_color", (1, 1, 1, 1))
        kwargs.setdefault("border_color", PRIMARY_COLOR)
        kwargs.setdefault("height", dp(56))
        kwargs.setdefault("font_size", "16sp")
        super().__init__(**kwargs)


class SecondaryButton(ModernButton):
    def __init__(self, **kwargs):
        kwargs.setdefault("fill_color", CARD_COLOR)
        kwargs.setdefault("fill_color_down", (0.94, 0.95, 0.97, 1))
        kwargs.setdefault("text_color", PRIMARY_COLOR)
        kwargs.setdefault("border_color", BORDER_COLOR)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("height", dp(52))
        kwargs.setdefault("font_size", "15sp")
        super().__init__(**kwargs)


class DangerButton(ModernButton):
    def __init__(self, **kwargs):
        kwargs.setdefault("fill_color", DANGER_COLOR)
        kwargs.setdefault("fill_color_down", DANGER_DARK)
        kwargs.setdefault("text_color", (1, 1, 1, 1))
        kwargs.setdefault("border_color", DANGER_COLOR)
        kwargs.setdefault("height", dp(44))
        kwargs.setdefault("font_size", "14sp")
        super().__init__(**kwargs)


class ChipButton(ModernButton):
    def __init__(self, **kwargs):
        kwargs.setdefault("fill_color", CARD_COLOR)
        kwargs.setdefault("fill_color_down", PRIMARY_LIGHT)
        kwargs.setdefault("text_color", MUTED_COLOR)
        kwargs.setdefault("border_color", BORDER_COLOR)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("height", dp(38))
        kwargs.setdefault("font_size", "13sp")
        kwargs.setdefault("radius", dp(16))
        super().__init__(**kwargs)


class ModernTextInput(TextInput):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_name", FONT_NAME)
        kwargs.setdefault("foreground_color", TEXT_COLOR)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_active", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("multiline", True)
        kwargs.setdefault("padding", [dp(14), dp(14), dp(14), dp(14)])
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(140))
        kwargs.setdefault("cursor_color", PRIMARY_COLOR)
        kwargs.setdefault("hint_text_color", MUTED_COLOR)
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_color = Color(rgba=CARD_COLOR)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
            self._border_color = Color(rgba=BORDER_COLOR)
            self._border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)), width=1)
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *_args):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._border.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(16))


class ModernSpinner(Spinner):
    def __init__(self, **kwargs):
        kwargs.setdefault("font_name", FONT_NAME)
        super().__init__(**kwargs)


class ModernPopup(Popup):
    def __init__(self, **kwargs):
        kwargs.setdefault("title_font", FONT_NAME)
        kwargs.setdefault("separator_height", 0)
        super().__init__(**kwargs)
