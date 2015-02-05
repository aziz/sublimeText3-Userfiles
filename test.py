import sublime, sublime_plugin
import time
from urllib import request
from urllib.parse import quote


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
        for u in urls[-5:]:
            json_str = request.urlopen(u).read().decode("utf-8")
            json = sublime.decode_value(json_str)
            last_modified = time.strptime(json["last_modified"], "%Y-%m-%dT%H:%M:%SZ")
            data.append((json["name"], last_modified))
        data.sort(key=lambda x: x[1], reverse=True)
        max_name = len(max(data, key=lambda x: len(x[0]))[0])

        def print_line(d):
            return " | " + d[0] + " " * (max_name - len(d[0])) + " | " + time.strftime("%Y-%m-%d", d[1]) + " | "

        lines = (print_line(d) for d in data)
        x = "\n".join(lines)
        out = self.view.window().get_output_panel("pack_stats")
        self.view.window().run_command("show_panel", {"panel": "output.pack_stats"})
        out.set_syntax_file("Packages/DrMonthsCalendar/DrCalendar.tmLanguage")
        out.set_read_only(False)
        out.insert(edit, out.size(), x)


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
