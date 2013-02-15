#################################### IMPORTS ###################################

# Std Libs
import os
import sys

# Sublime Libs
import sublime
import sublime_plugin

#################################### HELPERS ###################################

def direction_iterator():
    yield -1, 'backward', False
    yield 1, 'forward', True

def x_key(view, r):
    x,y = view.text_to_layout(r.begin())
    return (x, (r, y))

################################### COMMANDS ###################################

class auto_select_lines(sublime_plugin.TextCommand):
    def run(self, edit, check_scope=True):
        """

        Stop conditions:

            Different start x value
            New area doesnt match start scope
            Behind cursor is not space but is on new cursor
            Behind cursor is space but behind new cursor isn't
            Cursor is space but new cursor isn't
            Cursor isn't space but new cursor is
        """

        view = self.view
        start_selections = list(view.sel())
        line_height = view.line_height()
        unique_pts_first_sels = dict( x_key(view, s) for s
                                      in reversed(start_selections ))
        additional_selections = []
        x_extent, y_extent = view.layout_extent()

        for leader_x_val, (leader_r, leader_y) in unique_pts_first_sels.items():
            leader_is_space = []

            start_scope = view.scope_name(leader_r.begin()).rstrip()
            for offset in (0, -1):
                leader_is_space.append (
                        view.substr(leader_r.begin() + offset).isspace())

            for direction, direction_repr, forward in direction_iterator():
                n = 0
                while True:
                    n+=1

                    y_offset = (n * direction * line_height)
                    y_val = leader_y + y_offset
                    if y_val < 0 or y_val > y_extent: break

                    # candidate point
                    cp = view.layout_to_text((leader_x_val, y_val))
                    check_x, check_y = view.text_to_layout(cp)

                    if check_x != leader_x_val: break

                    try:
                        for offset in (0, -1):
                            candidate_is_space = (view.substr(cp + offset)
                                                      .isspace())
                            if leader_is_space[offset] != candidate_is_space:
                                raise ValueError
                    except ValueError: break

                    if check_scope and not view.match_selector(cp, start_scope):
                        break

                    additional_selections.append(sublime.Region(cp))

        view.sel().add_all(additional_selections)