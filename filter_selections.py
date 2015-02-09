#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime_plugin

################################### COMMANDS ###################################

class SelectionFilterBase(sublime_plugin.TextCommand):
    def is_enabled(self):
        return len(self.view.sel()) > 1
    def run(self, edit, **args):
        self.setup(self.view)
        filter_sels(self.view, self.filter_func)
        self.view.show(self.view.sel())
    def setup(self, view):
        pass

class RemoveDuplicateSelections(sublime_plugin.TextCommand):
    def run(self, edit):
        replace_sels(self.view, list(
            dict((self.view.substr(s), s) for s in reversed(self.view.sel()))
                .values()))

class RestrictSelectionsToVisibleRegion(SelectionFilterBase):
    def is_enabled(self):
        vis = self.view.visible_region()
        enabled = len([r for r in self.view.sel() if vis.intersects(r)]) > 0
        return enabled

    def setup(self, view):
        self.visible_region = view.visible_region()
    def filter_func(self, s):
        return self.visible_region.contains(s)

class RemoveEmptySelections(SelectionFilterBase):
    def filter_func(self, s):
        return not s.empty()

#################################### HELPERS ###################################

def filter_sels(view, filter_func):
    selection_set = view.sel()
    for i in range(len(selection_set)-1, -1, -1):
        if not filter_func(selection_set[i]): del selection_set[i]
    return selection_set

def replace_sels(view, new_sels):
    view.sel().clear()
    view.sel().add_all(new_sels)
    view.show(view.sel())

################################################################################
