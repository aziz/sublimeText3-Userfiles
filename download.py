from urllib import parse, request
from threading import Thread
from collections import namedtuple
import sublime, sublime_plugin
import time, queue, json, re
from os import listdir, walk
from os.path import join, dirname, basename, isdir

callbacks = vars(vars()['sublime_plugin'])

def get_packages_uris():
    PC_URI = "https://packagecontrol.io/packages/"
    pc = sublime.load_settings("Package Control.sublime-settings")
    installed_packages = pc.get("installed_packages")
    urls = [PC_URI + parse.quote(p) + ".json" for p in installed_packages]
    return urls


def get_url(u):
    try:
        json_str = request.urlopen(u).read().decode("utf-8")
        j = json.loads(json_str)
        last_modified = time.strptime(j["last_modified"], "%Y-%m-%dT%H:%M:%SZ")
        return j["name"], last_modified
    except:
        return "error", u


def pprinttable(rows):
    """
    Usage:
        from collections import namedtuple
        Row = namedtuple('Row',['first','second','third'])
        data = Row(1,2,3)
        pprinttable([data, data, data, data])
    """
    result = []
    if len(rows) > 1:
        headers = rows[0]._fields
        lens = []
        for i in range(len(rows[0])):
            lens.append(len(max([x[i] for x in rows] + [headers[i]], key=lambda x: len(str(x)))))
        formats = []
        hformats = []
        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            hformats.append("%%-%ds" % lens[i])
        pattern = " | ".join(formats)
        hpattern = " | ".join(hformats)
        separator = "—+—".join(['—' * n for n in lens])
        result.append(hpattern % tuple(headers))
        result.append(separator)
        for line in rows:
            result.append(pattern % tuple(line))
    elif len(rows) == 1:
        row = rows[0]
        hwidth = len(max(row._fields, key=lambda x: len(x)))
        for i in range(len(row)):
            result.append("%*s = %s" % (hwidth, row._fields[i], row[i]))
    return "\n".join(result)


def get_user_packages():
    user = set()
    for fname in listdir(sublime.packages_path()):
        path = join(sublime.packages_path(), fname)
        if isdir(path) and not(fname.startswith('.')):
            user.add(fname)
    return user


def get_dependencies():
    dependecies = set()
    for root, dirs, files in walk(sublime.packages_path()):
        if 'dependency-metadata.json' in files:
            dependecies.add(basename(root))
    return dependecies


class PackStatsTableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def_path = join(dirname(sublime.executable_path()), 'Packages')
        default = set([re.sub(r'\.sublime-package', '', p) for p in listdir(def_path)])
        user = get_user_packages() - get_dependencies()
        pc = set([re.sub(r'\.sublime-package', '', p) for p in listdir(sublime.installed_packages_path())])
        disabled = set(sublime.load_settings('Preferences.sublime-settings').get('ignored_packages', []))
        ignored = set(["User", "bz2", "0_package_control_loader", ".DS_Store"])

        enabled_def = default - disabled
        disabled_def = default - enabled_def
        pc_total = (pc | (user - default)) - ignored
        enabled_pc = pc_total - disabled
        disabled_pc = pc_total - enabled_pc
        total = (pc | user | disabled | default) - ignored
        enabled = total - disabled

        Row = namedtuple('Row', ['Type', 'Total', 'Disabled', 'Enabled'])
        row1 = Row("Built-in", len(default), len(disabled_def), len(enabled_def))
        row2 = Row("Package Control", len(pc_total), len(disabled_pc), len(enabled_pc))
        row3 = Row("Total", len(total), len(disabled), len(enabled))
        results = pprinttable([row1, row2, row3])
        sep_line = "\n————————————————————————————————————————————\n\t"

        out = self.view.window().get_output_panel("stats")
        self.view.window().run_command("show_panel", {"panel": "output.stats"})
        out.insert(edit, out.size(), results)
        out.insert(edit, out.size(), "\n\nPackage Control Packages (Enabled):" + sep_line + '\n\t'.join(sorted(enabled_pc, key=lambda s: s.lower())))
        out.insert(edit, out.size(), "\n\nPackage Control Packages (Disabled):" + sep_line + '\n\t'.join(sorted(disabled_pc, key=lambda s: s.lower())))
        out.insert(edit, out.size(), "\n\nDefault Packages (Enabled):" + sep_line + '\n\t'.join(sorted(enabled_def, key=lambda s: s.lower())))
        out.insert(edit, out.size(), "\n\nDefault Packages (Disabled):" + sep_line + '\n\t'.join(sorted(disabled_def, key=lambda s: s.lower())))


class PackStatsLastupdateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        concurrent = 200
        self.data = []
        self.q = queue.Queue(concurrent * 2)
        self.Row = namedtuple('Row', ['Package', 'Last_Update'])

        for _ in range(concurrent):
            t = Thread(target=self.doWork)
            t.daemon = True
            t.start()

        urls = get_packages_uris()
        print(len(urls))
        for u in urls:
            self.q.put(u)
        self.q.join()
        self.data.sort(key=lambda x: x[1], reverse=True)
        rows = []
        for d in self.data:
            rows.append(self.Row(d[0], time.strftime("%Y-%m-%d", d[1])))
        results = pprinttable(rows)
        out = self.view.window().get_output_panel("stats")
        self.view.window().run_command("show_panel", {"panel": "output.stats"})
        out.insert(edit, out.size(), results)

    def doWork(self):
        while True:
            url = self.q.get()
            name, last_modified = get_url(url)
            if name == "error":
                print("Error: " + last_modified)
            else:
                self.data.append((name, last_modified))
            self.q.task_done()


class PackStatsEventsReport(sublime_plugin.TextCommand):
    def run(self, edit):
        events = ["on_selection_modified", "on_selection_modified_async",
                  "on_modified", "on_modified_async",
                  "on_activated", "on_activated_async",
                  "on_deactivated", "on_deactivated_async",
                  "on_text_command", "on_post_text_command",
                  "on_window_command", "on_post_window_command",
                  "on_query_completions", "on_query_context",
                  "on_pre_close", "on_close",
                  "on_pre_save", "on_pre_save_async",
                  "on_load", "on_load_async",
                  "on_new", "on_new_async",
                  "on_post_save", "on_post_save_async",
                  "on_clone", "on_clone_async"]
        report = []
        empty_events = []
        report.append("\tAll the events registered by your installed and enabled packages:")
        report.append("\tNOTE:")
        report.append("\t  The events on the top are the most expensive ones. consider")
        report.append("\t  disabling the plugins if you are not using them.")
        report.append("—" * 70)
        for e in events:
            event = callbacks['all_callbacks'][e]
            if len(event) > 0:
                report.append("\n\t" + e)
            else:
                empty_events.append(e)

            for obj in event:
                if obj.__class__.__name__ == "SublimeEventLogger":
                    continue
                report.append(u"\t  - {0}.{1}".format(obj.__class__.__module__, obj.__class__.__name__))
        empty = "\n" + "—" * 70 + "\n\n\tEmpty Events:\n\t\t" + "\n\t\t".join(empty_events)
        x = "\n".join(report) + empty
        out = sublime.active_window().get_output_panel("event_reports")
        self.view.window().run_command("show_panel", {"panel": "output.event_reports"})
        out.insert(edit, out.size(), x)
