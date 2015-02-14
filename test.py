import sublime, sublime_plugin
import time
from urllib import request
from urllib.parse import quote
from os import path, listdir
from os.path import join, dirname
import re
from collections import namedtuple

# ------------------------------------------------------------------------------

callbacks = vars(vars()['sublime_plugin'])


def log_event(event_name):
    global callbacks
    event_cbs = callbacks['all_callbacks'][event_name]
    print(u"➤ `{0}` fired:".format(event_name))
    for obj in event_cbs:
        if obj.__class__.__name__ == "SublimeEventLogger":
            continue
        print(u"- {0}.{1}".format(obj.__class__.__module__, obj.__class__.__name__))


class SublimeEventReport(sublime_plugin.TextCommand):
    def run(self, edit):
        events = ["on_selection_modified", "on_selection_modified_async", "on_modified", "on_modified_async", "on_activated", "on_deactivated", "on_activated_async", "on_deactivated_async", "on_text_command", "on_post_text_command", "on_window_command", "on_post_window_command", "on_query_completions", "on_query_context", "on_pre_close", "on_pre_save", "on_pre_save_async", "on_close", "on_load", "on_load_async", "on_new", "on_new_async", "on_post_save", "on_post_save_async", "on_clone", "on_clone_async"]
        report = []
        empty_events = []
        report.append("All the events registered by your installed and enabled packages:")
        report.append("NOTE:")
        report.append("  The events on the top are the most expensive ones. please consider")
        report.append("  disabling the plugins if you are not using them.")
        report.append("-"*70)
        for e in events:
            event = callbacks['all_callbacks'][e]
            if len(event) > 0:
                report.append(e)
            else:
                empty_events.append(e)

            for obj in event:
                if obj.__class__.__name__ == "SublimeEventLogger":
                    continue
                report.append(u"  - {0}.{1}".format(obj.__class__.__module__, obj.__class__.__name__))
        empty = "\n" + "-" * 70 + "\nEmpty Events:\n" + "\n".join(empty_events)
        x = "\n".join(report) + empty
        out = sublime.active_window().get_output_panel("event_reports")
        self.view.window().run_command("show_panel", {"panel": "output.event_reports"})
        out.insert(edit, out.size(), x)


# class SublimeEventLogger(sublime_plugin.EventListener):
#     def on_selection_modified(self, view):
#         log_event('on_selection_modified')

#     def on_selection_modified_async(self, view):
#         log_event('on_selection_modified_async')

#     def on_modified(self, view):
#         log_event('on_modified')

#     def on_modified_async(self, view):
#         log_event('on_modified_async')

# ------------------------------------------------------------------------------


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
        separator = "-+-".join(['-' * n for n in lens])
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


class PackStatsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        default = set([re.sub(r'\.sublime-package', '', p) for p in listdir(join(dirname(sublime.executable_path()), 'Packages'))])
        user = set(listdir(sublime.packages_path()))
        pc = set([re.sub(r'\.sublime-package', '', p) for p in listdir(sublime.installed_packages_path())])
        disabled = set(sublime.load_settings('Preferences.sublime-settings').get('ignored_packages', []))
        ignored = set(["User", "bz2", "0_package_control_loader"])

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

        out = self.view.window().get_output_panel("pack_stats")
        self.view.window().run_command("show_panel", {"panel": "output.pack_stats"})
        out.insert(edit, out.size(), results)


# ------------------------------------------------------------------------------


def get_packages_uris():
    PC_URI = "https://packagecontrol.io/packages/"
    pc = sublime.load_settings("Package Control.sublime-settings")
    installed_packages = pc.get("installed_packages")
    urls = [PC_URI + quote(p) + ".json" for p in installed_packages]
    return urls


class PackagesStatsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        urls = get_packages_uris()
        data = []
        Row = namedtuple('Row', ['Package', 'Last_Update'])
        for u in urls[-50:]:
            json_str = request.urlopen(u).read().decode("utf-8")
            json = sublime.decode_value(json_str)
            last_modified = time.strptime(json["last_modified"], "%Y-%m-%dT%H:%M:%SZ")
            data.append((json["name"], last_modified))
        data.sort(key=lambda x: x[1], reverse=True)
        rows = []
        for d in data:
            rows.append(Row(d[0], time.strftime("%Y-%m-%d", d[1])))
        results = pprinttable(rows)
        out = self.view.window().get_output_panel("pack_stats")
        self.view.window().run_command("show_panel", {"panel": "output.pack_stats"})
        out.insert(edit, out.size(), results)


# ------------------------------------------------------------------------------
# TODO: remember selection and move back to selection after insert
class PrintAtPosCommand(sublime_plugin.TextCommand):
    def run(self, edit, row, col, text):
        v = self.view
        orig_sel = v.sel()
        text_lines = text.splitlines()

        # checkin if we need to add new line to put all content
        rows_current = v.rowcol(v.size())[0]
        rows_needed = len(text_lines) + row
        if rows_current < rows_needed:
            new_lines = "\n" * (rows_needed - rows_current)
            v.insert(edit, v.size(), new_lines)

        # inserting new content
        for i in range(len(text_lines)):
            current_state = self.get_line(i + row)
            final_line_str = current_state["content"]
            if len(current_state["content"]) < col:
                final_line_str += " " * (col - len(current_state["content"]) - 1)
            final_line_str = final_line_str[:col] + text_lines[i] + final_line_str[col + len(text_lines[i]):]
            v.replace(edit, current_state["region"], final_line_str)

        # restoring cursor position
        print(orig_sel)
        print(sublime.Region(orig_sel))
        v.sel().clear()
        v.sel().add_all(orig_sel)

    def get_line(self, row):
        v = self.view
        start_of_line_p = v.text_point(row, 0)
        full_line_r = v.line(start_of_line_p)
        return {"region": full_line_r, "content": v.substr(full_line_r)}


class TestPrintAtPosCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = """     January 2015
Mo Tu We Th Fr Sa Su
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
"""
        new_text = """     March 2015
Mo Tu We Th Fr Sa Su
                   1
 2  3  4  5  6  7  8
 9 10 11 12 13 14 15
16 17 18 19 20 21 22
23 24 25 26 27 28 29
30 31
"""
        v = self.view
        v.set_scratch(True)
        v.insert(edit, v.size(), text)
        # v.run_command("print_at_pos", {"row": 1, "col": 56, "text": text})
        # v.run_command("print_at_pos", {"row": 3, "col": 25, "text": new_text})
        v.run_command("print_at_pos", {"row": 5, "col": 0, "text": new_text})
