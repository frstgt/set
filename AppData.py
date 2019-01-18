# -*- coding: utf-8 -*-

import sys, io

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango

import json
# import re # sometimes useful

import AppDef

class AppData:

  def __init__(self, tables):
      self.tables = tables

  def get_changed(self):
      return self.tables.get_changed()
  def clear_changed(self):
      self.tables.clear_changed()

  def clear_data(self):
      tn = self.tables.get_numof_tables()
      for ti in range(tn):
          self.tables.remove_nth_table(ti)

  def load_data(self, filename):
      f = io.open(filename, 'r', encoding='utf-8')
      first_line = f.readline().rstrip()
      if first_line != AppDef.FILE_HEADER:
          return
      data = json.load(f)
      f.close

      self.copy_data_to_tables(data, self.tables)

  def save_data(self, filename):
      data = self.copy_data_from_tables(self.tables);

      f = io.open(filename, 'w', encoding='utf-8')
      f.write(AppDef.FILE_HEADER + "\n")

      # json.dumps return utf-8 as str. it is a bug.
      dump_utf8 = unicode(json.dumps(data, encoding='utf-8'))
      f.write(dump_utf8)

      f.close

      #

  def copy_data_to_tables(self, data, tables):

      for ti, t_name_data in enumerate(data):

          tname, tdata = t_name_data
          sd, ed, trd = tdata

          tables.append_table(tname)
          table = tables.get_nth_table(ti)

          for sname, scode in sd:
              table.append_state(sname, scode)

          for ename, ecode in ed:
              table.append_event(ename, ecode)

          for si, ei, tsi in trd:
              table.set_tr(si, ei, tsi)

  def copy_data_from_tables(self, tables):

      data = []
      tn = tables.get_numof_tables()
      for ti in range(tn):

          table = tables.get_nth_table(ti)
          tname = tables.get_table_name(table)

          sd = []
          sn = table.get_numof_states()
          for si in range(sn):
              sname, scode = table.get_nth_state(si)
              sd.append([sname, scode])

          ed = []
          en = table.get_numof_events()
          for ei in range(en):
              ename, ecode = table.get_nth_event(ei)
              ed.append([ename, ecode])

          trd = []
          for si in range(sn):
              for ei in range(en):
                  tsi = table.get_tr(si, ei)
                  trd.append([si, ei, tsi])

          tdata = [sd, ed, trd]
          data.append([tname, tdata])

      return data

# end of file
