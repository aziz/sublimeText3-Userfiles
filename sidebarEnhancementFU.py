from SideBarEnhancements.SideBar import *

class SideBarDonateCommand(sublime_plugin.WindowCommand):
    def is_visible(self):
        return False

    def is_enabled(self):
        return False
