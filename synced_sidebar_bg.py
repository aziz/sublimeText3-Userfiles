#!/usr/bin/python
# -*- coding: utf-8 -*-

# later:
# enable or disable with a custom setting
# darken/lighten sidebar by a percentage
# color highlighter issue

import sublime, sublime_plugin
import codecs, json
from os import path
from plistlib import readPlist


class SidebarMatchColorScheme(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        global cache
        scheme_file = view.settings().get('color_scheme')
        if scheme_file == cache.get('color_scheme'):
            return
        color_scheme = path.normpath(scheme_file)
        path_packages = sublime.packages_path()
        plist_path = path_packages + color_scheme.replace('Packages', '')
        if plist_path.endswith("Widgets.stTheme"):
            return
        # print(plist_path)
        plist_file = readPlist(plist_path)
        color_settings = plist_file["settings"][0]["settings"]
        # print(color_settings)

        bg = color_settings.get("background", '#FFFFFF')
        fg = color_settings.get("foreground", '#000000')

        cache = {
            "bg": bg,
            "fg": fg,
            "color_scheme": scheme_file
        }
        # print("Updating sidebar BG to", cache)

        _NUMERALS = '0123456789abcdefABCDEF'
        _HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}

        def rgb(triplet):
            return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]

        def is_light(triplet):
            r, g, b = _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]
            yiq = ((r*299)+(g*587)+(b*114))/1000;
            return yiq >= 128

        def label_color(triplet):
            if is_light(triplet):
                return [30, 30, 30]
            else:
                return [220, 220, 220]

        bgc = bg.lstrip('#')

        template = [
            {
                "class": "sidebar_tree",
                "layer0.tint": rgb(bgc),
                "layer0.opacity": 1,
                "dark_content": not is_light(bgc)
            },
            {
                "class": "sidebar_label",
                "color": label_color(bgc),
            },
            {
                "class": "sidebar_heading",
                "shadow_offset": [0, 0]
            }
        ]

        json_str = json.dumps(template, sort_keys=True, indent=4, separators=(',', ': ')).encode('raw_unicode_escape')
        new_theme_file_path = path_packages + "/User/" + view.settings().get('theme')
        with codecs.open(new_theme_file_path, 'w', 'utf-8') as f:
            f.write(json_str.decode())


def plugin_loaded():
    global cache
    cache = {}
