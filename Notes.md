# Markdown Bugs:
- image syntax coloring is wrong
- bold and italic both together is not working
- do not draw indent lines in MD
- support definition lists
- nested list items are not highlited
- link referances does not support these two formats:
    [foo]: http://example.com/  'Optional Title Here'
    [foo]: http://example.com/  (Optional Title Here)


# TODO:
- font rendering comparison
- fix general colors of color scheme
- HTML tags in Markdown should hav different color <s></s>
- delete and close
- fade_fold_buttons should be syntax specific
- indent_to_bracket syntax specific
- LiveReload
- ruby test
- ruby debugger
- Bound​Keys

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

___

# BUG: 
- stippled_underline in not that stippled on retina
- Mac color Emoji's changed colors
- fold triangle and dots are aligned bottom

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
- Better find results 
    - Make search results readonly
    - better syntax highlighting
    - custom color scheme
    - keyboard navigation
- Sublime-Tweet (https://github.com/fukayatsu/SublimeTweetLine)
- better QuickCal
- colored tabs chaging background and setting langspecefic background as the old bg

___

# Best Practices in ST Plugin Development

## Plugins
1. limit your key bindings to a specific scope to reduce conflicts
2. do not pollute context menu, when your command is not relevant to current buffer hide it (use is_visible)

## Language Definitions

## ColorSchemes
1. what are the general settings
2. what are the bare miminum scopes
    * Base
    * tmlang Specific
    * plugin Specific

# ColorScheme General Keys:
## sublime
- background
- foreground
- caret
- lineHighlight
- invisibles
---------------
- selection
- selectionBorder
- selectionForeground
- inactiveSelection
- inactiveSelectionForeground (✱) does not exists. gets it from selectionForeground
---------------
- findHighlight
- findHighlightForeground
- findHighlightBorder (✱) does not exists. gets it from inactiveSelection
- findMatchesBorder   (✱) does not exists. gets it from caret
---------------
- guide       (✔) if indent_guide_options include 'draw_normal'
- activeGuide (✔) if indent_guide_options include 'draw_active'
- stackGuide  (✔) if indent_guide_options include 'draw_active'
---------------
- gutterForeground
- gutter
---------------
- bracketsForeground        (✔) color of the UI element used to highlight matching brackets when cursor is beside the brakets
- bracketsOptions           (✔) how to higlight matching brackets when the cursor is beside one of the brackets. values are 'foreground', 'underline', 'stippled_underline'
- bracketContentsForeground (✔) color of the UI element used to highlight matching brackets when cursor is in between matching brakets
- bracketContentsOptions    (✔) how to higlight matching brackets when the cursor is between the matching brackets. values are 'foreground', 'underline', 'stippled_underline'
---------------
- tagsOptions    (✔) how to higlight matching tags in html/xml. values are 'foreground', 'underline', 'stippled_underline'
- tagsForeground (✔) color of the UI element used to highlight matching tags
---------------
- bracketHighlight   (✘) 
- multiEditHighlight (✘)
- searchHighlight    (✘)

## textmate
```
deco.folding
colorSpaceName = 'sRGB';
gutterSettings = {
    foreground = '#004581';
    background = '#00182c';
    divider = '#00182c';
    selectionBorder = '#0C1021';
    selectionBackground = '#003767';
    selectionForeground = '#93a1a1';
    icons
    iconsHover
    iconsPressed
    selectionIcons
    selectionIconsHover
    selectionIconsPressed
};
```
