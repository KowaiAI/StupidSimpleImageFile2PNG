#!/usr/bin/env python3
"""Bulk Image Converter - Convert images to PNG with metadata stripping."""

import sys

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio

from window import MainWindow


class BulkImageConverterApp(Adw.Application):
    """Main application class."""

    def __init__(self):
        super().__init__(
            application_id="io.github.bulkimageconverter",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )

    def do_activate(self):
        """Handle application activation."""
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()


def main():
    """Application entry point."""
    app = BulkImageConverterApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
