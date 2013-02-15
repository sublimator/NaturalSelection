#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime_plugin

class AutoIncrement(sublime_plugin.TextCommand):
    def run(self, edit, shift=1):
        view = self.view

        for i, sel in enumerate(view.sel()):
            view.insert(edit, sel.begin(), str(i+shift))

class ModuloSelections(sublime_plugin.TextCommand):
    def run(self, edit, m=2, n=1):
        view = self.view

        for i, sel in enumerate(list(view.sel())):
            if not i % int(m) == int(n) - 1:
                view.sel().subtract(sel)

################################################################################