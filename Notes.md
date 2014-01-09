
# THEME:
- fold triangle/bookmark/circle 
- sidebar fade: fade selected row
- hover over labels on sidebar should highlight
- transparent tabs
- open files in sidebar has some issues

# Color Scheme:
- less scheme colors should closely match css scheme colors
- better inactiveSelection color
- cleanup and update knockdown colorScheme


# TODO:
- LiveReload-sublimetext
- ruby test
    
# Want:
- color highlighting
- better spell checker (add word, remember ignored, multi langs, scope specific)
- RTL and BIDI support
- hiding menu item from context menu that has children items (?)

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
