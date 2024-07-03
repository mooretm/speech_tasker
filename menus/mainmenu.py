""" Main menu for automated HINT.  

    Written by: Travis M. Moore
    Last edited: May 14, 2024
"""

###########
# Imports #
###########
# Standard library
import logging
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Add custom path
try:
    sys.path.append(os.environ['TMPY'])
except KeyError:
    sys.path.append('C:\\Users\\MooTra\\Code\\Python')

# Custom
from tmpy.tkgui.shared_assets import images

###########
# Logging #
###########
# Create new logger
logger = logging.getLogger(__name__)

############
# MainMenu #
############
class MainMenu(tk.Menu):
    """ Main Menu. """
    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback


    def _bind_accelerators(self):
        """ Bind shortcut keys to event triggers. """
        logger.info("Binding menu accelerators")
        self.bind_all('<Control-q>', self._event('<<FileQuit>>'))


    def _create_icons(self):
        """ Create a dictionary of icons. Necessary because
            PhotoImage objects cannot be created until an 
            instance of Tk has been created.
        """
        logger.info("Importing icons")
        self.icons = {
            # File menu
            'file_settings': tk.PhotoImage(file=images.SETTINGS_ICON),
            'file_start': tk.PhotoImage(file=images.PLAY_ICON),
            'file_upload': tk.PhotoImage(file=images.UPLOAD_ICON),
            'file_new': tk.PhotoImage(file=images.HELP_ICON),

            # Tools menu
            'tools_audio': tk.PhotoImage(file=images.AUDIO_ICON),
            'tools_calibration': tk.PhotoImage(file=images.CALIBRATION_ICON),

            # Help menu
            'help_about': tk.PhotoImage(file=images.ABOUT_ICON),
            'help_help': tk.PhotoImage(file=images.HELP_ICON),
            'help_changelog': tk.PhotoImage(file=images.CHANGELOG_ICON)
        }


    def __init__(self, parent, _app_info, **kwargs):
        super().__init__(parent, **kwargs)
        logger.info("Initializing MainMenu")

        # Assign variables
        self._app_info = _app_info

        # Create icons
        self._create_icons()

        #############
        # File Menu #
        #############
        logger.info("Creating 'File' menu")
        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(
            label="Import Matrix File...",
            command=self._event('<<FileImportMatrixFile>>'),
            image=self.icons['file_upload'],
            compound=tk.LEFT
        )
        self.file_menu.add_command(
            label="Create Matrix File...",
            command=self._event('<<FileCreateMatrixFile>>'),
            image=self.icons['file_settings'],
            compound=tk.LEFT
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Start",
            command=self._event('<<FileStart>>'),
            image=self.icons['file_start'],
            compound=tk.LEFT
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>'),
            accelerator='Ctrl+Q',
        )
        self.add_cascade(label='File', menu=self.file_menu)

        ############## 
        # Tools menu #
        ##############
        logger.info("Creating 'Tools' menu")
        tools_menu = tk.Menu(self, tearoff=False)
        tools_menu.add_command(
            label='Audio Settings...',
            command=self._event('<<ToolsAudioSettings>>'),
            image=self.icons['tools_audio'],
            compound=tk.LEFT,
        )
        tools_menu.add_command(
            label='Calibration...',
            command=self._event('<<ToolsCalibration>>'),
            image=self.icons['tools_calibration'],
            compound=tk.LEFT,
        )
        # Add Tools menu to the menubar
        self.add_cascade(label="Tools", menu=tools_menu)

        #############
        # Help Menu #
        #############
        logger.info("Creating 'Help' menu")
        self.help_menu = tk.Menu(self, tearoff=False)
        self.help_menu.add_command(
            label='About...',
            command=self.show_about,
            image=self.icons['help_about'],
            compound=tk.LEFT,
        )
        self.help_menu.add_command(
            label='README...',
            command=self._event('<<HelpREADME>>'),
            image=self.icons['help_help'],
            compound=tk.LEFT,
        )
        self.help_menu.add_command(
            label="CHANGELOG...",
            command=self._event('<<HelpCHANGELOG>>'),
            image=self.icons['help_changelog'],
            compound=tk.LEFT,
        )
        # Add help menu to the menubar
        self.add_cascade(label="Help", menu=self.help_menu)

        #####################
        # Bind accelerators #
        #####################
        self._bind_accelerators()

    ##################
    # Menu Functions #
    ##################
    # HELP menu
    def show_about(self):
        """ Show the 'About' dialog. """
        logger.info("Loading 'About' window")
        about_message = self._app_info['name']
        about_detail = (
            'Written by: Travis M. Moore\n' +
            'Version: {}\n'.format(self._app_info['version']) +
            'Created: December 07, 2022\n'
            'Last edited: {}'.format(self._app_info['last_edited'])
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )
