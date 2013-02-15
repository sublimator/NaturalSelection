#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime
import sublime_plugin

from .region_helpers import normalized_region, normalized_regions,\
                            subtract_region, PyRegionSet

################################### CONSTANTS ##################################

INIT          = 'init'
STOREEMPTYS   = 'store_emptys'
MERGE         = 'merge'

KEY           = 'auto_select'
SCOPE         = 'autoselect'
FLAGS         = 1

DEBUG         = 0
ALL_TESTS     = 1
TESTS         = 0

##################################### DEBUG ####################################

def debug(*args):
    if DEBUG: print(args)

################################################################################

def auto_on(view):
    view.settings().set(KEY, True)
    view.set_status(KEY,  '%s: on' % KEY.title())

def auto_off(view):
    view.settings().set(KEY, False)
    view.erase_status(KEY)

class AutoSelectListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        if view.settings().get(KEY):
            cmd = view.command_history(0)[:2]

            def do():
                view.run_command('undo')
                view.run_command('auto_select', {'cmd' : 'merge'})
                view.run_command(*cmd)

            view.settings().set(KEY, False)
            sublime.set_timeout(do, 0)

    def on_selection_modified(self, view):
        if view.settings().get(KEY):
            has_one_sel = len(view.sel()) == 1

            if all(s.empty() for s in view.sel()) or has_one_sel:
                existing_regions = PyRegionSet (
                    normalized_regions( view.get_regions(KEY)) )
                sels = [s for s in view.get_regions(KEY + '.selections' ) if s]

                for sel in normalized_regions(sels):
                    if existing_regions.contains(sel) and not has_one_sel:
                        existing_regions.subtract(sel)
                    else:
                        existing_regions.add(sel)

                view.add_regions(KEY, existing_regions, scope=SCOPE,
                                                        flags=FLAGS)

            view.add_regions( KEY+'.selections', regions=list(view.sel()),
                                                 scope='',
                                                 flags=sublime.HIDDEN )

class SplitExtents(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        view = self.view
        sels = list(view.sel())
        view.sel().clear()

        for sel in sels:
            for pt in (sel.begin(), sel.end()):
                view.sel().add(sublime.Region(pt))

        view.run_command('auto_select')

class AutoSelect(sublime_plugin.TextCommand):
    def run(self, edit, cmd=INIT):
        view = self.view

        if cmd == INIT:
            view.erase_regions(KEY+'.selections')
            view.erase_regions(KEY)
            view.add_regions(KEY, list(s for s in view.sel() if not s),
                                  scope=SCOPE, flags=FLAGS)
            return auto_on(view)

        if cmd == STOREEMPTYS:
            regions = PyRegionSet(view.get_regions(KEY))

            if all(regions.contains(s) for s in view.sel()):
                cmd = MERGE
            else:
                return view.add_regions( KEY,
                                         regions=regions + list(view.sel()),
                                         scope=SCOPE,  flags=FLAGS )

        if cmd == MERGE:
            auto_selected = view.get_regions(KEY)

            if auto_selected:
                existing = list(normalized_regions(view.sel()))
                view.sel().clear()
                for sel in auto_selected + existing: view.sel().add(sel)
                view.erase_regions(KEY)

            auto_off(view)