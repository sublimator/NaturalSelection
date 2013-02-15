#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime_plugin

################################################################################

class IndexableSingleSelect(sublime_plugin.TextCommand):
    def is_enabled(self, ix=0):
        sels = self.view.sel()
        try:
            sels[ix]
            return True
        except IndexError:
            return False
    def run(self, edit, ix=-1, restrict_to_visible="TODO!"):
        sels = self.view.sel()
        sel = sels[ix]
        sels.clear()
        sels.add(sel)

################################################################################