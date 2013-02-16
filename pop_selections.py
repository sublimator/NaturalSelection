#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime_plugin

################################################################################

class PopSelections(sublime_plugin.TextCommand):
    """
     {"args": {"forward": false},
      "command": "pop_selections",
      "context": [{"key": "selection_empty",
                   "match_all": true,
                   "operand": false,
                   "operator": "equal"},
                  {"key": "num_selections",
                   "operand": 1,
                   "operator": "not_equal"}],
      "keys": ["ctrl+alt+shift+up"]},
     {"args": {"forward": true},
      "command": "pop_selections",
      "context": [{"key": "selection_empty",
                   "match_all": true,
                   "operand": false,
                   "operator": "equal"},
                  {"key": "num_selections",
                   "operand": 1,
                   "operator": "not_equal"}],
      "keys": ["ctrl+alt+shift+down"]}
    """
    def is_enabled(self, forward):
        return len(self.view.sel()) > 1

    def run(self, edit, forward=True):
        view = self.view
        view.sel().subtract(view.sel()[0 if forward else -1])

################################################################################