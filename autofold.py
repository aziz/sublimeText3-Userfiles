import sublime, sublime_plugin
import threading
from SideBarEnhancements.SideBar import *
from SideBarEnhancements.Stats import *


class AutoFold(sublime_plugin.EventListener):
    def on_load_async(self, view):
        if view.settings().get('syntax').endswith('PHP.sublime-syntax'):
            view.run_command('fold_comments')


class SideBarDonateCommand(sublime_plugin.WindowCommand):
    def is_visible(self):
        return False

    def is_enabled(self):
        return False


class SideBarEnhancementsStats(sublime_plugin.EventListener, threading.Thread):
    def __init__(self):
        pass

    def _send(self, data):
        pass
