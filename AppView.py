import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, cairo

class EditNameDialog(Gtk.Dialog):

    def __init__(self, win_title, parent, name):
        Gtk.Dialog.__init__(self, win_title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(200, 50)

        vbox = self.get_content_area()

        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)

        self.set_name(name)

        self.show_all()

    def set_name(self, name):
        self.entry.set_text(name)
    def get_name(self):
        return self.entry.get_text()

class EditCodeDialog(Gtk.Dialog):

    def __init__(self, win_title, parent, code):
        Gtk.Dialog.__init__(self, win_title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(400, 300)

        vbox = self.get_content_area()

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        scrolledwindow.add(self.textview)
        vbox.pack_start(scrolledwindow, True, True, 0)

        self.set_code(code)

        self.show_all()

    def set_code(self, code):
        self.textview.get_buffer().set_text(code)
    def get_code(self):
        buffer = self.textview.get_buffer()
        code = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), False)
        return code


class StateButton(Gtk.ToggleButton):

    def __init__(self, name=None, code=""):
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


class EventButton(Gtk.ToggleButton):

    def __init__(self, name=None, code=""):
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


class StateEventTable(Gtk.Grid):

    state_id = 1
    event_id = 1
    def __init__(self, name=None):
        Gtk.Grid.__init__(self)

        self.states = [] # button
        self.events = []
        self.current_state = None # button
        self.current_event = None

        self.changed = False

    def get_changed(self):
        return self.changed
    def clear_changed(self):
        self.changed = False

    def clear_data(self):
        sn = len(self.states)
        for si in range(sn):
            self.remove_row(si+1)
        self.remove_row(0)

        self.states = []
        self.events = []
        self.current_state = None
        self.current_event = None
        self.changed = False

        StateEventTable.state_id = 1
        StateEventTable.event_id = 1

    def get_data(self):
        sd = []
        sn = len(self.states)
        for si in range(sn):
            sname, scode = self.states[si].get_name_code()
            sd.append([sname, scode])

        ed = []
        en = len(self.events)
        for ei in range(en):
            ename, ecode = self.events[ei].get_name_code()
            ed.append([ename, ecode])

        trd = []
        for si in range(sn):
            for ei in range(en):
                cmb = self.get_child_at(ei+1, si+1)
                tsi = cmb.get_active()
                trd.append([si, ei, tsi])

        return [sd, ed, trd]

    def set_data(self, data):
        sd, ed, trd = data

        for sname, scode in sd:
            self.append_state(sname, scode)

        for ename, ecode in ed:
            self.append_event(ename, ecode)

        for si, ei, tsi in trd:
            cmb = self.get_child_at(ei+1, si+1)
            cmb.set_active(tsi)

        #

    def edit_state_name(self, parent):
        button = self.current_state
        if button == None:
            return

        old_name = button.get_name()
        dialog = EditNameDialog("Edit State Name: " + old_name, parent,
                                old_name)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            new_name = dialog.get_name()
            button.set_name(new_name)

            sn = len(self.states)
            en = len(self.events)
            sp = self.states.index(self.current_state)
            for si in range(sn):
                for ei in range(en):
                    if si < sp:
                        combo = self.get_child_at(ei+1, si+1)
                        combo.remove(sp)
                        combo.insert_text(sp, new_name)
                    elif si > sp:
                        combo = self.get_child_at(ei+1, si+1)
                        combo.remove(sp+1)
                        combo.insert_text(sp+1, new_name)
                    else:
                        pass

        dialog.destroy()

        self.changed = True
        self.show_all()

    def edit_state_code(self, parent):
        button = self.current_state
        if button == None:
            return

        name, code = button.get_name_code()
        dialog = EditCodeDialog("Edit State Code: " + name, parent, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            code = dialog.get_code()
            button.set_code(code)

        dialog.destroy()

        self.changed = True
        self.show_all()

    def append_state(self, name=None, code=""):

        if name == None:
            name = "State" + str(StateEventTable.state_id)
        StateEventTable.state_id += 1

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
                    combo.connect("changed", self.on_changed)
                    combo.append_text("")
                    for st2 in self.states:
                        if st2 != button:
                            nm2 = st2.get_name()
                            combo.append_text(nm2)
                    self.attach(combo, ei+1, sn+1, 1, 1)

        self.changed = True
        self.show_all()

    def remove_state(self):
        button = self.current_state
        if button == None:
            return

        sp = self.states.index(self.current_state)

        del self.states[sp]

        self.remove_row(sp+1)
        for si, st in enumerate(self.states):
            for ei, ev in enumerate(self.events):
                combo = self.get_child_at(ei+1, si+1)
                combo.remove(sp+1)
        if sp >= len(self.states):
            sp = len(self.states)-1
        self.current_state = self.get_child_at(0, sp+1)

        self.changed = True
        self.show_all()

        #

    def edit_event_name(self, parent):
        button = self.current_event
        if button == None:
            return

        name = button.get_name()
        dialog = EditNameDialog("Edit Event Name: " + name, parent, name)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name = dialog.get_name()
            button.set_name(name)

        dialog.destroy()

        self.changed = True
        self.show_all()

    def edit_event_code(self, parent):
        button = self.current_event
        if button == None:
            return

        name, code = button.get_name_code()
        dialog = EditCodeDialog("Edit Event Code: " + name, parent, code)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            code = dialog.get_code()
            button.set_code(code)

        dialog.destroy()

        self.changed = True
        self.show_all()

    def append_event(self, name=None, code=""):
        if name == None:
            name = "Event" + str(StateEventTable.event_id)
        StateEventTable.event_id += 1

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
            combo.connect("changed", self.on_changed)
            combo.append_text("")
            for st2 in self.states:
                if st2 != st1:
                    nm2 = st2.get_name()
                    combo.append_text(nm2)
            self.attach(combo, en+1, si+1, 1, 1)

        self.changed = True
        self.show_all()

    def remove_event(self):
        button = self.current_event
        if button == None:
            return

        ep = self.events.index(self.current_event)

        del self.events[ep]

        self.remove_column(ep+1)
        if ep >= len(self.events):
            ep = len(self.events)-1
        self.current_evnet = self.get_child_at(ep+1, 0)

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

    def on_changed(self, combo_box):
        self.changed = True

class StateEventTables(Gtk.Notebook):

    def __init__(self):
        Gtk.Notebook.__init__(self)

        self.id = 1
        self.changed = False
        self.connect("page_reordered", self.on_page_reordered)

    def get_changed(self):
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            if table.get_changed():
                return True
        return self.changed
    def clear_changed(self):
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            table.clear_changed()
        self.changed = False

    def clear_data(self):
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            table.clear_data()
            self.remove_page(ti)

        self.id = 1

    def set_data(self, data):
        for ti, name_data in enumerate(data):
            tname, tdata = name_data
            self.append_table(tname)
            table = self.get_nth_page(ti)
            table.set_data(tdata)

    def get_data(self):
        data = []
        tn = self.get_n_pages()
        for ti in range(tn):
            table = self.get_nth_page(ti)
            tname = self.get_tab_label_text(table)
            tdata = table.get_data()
            data.append([tname, tdata])
        return data

        #

    def get_current_table(self):
        page = self.get_current_page()
        if page == -1:
            return None

        table = self.get_nth_page(page)
        return table

    def edit_table_name(self, parent):
        page = self.get_current_page()
        if page == -1:
            return

        table = self.get_nth_page(page)
        name = self.get_tab_label_text(table)
        
        dialog = EditNameDialog("Edit Table Name: " + name, parent, name)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name = dialog.get_name()
            self.set_tab_label_text(table, name)

        dialog.destroy()

    def append_table(self, name):

        if name == None:
            name = "Table" + str(self.id)
        self.id += 1

        table = StateEventTable()

        self.append_page(table, Gtk.Label(name))
        self.set_tab_reorderable(table, True)

        self.changed = True
        self.show_all()

    def remove_table(self):
        page = self.get_current_page()
        if page == -1:
            return

        self.remove_page(page)

        self.changed = True
        self.show_all()

        #

    def on_page_reordered(self, notebook, child, page_num):
        self.changed = True

# end of file
