import sublime, sublime_plugin

class AutoFold(sublime_plugin.EventListener):
    def on_load_async(self, view):
        if view.settings().get('syntax').endswith('PHP.sublime-syntax'):
            view.run_command('fold_comments')
