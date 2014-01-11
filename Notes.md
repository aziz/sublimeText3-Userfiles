# TODO:
- delete and close
- fade_fold_buttons should be syntax specific
- LiveReload
- ruby test
- ruby debugger
- Bound​Keys

# Ask:
- what is sheet
- what is view().meta_info(key,pt)

# THEME:
- fold triangle/circle/dot
- sidebar fade: fade selected row
- hover over labels on sidebar should highlight
- transparent tabs
- open files in sidebar has some issues

# Color Scheme:
- less scheme colors should closely match css scheme colors
- better inactiveSelection color
- cleanup and update knockdown colorScheme

    
# Want:
- color highlighting
- better spell checker (add word, remember ignored, multi langs, scope specific)
- RTL and BIDI support
- hiding menu item from context menu that has children items (?)

# Wanted API:
- context for mousemaps
- "show_minimap": false,
- "show_open_files": true,
- "show_tabs": false,
- "side_bar_visible": false,
- "side_bar_width": 264.0,
- "status_bar_visible": false,
- "template_settings": {"max_columns": 1 }

# IDEA
- Non-fullscreen Distraction Free Mode 
    http://www.sublimetext.com/forum/viewtopic.php?f=4&t=15118
- Make search results readonly
- Sublime-Tweet (https://github.com/fukayatsu/SublimeTweetLine)
- better QuickCal

# Best Practices in ST Plugin Development

## Plugins
1. limit your key bindings to a specific scope to reduce conflicts
2. do not pollute context menu, when your command is not relevant to current buffer hide it (use is_visible)

## Language Definitions

## ColorSchemes


# Missing ColorScheme General Colors
``` html
<key>inactiveSelectionForeground</key>
<string>#00ff00</string>

<key>bracketsOptions</key>
<string>foreground underline</string>

<key>bracketContentsForeground</key>
<string>#ff0000</string>

<key>bracketContentsOptions</key>
<string>underline</string>

<key>tagsForeground</key>
<string>#ff0000</string>

<key>tagsOptions</key>
<string>underline</string>
```
