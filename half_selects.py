#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime
import sublime_plugin

#################################### HELPERS ###################################

def cmp(a, b):
    return (a > b) - (a < b)

def sel_direction(sel, zero=1):
    trend = sel.b - sel.a
    if not trend: return zero
    return trend / abs(trend)

################################### LISTENERS ##################################

class ListenUp(sublime_plugin.EventListener):
    trend     = 1
    last_pt   = 0

    def on_selection_modified(self, view):
        if not view.sel(): return

        pt              = view.sel()[0].b
        ListenUp.trend  = cmp(pt, self.last_pt) or ListenUp.trend
        self.last_pt    = pt

        if view.settings().get('half_selections'):
            view.run_command('half_selections', dict(init=False))

################################### COMMANDS ###################################

class HalfSelections(sublime_plugin.TextCommand):
    def set_waiting(self, val):
        self.view.settings().set('half_selections', val)

    def run(self, edit, init=True):
        self.set_waiting(init is True)

        if init:
            self.two_stage = self.continues_on_selection_modified()
            next(self.two_stage)
        else:
            for stage in self.two_stage: stage

    def continues_on_selection_modified(self):
        view      = self.view
        sels      = list(view.sel())
        trend     = ListenUp.trend
        dirs_sels = zip([sel_direction(s, trend) for s in sels], sels)

        yield

        for (direction,  old_sel), sel in zip(dirs_sels, view.sel()):
            if direction and old_sel != sel:
                half = None

                if direction == 1:
                    if old_sel.begin() > sel.begin():
                        half = old_sel.begin(), sel.end()
                else:
                    if sel.end() > old_sel.end():
                        half = old_sel.end(), sel.begin()

                if half is not None:
                    view.sel().subtract(sel)
                    view.sel().add(sublime.Region(*half))

################################################################################