""" Create matrix file view for Speech Tasker. 

    Written by: Travis M. Moore
    Last edited: July 1, 2024
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
from tkinter import ttk

# Add custom path
try:
    sys.path.append(os.environ['TMPY'])
except KeyError:
    sys.path.append('C:\\Users\\MooTra\\Code\\Python')

# Custom
import tmpy
from tmpy.tkgui import widgets as w

##########
# Logger #
##########
# Create new logger
logger = logging.getLogger(__name__)

##############
# CreateView #
##############
class CreateView(tk.Toplevel):
    """ View for setting session parameters. """
    def __init__(self, parent, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        logger.info("Initializing CreateView")

        # Assign attributes
        self.parent = parent
        self.settings = settings
        self.list_length_var = tk.IntVar()

        # Window setup
        self.withdraw()
        self.resizable(False, False)
        self.grab_set()
        self._draw_widgets()

    def _draw_widgets(self):
        """ Populate the MainView with widgets. """
        logger.info("Drawing MainView widgets")
        ##########
        # Frames #
        ##########
        # Shared frame settings
        frame_options = {
            'padx': 10, 
            'pady': 10, 
            'ipadx': 5, 
            'ipady': 5,
            'sticky': 'nsew'
            }

        # Session info
        lfrm_session = ttk.Labelframe(self, text='Session Information')
        lfrm_session.grid(row=5, column=5, **frame_options)

        # Sentence options
        lfrm_sentence = ttk.Labelframe(self, text='Sentence Options')
        lfrm_sentence.grid(row=10, column=5, **frame_options)

        # Noise options
        lfrm_noise = ttk.Labelframe(self, text='Noise Options')
        lfrm_noise.grid(row=5, column=10, **frame_options)

        # AskPathGroup widgets
        lfrm_path = ttk.Labelframe(self, text="File Locations")
        lfrm_path.grid(row=10, column=10, **frame_options)
        # Audio file browser
        lfrm_audiopath = ttk.Labelframe(lfrm_path, text="Audio File Directory")
        lfrm_audiopath.grid(row=5, column=5, **frame_options)
        # Sentence file browser
        lfrm_sentencepath = ttk.Labelframe(lfrm_path, text="Sentence CSV File")
        lfrm_sentencepath.grid(row=10, column=5, **frame_options)

        ###################
        # Session Widgets #
        ###################
        # Subject
        w.LabelInput(
            lfrm_session,
            label="Subject",
            var=self.settings['Subject'],
            input_class=w.RequiredEntry,
            tool_tip="A unique subject identifier."
                + "\nCan be alpha, numeric, or both."
        ).grid(row=5, column=5, padx=5, pady=(5,0))

        # Condition
        w.LabelInput(
            lfrm_session,
            label="Condition",
            var=self.settings['Condition'],
            input_class=w.RequiredEntry,
            tool_tip="A unique condition name."
                + "\nCan be alpha, numeric, or both."
                + "\nSeparate words with underscores."
        ).grid(row=5, column=10, padx=5, pady=(5,0))

        ####################
        # Sentence Widgets #
        ####################
        # Lists
        w.LabelInput(
            lfrm_sentence,
            label="List(s)",
            var=self.settings['Sentence Lists'],
            input_class=w.BoundListEntry,
            input_args={
                'focus_update_var': self.list_length_var
            },
            tool_tip="The list numbers to include in the session." +
                "\nSeparate multiple values with a comma and space: 1, 2, 3"
        ).grid(row=5, column=5, padx=5, pady=(5,0))

        # Sentence level(s)
        w.LabelInput(
            lfrm_sentence,
            label="Level(s)",
            var=self.settings['Sentence Levels'],
            input_class=w.BoundListEntry,
            input_args={
                'max_var': self.list_length_var
            },
            tool_tip="Either a single level for all lists, or multiple " +
                "levels (must be one per list)." +
                "\nSeparate multiple values with a comma and space: 1, 2, 3"
        ).grid(row=5, column=10, padx=5, pady=(5,0))

        # Sentence speaker(s)
        w.LabelInput(
            lfrm_sentence,
            label="Speaker(s)",
            var=self.settings['Sentence Speakers'],
            input_class=w.BoundListEntry,
            input_args={
                'max_var': self.list_length_var
            },
            tool_tip="Either a single speaker for all lists, or a list " +
                "of multiple speakers (must be one per list)." +
                "\nSeparate multiple values with a comma and space: 1, 2, 3"
        ).grid(row=10, column=5, padx=5, pady=(5,0))

        # Number of sentences per list
        w.LabelInput(
            lfrm_sentence,
            label="Sentences per List",
            var=self.settings['Sentences per List'],
            input_class=w.RequiredEntry,
            tool_tip="The number of sentences to present from each list."
        ).grid(row=10, column=10, padx=5, pady=(5,0))

        # Presentations
        w.LabelInput(
            lfrm_sentence,
            label="Presentations",
            var=self.settings['Presentations'],
            input_class=w.RequiredEntry,
            tool_tip="Number of times to present all trials."
        ).grid(row=15, column=5, padx=5, pady=(5,0))

        # Randomize
        w.LabelInput(
            lfrm_sentence,
            label="Randomize",
            var=self.settings['Randomize'],
            input_class=ttk.Checkbutton,
            input_args={'takefocus': 0},
            tool_tip="Randomize trials in provided matrix file."
        ).grid(row=15, column=10, padx=5, pady=(5,0), sticky='n')

        #################
        # Noise Widgets #
        #################
        # Noise level
        w.LabelInput(
            lfrm_noise,
            label="Level",
            var=self.settings['Noise Level'],
            input_class=w.RequiredEntry,
            tool_tip="Level of the noise."
        ).grid(row=5, column=5, padx=5, pady=(5,0), sticky='n')

        #####################
        # File Path Widgets #
        #####################
        # Audio files directory
        w.AskPathGroup(
            parent=lfrm_audiopath,
            var=self.settings['import_audio_path'],
            title_args={'text': 'Audio Files'},
            type='dir',
            tool_tip="Path to folder with audio files."
        ).grid(row=5, column=5)

        # Matrix file path
        w.AskPathGroup(
            parent=lfrm_sentencepath,
            var=self.settings['sentence_file_path'],
            title_args={'text': 'Sentence File'},
            type='file',
            tool_tip="Path to CSV file containing sentences."
        ).grid(row=10, column=5)

        #################
        # Submit button #
        #################
        btn_submit = ttk.Button(self, text="Submit", command=self._on_submit)
        btn_submit.grid(row=30, column=5, columnspan=20, pady=(0, 10))

        # Center CreateView over root
        tmpy.functions.tkgui_funcs.center_window_over_parent(self)

    ###########
    # Methods #
    ###########
    def _on_submit(self):
        """ Send submit event to controller and close window. """
        logger.info("SUBMIT button pressed.")
        # Validate form
        errors = tmpy.functions.tkgui_funcs.get_errors(self.settings)
        if errors:
            messagebox.showerror(
                title="Invalid Entry",
                message="Unable to save form!",
                detail="Error in fields:\n{}"
                .format('\n'.join(errors.keys()))
            )
            return
        logger.info("Sending 'SUBMIT' event to %s", self.parent.REF)
        self.parent.event_generate('<<CreateViewSubmit>>')
        logger.info("Destroying CreateView instance")
        self.destroy()

################
# Module Guard #
################
if __name__ == "__main__":
    pass
