#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime
import sublime_plugin

################################################################################

class ReverseSelectionDirections(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        for sel in (sublime.Region(sel.b, sel.a) for sel in view.sel()):
            view.sel().add(sel)
        
        view.show(view.sel())

################################################################################