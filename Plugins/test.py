import sublime, sublime_plugin

# callbacks = vars(vars()['sublime_plugin'])
#
# def log_event(event_name):
#     global callbacks
#     event_cbs = callbacks['all_callbacks'][event_name]
#     print(u"➤ `{0}` fired:".format(event_name))
#     for obj in event_cbs:
#         if obj.__class__.__name__ == "SublimeEventLogger":
#             continue
#         print(u"- {0}.{1}".format(obj.__class__.__module__, obj.__class__.__name__))
#
#
# class SublimeEventLogger(sublime_plugin.EventListener):
#     def on_selection_modified(self, view):
#         log_event('on_selection_modified')
#
#     def on_selection_modified_async(self, view):
#         log_event('on_selection_modified_async')
#
#     def on_modified(self, view):
#         log_event('on_modified')
#
#     def on_modified_async(self, view):
#         log_event('on_modified_async')

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
