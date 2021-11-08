import fsgs
import fsui
from launcher.option import Option
from launcher.settings.settings_page import SettingsPage


class ArcadeSettingsPage(SettingsPage):
    def __init__(self, parent):
        super().__init__(parent)
        icon = fsui.Icon("fs-uae-arcade", "pkg:launcher")
        self.add_header(icon, "{} Arcade".format(fsgs.product))
        self.add_option(Option.ARCADE_FULLSCREEN)
        self.add_option(Option.ARCADE_THEME)
        self.add_option(Option.ARCADE_INITIAL_FAVORITES)
