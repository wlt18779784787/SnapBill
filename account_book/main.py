import os

os.environ.setdefault("KIVY_NO_FILELOG", "1")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from utils.font_utils import register_chinese_font


class SnapBillApp(App):
    def build(self):
        register_chinese_font()

        from db.sqlite_helper import init_database
        from ui.add_image_screen import AddImageScreen
        from ui.add_text_screen import AddTextScreen
        from ui.bill_list_screen import BillListScreen
        from ui.home_screen import HomeScreen
        from ui.stats_screen import StatsScreen

        init_database()

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(AddTextScreen(name="add_text"))
        sm.add_widget(AddImageScreen(name="add_image"))
        sm.add_widget(BillListScreen(name="bill_list"))
        sm.add_widget(StatsScreen(name="stats"))
        return sm


if __name__ == "__main__":
    Window.size = (360, 640)
    Window.clearcolor = (0.96, 0.97, 0.98, 1)
    Window.set_title("SnapBill")
    SnapBillApp().run()
