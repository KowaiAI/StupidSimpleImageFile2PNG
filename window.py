"""Main application window with GTK4/Libadwaita UI."""

import threading
from pathlib import Path

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

from converter import batch_convert, SUPPORTED_FORMATS


class MainWindow(Adw.ApplicationWindow):
    """Main window for the Bulk Image Converter application."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_files: list[Path] = []
        self.output_folder: Path = Path.home() / "Pictures" / "converted"
        self.is_converting = False

        self.set_title("Bulk Image Converter")
        self.set_default_size(500, 600)

        self._build_ui()

    def _build_ui(self):
        """Build the user interface."""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(main_box)

        # Header bar
        header = Adw.HeaderBar()
        main_box.append(header)

        # Content with clamp for proper width
        clamp = Adw.Clamp()
        clamp.set_maximum_size(600)
        clamp.set_margin_start(12)
        clamp.set_margin_end(12)
        clamp.set_margin_top(12)
        clamp.set_margin_bottom(12)
        main_box.append(clamp)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        clamp.set_child(content_box)

        # Select Images section
        select_group = Adw.PreferencesGroup()
        select_group.set_title("Input")
        content_box.append(select_group)

        # Select images button row
        select_row = Adw.ActionRow()
        select_row.set_title("Select Images")
        select_row.set_subtitle("0 files selected")
        self.select_subtitle = select_row

        select_button = Gtk.Button(label="Browse")
        select_button.set_valign(Gtk.Align.CENTER)
        select_button.add_css_class("suggested-action")
        select_button.connect("clicked", self._on_select_images)
        select_row.add_suffix(select_button)
        select_row.set_activatable_widget(select_button)
        select_group.add(select_row)

        # File list
        list_frame = Gtk.Frame()
        list_frame.set_margin_top(6)
        content_box.append(list_frame)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(200)
        scrolled.set_max_content_height(250)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        list_frame.set_child(scrolled)

        self.file_listbox = Gtk.ListBox()
        self.file_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.file_listbox.add_css_class("boxed-list")
        scrolled.set_child(self.file_listbox)

        # Placeholder when no files
        self.placeholder = Gtk.Label(label="No images selected")
        self.placeholder.add_css_class("dim-label")
        self.placeholder.set_margin_top(40)
        self.placeholder.set_margin_bottom(40)
        self.file_listbox.set_placeholder(self.placeholder)

        # Output section
        output_group = Adw.PreferencesGroup()
        output_group.set_title("Output")
        content_box.append(output_group)

        # Output folder row
        output_row = Adw.ActionRow()
        output_row.set_title("Output Folder")
        output_row.set_subtitle(str(self.output_folder))
        self.output_row = output_row

        output_button = Gtk.Button(icon_name="folder-open-symbolic")
        output_button.set_valign(Gtk.Align.CENTER)
        output_button.connect("clicked", self._on_select_output)
        output_row.add_suffix(output_button)
        output_row.set_activatable_widget(output_button)
        output_group.add(output_row)

        # Progress section
        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        progress_box.set_margin_top(12)
        content_box.append(progress_box)

        self.progress_label = Gtk.Label(label="Ready")
        self.progress_label.set_halign(Gtk.Align.START)
        self.progress_label.add_css_class("dim-label")
        progress_box.append(self.progress_label)

        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(False)
        progress_box.append(self.progress_bar)

        # Convert button
        self.convert_button = Gtk.Button(label="Convert to PNG")
        self.convert_button.add_css_class("suggested-action")
        self.convert_button.add_css_class("pill")
        self.convert_button.set_halign(Gtk.Align.CENTER)
        self.convert_button.set_margin_top(18)
        self.convert_button.set_sensitive(False)
        self.convert_button.connect("clicked", self._on_convert)
        content_box.append(self.convert_button)

    def _on_select_images(self, button):
        """Handle image selection button click."""
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Images")

        # Create file filter for images
        filter_images = Gtk.FileFilter()
        filter_images.set_name("Images")
        for fmt in SUPPORTED_FORMATS:
            filter_images.add_suffix(fmt.lstrip('.'))
            filter_images.add_suffix(fmt.lstrip('.').upper())

        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_images)
        dialog.set_filters(filters)
        dialog.set_default_filter(filter_images)

        dialog.open_multiple(self, None, self._on_images_selected)

    def _on_images_selected(self, dialog, result):
        """Handle image selection result."""
        try:
            files = dialog.open_multiple_finish(result)
            if files:
                self.selected_files = [Path(f.get_path()) for f in files]
                self._update_file_list()
        except GLib.Error:
            # User cancelled
            pass

    def _update_file_list(self):
        """Update the file list display."""
        # Clear existing items
        while True:
            row = self.file_listbox.get_row_at_index(0)
            if row is None:
                break
            self.file_listbox.remove(row)

        # Add new items
        for file_path in self.selected_files:
            row = Adw.ActionRow()
            row.set_title(file_path.name)
            row.set_subtitle(file_path.suffix.upper().lstrip('.'))

            # Remove button
            remove_btn = Gtk.Button(icon_name="user-trash-symbolic")
            remove_btn.set_valign(Gtk.Align.CENTER)
            remove_btn.add_css_class("flat")
            remove_btn.connect("clicked", self._on_remove_file, file_path)
            row.add_suffix(remove_btn)

            self.file_listbox.append(row)

        # Update subtitle
        count = len(self.selected_files)
        self.select_subtitle.set_subtitle(f"{count} file{'s' if count != 1 else ''} selected")

        # Update convert button state
        self.convert_button.set_sensitive(count > 0 and not self.is_converting)

    def _on_remove_file(self, button, file_path):
        """Remove a file from the selection."""
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            self._update_file_list()

    def _on_select_output(self, button):
        """Handle output folder selection."""
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Output Folder")

        # Set initial folder
        if self.output_folder.exists():
            dialog.set_initial_folder(Gio.File.new_for_path(str(self.output_folder)))

        dialog.select_folder(self, None, self._on_output_selected)

    def _on_output_selected(self, dialog, result):
        """Handle output folder selection result."""
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                self.output_folder = Path(folder.get_path())
                self.output_row.set_subtitle(str(self.output_folder))
        except GLib.Error:
            # User cancelled
            pass

    def _on_convert(self, button):
        """Start the conversion process."""
        if not self.selected_files or self.is_converting:
            return

        self.is_converting = True
        self.convert_button.set_sensitive(False)
        self.progress_bar.set_fraction(0)
        self.progress_label.set_text("Starting conversion...")

        # Run conversion in background thread
        thread = threading.Thread(
            target=self._convert_thread,
            args=(self.selected_files.copy(), self.output_folder),
            daemon=True
        )
        thread.start()

    def _convert_thread(self, files, output_folder):
        """Background thread for conversion."""
        def progress_callback(current, total, filename):
            GLib.idle_add(self._update_progress, current, total, filename)

        successful, failed = batch_convert(files, output_folder, progress_callback)

        GLib.idle_add(self._conversion_complete, successful, failed)

    def _update_progress(self, current, total, filename):
        """Update progress bar from main thread."""
        if total > 0:
            fraction = current / total
            self.progress_bar.set_fraction(fraction)
            percent = int(fraction * 100)
            self.progress_label.set_text(f"Converting: {filename} ({percent}%)")
        return False  # Remove idle callback

    def _conversion_complete(self, successful, failed):
        """Handle conversion completion."""
        self.is_converting = False
        self.convert_button.set_sensitive(len(self.selected_files) > 0)
        self.progress_bar.set_fraction(1.0)

        # Show result message
        success_count = len(successful)
        fail_count = len(failed)

        if fail_count == 0:
            self.progress_label.set_text(f"Complete! {success_count} images converted.")
            self._show_success_dialog(success_count)
        else:
            self.progress_label.set_text(f"Done: {success_count} converted, {fail_count} failed.")
            self._show_result_dialog(successful, failed)

        return False

    def _show_success_dialog(self, count):
        """Show success dialog."""
        dialog = Adw.AlertDialog()
        dialog.set_heading("Conversion Complete")
        dialog.set_body(f"Successfully converted {count} image{'s' if count != 1 else ''} to PNG.\n\nOutput folder: {self.output_folder}")
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.choose(self, None, None)

    def _show_result_dialog(self, successful, failed):
        """Show result dialog with failures."""
        dialog = Adw.AlertDialog()
        dialog.set_heading("Conversion Complete")

        body = f"Converted: {len(successful)}\nFailed: {len(failed)}\n\n"
        if failed:
            body += "Failed files:\n"
            for path, error in failed[:5]:  # Show first 5 failures
                body += f"• {path.name}: {error}\n"
            if len(failed) > 5:
                body += f"...and {len(failed) - 5} more"

        dialog.set_body(body)
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.choose(self, None, None)
