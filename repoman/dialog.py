#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)
   Copyright 2017 Ian Santopietro (ian@system76.com)

   This file is part of Repoman.

    Repoman is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Repoman is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Repoman.  If not, see <http://www.gnu.org/licenses/>.
'''

import logging
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext

FLATPAK_SUPPORT = False
try:
    import pyflatpak as Flatpak
    FLATPAK_SUPPORT = True
except ImportError:
    FLATPAK_SUPPORT = False
    pass

from .repo import Repo

gettext.bindtextdomain('repoman', '/usr/share/repoman/po')
gettext.textdomain("repoman")
_ = gettext.gettext

class ErrorDialog(Gtk.Dialog):

    def __init__(self, parent, dialog_title, dialog_icon,
                 message_title, message_text):
        Gtk.Dialog.__init__(self, dialog_title, parent, 0, "hg",
                            (Gtk.STOCK_CLOSE, Gtk.ResponseType.OK),
                            modal=1)

        self.log = logging.getLogger("repoman.ErrorDialog")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.WARNING)

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(24)
        content_grid.set_margin_right(24)
        content_grid.set_margin_bottom(24)
        content_grid.set_column_spacing(36)
        content_grid.set_row_spacing(12)
        content_area.add(content_grid)

        error_image = Gtk.Image.new_from_icon_name(dialog_icon,
                                                   Gtk.IconSize.DIALOG)
        content_grid.attach(error_image, 0, 0, 1, 2)

        dialog_label = Gtk.Label(message_title)
        dialog_message = Gtk.Label(message_text)
        content_grid.attach(dialog_label, 1, 0, 1, 1)
        content_grid.attach(dialog_message, 1, 1, 1, 1)

        self.show_all()


class DeleteDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self, parent):

        settings = Gtk.Settings.get_default()

        header = settings.props.gtk_dialogs_use_header

        Gtk.Dialog.__init__(self, _("Remove Source"), parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_REMOVE, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=header)

        self.log = logging.getLogger("repoman.DeleteDialog")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.WARNING)

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(24)
        content_grid.set_margin_right(24)
        content_grid.set_margin_bottom(24)
        content_grid.set_column_spacing(12)
        content_grid.set_row_spacing(6)
        content_area.add(content_grid)

        delete_image = Gtk.Image.new_from_icon_name("dialog-warning-symbolic",
                                                Gtk.IconSize.DIALOG)
        delete_image.props.valign = Gtk.Align.START
        content_grid.attach(delete_image, 0, 0, 1, 2)

        delete_label = Gtk.Label(_("Are you sure you want to remove this source?"))
        Gtk.StyleContext.add_class(delete_label.get_style_context(), "h2")
        content_grid.attach(delete_label, 1, 0, 1, 1)

        delete_explain = Gtk.Label(_("If you remove this source, you will need to add it again to continue using it. Any software you've installed from this source will remain installed."))
        delete_explain.props.wrap = True
        delete_explain.set_max_width_chars(50)
        delete_explain.set_xalign(0)
        content_grid.attach(delete_explain, 1, 1, 1, 1)

        Gtk.StyleContext.add_class(self.get_widget_for_response(Gtk.ResponseType.OK).get_style_context(),
                                   "destructive-action")

        self.show_all()

class FpDeleteDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self, parent):

        settings = Gtk.Settings.get_default()

        header = settings.props.gtk_dialogs_use_header

        Gtk.Dialog.__init__(self, _("Remove Source"), parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_REMOVE, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=header)

        self.log = logging.getLogger("repoman.DeleteDialog")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.WARNING)

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(24)
        content_grid.set_margin_right(24)
        content_grid.set_margin_bottom(24)
        content_grid.set_column_spacing(12)
        content_grid.set_row_spacing(6)
        content_area.add(content_grid)

        delete_image = Gtk.Image.new_from_icon_name("dialog-warning-symbolic",
                                                Gtk.IconSize.DIALOG)
        delete_image.props.valign = Gtk.Align.START
        content_grid.attach(delete_image, 0, 0, 1, 2)

        delete_label = Gtk.Label(_("Are you sure you want to remove this source?"))
        Gtk.StyleContext.add_class(delete_label.get_style_context(), "h2")
        content_grid.attach(delete_label, 1, 0, 1, 1)

        delete_explain = Gtk.Label(_(
            "If you remove this source, you will need to add it again to "
            "continue using it. All software you've installed from this source "
            "will be removed."
        ))
        delete_explain.props.wrap = True
        delete_explain.set_max_width_chars(50)
        delete_explain.set_xalign(0)
        content_grid.attach(delete_explain, 1, 1, 1, 1)

        Gtk.StyleContext.add_class(self.get_widget_for_response(Gtk.ResponseType.OK).get_style_context(),
                                   "destructive-action")

        self.show_all()

class AddDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self, parent):

        settings = Gtk.Settings.get_default()
        header = settings.props.gtk_dialogs_use_header

        Gtk.Dialog.__init__(self, _("Add Source"), parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_ADD, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=header)

        self.log = logging.getLogger("repoman.AddDialog")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.WARNING)
        self.repo = Repo()

        content_area = self.get_content_area()

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(36)
        content_grid.set_margin_right(36)
        content_grid.set_margin_bottom(24)
        content_grid.set_column_spacing(12)
        content_grid.set_row_spacing(12)
        content_grid.set_halign(Gtk.Align.CENTER)
        content_area.add(content_grid)

        add_label = Gtk.Label(_('Enter a repository line:'))
        content_grid.attach(add_label, 0, 1, 2, 1)

        self.ppa_entry = Gtk.Entry()
        self.ppa_entry.set_placeholder_text(_('ppa:system76/pop'))
        self.ppa_entry.set_halign(Gtk.Align.CENTER)
        self.ppa_entry.set_activates_default(True)
        self.ppa_entry.set_width_chars(50)
        self.ppa_entry.connect(_("changed"), self.on_bottom_entry_changed)
        content_grid.attach(self.ppa_entry, 0, 2, 2, 1)

        full_label = Gtk.Label(_('Or, enter repository details below:'))
        full_label.set_margin_top(36)
        content_grid.attach(full_label, 0, 3, 2, 1)

        name_label = Gtk.Label(_("Name:"))
        name_label.set_halign(Gtk.Align.END)
        uri_label = Gtk.Label(_("URI:"))
        uri_label.set_halign(Gtk.Align.END)
        version_label = Gtk.Label(_("Version:"))
        version_label.set_halign(Gtk.Align.END)
        component_label = Gtk.Label(_("Component:"))
        component_label.set_halign(Gtk.Align.END)
        content_grid.attach(name_label, 0, 4, 1, 1)
        content_grid.attach(uri_label, 0, 5, 1, 1)
        content_grid.attach(version_label, 0, 6, 1, 1)
        content_grid.attach(component_label, 0, 7, 1, 1)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text('PPA...')
        self.name_entry.set_activates_default(False)
        self.name_entry.set_width_chars(40)
        self.name_entry.connect(_("changed"), self.on_top_entry_changed)
        content_grid.attach(self.name_entry, 1, 4, 1, 1)

        self.source_check = Gtk.CheckButton(_('Include Source Code'))
        self.source_check.set_active(False)
        self.source_check.set_halign(Gtk.Align.CENTER)
        content_grid.attach(self.source_check, 0, 8, 2, 1)

        self.uri_entry = Gtk.Entry()
        self.uri_entry.set_placeholder_text("https://ppa.launchpad.net/...")
        self.uri_entry.set_activates_default(False)
        self.uri_entry.set_width_chars(40)
        self.uri_entry.connect(_("changed"), self.on_top_entry_changed)
        content_grid.attach(self.uri_entry, 1, 5, 1, 1)

        self.version_entry = Gtk.Entry()
        self.version_entry.set_placeholder_text(self.repo.get_codename())
        self.version_entry.set_activates_default(False)
        self.version_entry.connect(_("changed"), self.on_top_entry_changed)
        content_grid.attach(self.version_entry, 1, 6, 1, 1)

        self.component_entry = Gtk.Entry()
        self.component_entry.set_placeholder_text("main")
        self.component_entry.set_activates_default(False)
        self.component_entry.connect(_("changed"), self.on_top_entry_changed)
        content_grid.attach(self.component_entry, 1, 7, 1, 1)

        self.add_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        self.add_button.set_sensitive(False)

        Gtk.StyleContext.add_class(self.add_button.get_style_context(),
                                   "suggested-action")
        self.add_button.grab_default()

        self.show_all()

    def on_top_entry_changed(self, widget):
        all_text = self.name_entry.get_text()
        all_text += self.uri_entry.get_text()
        all_text += self.version_entry.get_text()
        all_text += self.component_entry.get_text()

        if all_text == '' or all_text == None:
            self.name_entry.set_sensitive(True)
            self.uri_entry.set_sensitive(True)
            self.version_entry.set_sensitive(True)
            self.component_entry.set_sensitive(True)
            self.source_check.set_sensitive(True)
            self.ppa_entry.set_sensitive(True)
            self.add_button.set_sensitive(False)
        else:
            self.name_entry.set_sensitive(True)
            self.uri_entry.set_sensitive(True)
            self.version_entry.set_sensitive(True)
            self.component_entry.set_sensitive(True)
            self.source_check.set_sensitive(True)
            self.add_button.set_sensitive(True)
            self.ppa_entry.set_sensitive(False)
    
    def on_bottom_entry_changed(self, widget):
        ppa_line = widget.get_text()
        if ppa_line == '' or ppa_line == None:
            self.name_entry.set_sensitive(True)
            self.uri_entry.set_sensitive(True)
            self.version_entry.set_sensitive(True)
            self.component_entry.set_sensitive(True)
            self.source_check.set_sensitive(True)
            self.ppa_entry.set_sensitive(True)
            self.add_button.set_sensitive(False)
        else:
            self.name_entry.set_sensitive(False)
            self.uri_entry.set_sensitive(False)
            self.version_entry.set_sensitive(False)
            self.component_entry.set_sensitive(False)
            self.source_check.set_sensitive(False)
            self.ppa_entry.set_sensitive(True)

            if ppa_line.startswith('deb'):
                self.add_button.set_sensitive(True)
            elif ppa_line.startswith('ppa:'):
                if '/' in ppa_line:
                    self.add_button.set_sensitive(True)
                else: 
                    self.add_button.set_sensitive(False)
            else:
                self.add_button.set_sensitive(False)

class FpAddDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self, parent):

        settings = Gtk.Settings.get_default()
        header = settings.props.gtk_dialogs_use_header

        Gtk.Dialog.__init__(self, _("Add Source"), parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_ADD, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=header)

        self.log = logging.getLogger("repoman.FpAddDialog")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.WARNING)

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(12)
        content_grid.set_margin_right(12)
        content_grid.set_margin_bottom(12)
        content_grid.set_row_spacing(6)
        content_grid.set_halign(Gtk.Align.CENTER)
        content_grid.set_hexpand(True)
        content_area.add(content_grid)

        add_title = Gtk.Label(_("Add Flatpak Source"))
        Gtk.StyleContext.add_class(add_title.get_style_context(), "h2")
        content_grid.attach(add_title, 0, 0, 1, 1)

        self.fp_name_entry = Gtk.Entry()
        self.fp_name_entry.set_placeholder_text(_('Source Name e.g. "flathub"'))
        self.fp_name_entry.set_width_chars(50)
        self.fp_name_entry.set_margin_top(12)
        content_grid.attach(self.fp_name_entry, 0, 2, 1, 1)

        self.fp_entry = Gtk.Entry()
        self.fp_entry.set_placeholder_text(_("Source URL"))
        self.fp_entry.connect(_("changed"), self.on_entry_changed)
        self.fp_entry.set_width_chars(50)
        self.fp_entry.set_margin_top(12)
        content_grid.attach(self.fp_entry, 0, 3, 1, 1)

        self.add_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        self.add_button.set_sensitive(False)

        Gtk.StyleContext.add_class(self.add_button.get_style_context(),
                                   "suggested-action")
        self.add_button.grab_default()

        self.show_all()
    
    def on_entry_changed(self, widget):
        entry_text = widget.get_text()
        entry_valid = entry_text.endswith(".flatpakrepo")
        try:
            self.add_button.set_sensitive(entry_valid)
        except TypeError:
            pass

class EditDialog(Gtk.Dialog):

    ppa_name = False

    def __init__(self,
                 parent,
                 repo_filename):

        settings = Gtk.Settings.get_default()
        header = settings.props.gtk_dialogs_use_header

        Gtk.Dialog.__init__(self, _("Modify Source"), parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_SAVE, Gtk.ResponseType.OK),
                             modal=1, use_header_bar=header)

        self.log = logging.getLogger("repoman.EditDialog")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.WARNING)

        self.repo = Repo()
        self.source = self.repo.get_source(repo_filename)
        self.parent = parent

        self.props.resizable = False

        content_area = self.get_content_area()

        content_grid = Gtk.Grid()
        content_grid.set_margin_top(24)
        content_grid.set_margin_left(24)
        content_grid.set_margin_right(24)
        content_grid.set_margin_bottom(24)
        content_grid.set_column_spacing(12)
        content_grid.set_row_spacing(12)
        content_grid.set_halign(Gtk.Align.CENTER)
        content_area.add(content_grid)

        name_label = Gtk.Label(_("Name:"))
        name_label.set_halign(Gtk.Align.END)
        uri_label = Gtk.Label(_("URI:"))
        uri_label.set_halign(Gtk.Align.END)
        version_label = Gtk.Label(_("Version:"))
        version_label.set_halign(Gtk.Align.END)
        component_label = Gtk.Label(_("Component:"))
        component_label.set_halign(Gtk.Align.END)
        content_grid.attach(name_label, 0, 1, 1, 1)
        content_grid.attach(uri_label, 0, 2, 1, 1)
        content_grid.attach(version_label, 0, 3, 1, 1)
        content_grid.attach(component_label, 0, 4, 1, 1)

        enabled_grid = Gtk.Grid()
        enabled_grid.set_column_spacing(12)
        enabled_grid.set_halign(Gtk.Align.CENTER)

        enabled_label = Gtk.Label(_('Enabled'))
        enabled_label.set_halign(Gtk.Align.END)
        enabled_grid.attach(enabled_label, 0, 0, 1, 1)

        self.enabled_switch = Gtk.Switch()
        self.enabled_switch.set_active(self.source.enabled.get_bool())
        self.enabled_switch.set_halign(Gtk.Align.END)
        enabled_grid.attach(self.enabled_switch, 1, 0, 1, 1)
        content_grid.attach(enabled_grid, 0, 0, 2, 1)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("PPA...")
        self.name_entry.set_text(self.source.name)
        self.name_entry.set_activates_default(False)
        self.name_entry.set_width_chars(40)
        content_grid.attach(self.name_entry, 1, 1, 1, 1)

        self.uri_entry = Gtk.Entry()
        self.uri_entry.set_placeholder_text("https://ppa.launchpad.net/...")
        self.uri_entry.set_text(' '.join(self.source.uris))
        self.uri_entry.set_activates_default(False)
        content_grid.attach(self.uri_entry, 1, 2, 1, 1)

        self.version_entry = Gtk.Entry()
        self.version_entry.set_placeholder_text(self.repo.get_codename())
        self.version_entry.set_text(' '.join(self.source.suites))
        self.version_entry.set_activates_default(False)
        content_grid.attach(self.version_entry, 1, 3, 1, 1)

        self.component_entry = Gtk.Entry()
        self.component_entry.set_placeholder_text("main")
        self.component_entry.set_text(' '.join(self.source.components))
        self.component_entry.set_activates_default(False)
        content_grid.attach(self.component_entry, 1, 4, 1, 1)

        self.source_check = Gtk.CheckButton(_('Include Source Code'))
        self.source_check.set_halign(Gtk.Align.CENTER)
        source_enabled = False
        for type in self.source.types:
            if type.value == "deb-src":
                source_enabled = True
        self.source_check.set_active(source_enabled)
        content_grid.attach(self.source_check, 0, 5, 2, 1)


        remove_button = Gtk.Button.new_with_label(_("Remove Source"))
        Gtk.StyleContext.add_class(remove_button.get_style_context(),
                                   "destructive-action")
        remove_button.connect("clicked", self.on_remove_button_clicked)
        #content_grid.attach(remove_button, 0, 5, 1, 1)

        save_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        cancel_button = self.get_widget_for_response(Gtk.ResponseType.CANCEL)

        Gtk.StyleContext.add_class(save_button.get_style_context(),
                                   "suggested-action")

        action_area = self.get_action_area()
        action_area.add(remove_button)
        separator = Gtk.Box()
        separator.set_hexpand(True)
        action_area.add(separator)
        separator.show()
        separator2 = Gtk.Box()
        separator2.set_hexpand(True)
        action_area.add(separator2)
        separator2.show()
        action_area.props.layout_style = Gtk.ButtonBoxStyle.START

        self.show_all()

        if header == False:
            action_area.remove(save_button)
            action_area.remove(cancel_button)
            action_area.add(cancel_button)
            action_area.add(save_button)

    def on_remove_button_clicked(self, widget):
        self.log.debug("Remove Clicked")
        dialog = DeleteDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.repo.remove_source(self.source.filename)
            dialog.destroy()
            self.destroy()
        else:
            dialog.destroy()




