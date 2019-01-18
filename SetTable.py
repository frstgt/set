import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, cairo

class EditCodeDialog(Gtk.Dialog):

    def __init__(self, win_title, parent, name, code):
        Gtk.Dialog.__init__(self, win_title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(400, 300)

        vbox = self.get_content_area()

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        scrolledwindow.add(self.textview)
        vbox.pack_start(scrolledwindow, True, True, 0)

        self.set_name_code(name, code)

        self.show_all()

    def set_name_code(self, name, code):
        self.entry.set_text(name)
        self.textview.get_buffer().set_text(code)
    def get_name_code(self):
        name = self.entry.get_text()
        buffer = self.textview.get_buffer()
        code = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), False)
        return [name, code]


class StateButton(Gtk.ToggleButton):

    id = 1
    def __init__(self, name=None, code=""):
        if name == None:
            name = "State" + str(StateButton.id)
        StateButton.id += 1
        Gtk.ToggleButton.__init__(self, name)

        self.code = code

    def set_code(self, code):
        self.code = code
    def get_code(self):
        return self.code
    def set_name(self, name):
        self.set_label(name)
    def get_name(self):
        return self.get_label()
    def set_name_code(self, name, code):
        self.set_label(name)
        self.code = code
    def get_name_code(self):
        return [self.get_label(), self.code]

    def edit_code(self, win_title, parent):
        
        name, code = self.get_name_code()
        dialog = EditCodeDialog(win_title, parent, name, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name, code = dialog.get_name_code()
            self.set_name_code(name, code)

        dialog.destroy()


class EventButton(Gtk.ToggleButton):

    id = 1
    def __init__(self, name=None, code=""):
        if name == None:
            name = "State" + str(EventButton.id)
        EventButton.id += 1
        Gtk.ToggleButton.__init__(self, name)

        self.code = code

    def set_code(self, code):
        self.code = code
    def get_code(self):
        return self.code
    def set_name(self, name):
        self.set_label(name)
    def get_name(self):
        return self.get_label()
    def set_name_code(self, name, code):
        self.set_label(name)
        self.code = code
    def get_name_code(self):
        return [self.get_label(), self.code]

    def edit_code(self, win_title, parent):
        
        name, code = self.get_name_code()
        dialog = EditCodeDialog(win_title, parent, name, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name, code = dialog.get_name_code()
            self.set_name_code(name, code)

        dialog.destroy()


class StateEventTable(Gtk.Grid):

    id = 1
    def __init__(self, name=None):
        Gtk.Grid.__init__(self)

        if name == None:
            self.name = "Table" + str(StateEventTable.id)
        else:
            self.name = name
        StateEventTable.id += 1

        self.states = [] # button
        self.events = []
        self.current_state = None # button
        self.current_event = None

        self.changed = False

    def get_changed(self):
        return self.changed
    def clear_changed(self):
        self.changed = False

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name 

    def get_numof_states(self):
        return len(self.states)
    def get_numof_events(self):
        return len(self.events)

    def get_nth_state(self, nth):
        return self.states[nth].get_name_code()
    def get_nth_event(self, nth):
        return self.events[nth].get_name_code()

    def get_tr(self, si, ei):
        cmb = self.get_child_at(ei+1, si+1)
        return cmb.get_active()
    def set_tr(self, si, ei, tsi):
        cmb = self.get_child_at(ei+1, si+1)
        cmb.set_active(tsi)

        self.changed = True

    def get_current_state_pos(self):
        return self.states.index(self.current_state)
    def get_current_event_pos(self):
        return self.events.index(self.current_event)

        #

    def edit_state(self, parent):
        button = self.current_state
        name = button.get_name()
        button.edit_code("Edit State: " + name, parent)

        self.changed = True
        self.show_all()

    def append_state(self, name=None, code=""):
        sn = len(self.states)

        button = StateButton(name, code)
        name = button.get_name()
        button.connect("clicked", self.on_clicked_for_state)
        button.clicked()

        self.states.insert(sn, button)

        self.insert_row(sn+1)
        self.attach(button, 0, sn+1, 1, 1)
        for si, st1 in enumerate(self.states):
            if si != sn:
                for ei, ev in enumerate(self.events):
                    combo = self.get_child_at(ei+1, si+1)
                    combo.insert_text(sn+1, name)
            else:
                for ei, ev in enumerate(self.events):
                    combo = Gtk.ComboBoxText()
                    combo.append_text("")
                    for st2 in self.states:
                        if st2 != button:
                            nm2 = st2.get_name()
                            combo.append_text(nm2)
                    self.attach(combo, ei+1, sn+1, 1, 1)

        self.changed = True
        self.show_all()

    def remove_state(self):

        pos = self.get_current_state_pos()

        del self.states[pos]

        self.remove_row(pos+1)
        for si, st in enumerate(self.states):
            for ei, ev in enumerate(self.events):
                combo = self.get_child_at(ei+1, si+1)
                combo.remove(pos+1)
        if pos >= len(self.states):
            pos = len(self.states)-1
        self.current_state = self.get_child_at(0, pos+1)

        self.changed = True
        self.show_all()

        #

    def edit_event(self, parent):
        button = self.current_event
        name = button.get_name()
        button.edit_code("Edit Event: " + name, parent)

        self.changed = True
        self.show_all()

    def append_event(self, name=None, code=""):
        en = len(self.events)

        button = EventButton(name, code)
        name = button.get_name()
        button.connect("clicked", self.on_clicked_for_event)
        button.clicked()

        self.events.insert(en, button)

        self.insert_column(en+1)
        self.attach(button, en+1, 0, 1, 1)
        for si, st1 in enumerate(self.states):
            combo = Gtk.ComboBoxText()
            combo.append_text("")
            for st2 in self.states:
                if st2 != st1:
                    nm2 = st2.get_name()
                    combo.append_text(nm2)
            self.attach(combo, en+1, si+1, 1, 1)

        self.changed = True
        self.show_all()

    def remove_event(self):

        pos = self.get_current_event_pos()

        del self.events[pos]

        self.remove_column(pos+1)
        if pos >= len(self.events):
            pos = len(self.events)-1
        self.current_evnet = self.get_child_at(pos+1, 0)

        self.changed = True
        self.show_all()

        #

    def on_clicked_for_state(self, button):
        if button.get_active():
            self.current_state = button
            for st in self.states:
                if st != button:
                    st.set_active(False)
            self.show_all()
        else:
            if self.current_state == button:
                button.set_active(True)

    def on_clicked_for_event(self, button):
        if button.get_active():
            self.current_event = button
            for ev in self.events:
                if ev != button:
                    ev.set_active(False)
            self.show_all()
        else:
            if self.current_event == button:
                button.set_active(True)


class StateEventTables(Gtk.Notebook):

    def __init__(self):
        Gtk.Notebook.__init__(self)

        self.changed = False
        self.connect("page_reordered", self.on_page_reordered)

    def get_changed(self):
        tn = self.get_numof_tables()
        for ti in range(tn):
            table = self.get_nth_table(ti)
            if table.get_changed():
                return True
        return self.changed
    def clear_changed(self):
        tn = self.get_numof_tables()
        for ti in range(tn):
            table = self.get_nth_table(ti)
            table.clear_changed()
        self.changed = False

    def get_numof_tables(self):
        return self.get_n_pages()
    def get_nth_table(self, ti):
        return self.get_nth_page(ti)
    def get_table_name(self, table):
        label = self.get_tab_label(table)
        return label.get_text()

    def get_current_table(self):
        page = self.get_current_page()
        table = self.get_nth_page(page)
        return table

    def append_table(self, name):

        table = StateEventTable(name)
        name = table.get_name()

        self.append_page(table, Gtk.Label(name))
        self.set_tab_reorderable(table, True)

        self.changed = True
        self.show_all()

    def remove_table(self):
        page = self.get_current_page()
        self.remove_page(page)

        self.changed = True
        self.show_all()

    def remove_nth_table(self, nth):
        self.remove_page(nth)

        self.changed = True
        self.show_all()

    def on_page_reordered(self, notebook, child, page_num):
        self.changed = True

# end of file
