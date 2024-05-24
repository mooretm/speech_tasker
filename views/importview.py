""" Import matrix file view for Speech Tasker. 

    Written by: Travis M. Moore
    Last edited: May 22, 2024
"""

###########
# Imports #
###########
# Standard library
import logging
import os
import sys
import tkinter as tk
from idlelib.tooltip import Hovertip
from tkinter import filedialog
from tkinter import ttk

# Custom
sys.path.append(os.environ['TMPY'])
import tmpy

##########
# Logger #
##########
# Create new logger
logger = logging.getLogger(__name__)

##############
# ImportView #
##############
class ImportView(tk.Toplevel):
    """ View for setting session parameters. """
    def __init__(self, parent, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        logger.debug("Initializing ImportView")

        # Assign attributes
        self.parent = parent
        self.settings = settings
        
        # Window setup
        self.withdraw()
        self.resizable(False, False)
        self.grab_set()
        self._draw_widgets()


    def _draw_widgets(self):
        """ Populate the MainView with widgets. """
        logger.debug("Drawing MainView widgets")
        ##########
        # Frames #
        ##########
        # Tooltip delay (ms)
        tt_delay = 1000

        # Shared frame settings
        frame_options = {
            'padx': 10, 
            'pady': 10, 
            'ipadx': 5, 
            'ipady': 5,
            'sticky': 'nsew'
            }
        widget_options = {'padx': 5, 'pady': (10, 0)}

        # Session info
        lfrm_session = ttk.Labelframe(self, text='Session Information')
        lfrm_session.grid(row=5, column=5, **frame_options)

        # Sentence options
        lfrm_stimulus = ttk.Labelframe(self, text='Sentence Options')
        lfrm_stimulus.grid(row=10, column=5, **frame_options)

        # Noise options
        lfrm_noise = ttk.Labelframe(self, text='Noise Options')
        lfrm_noise.grid(row=15, column=5, **frame_options)

        # Audio file browser
        lfrm_audiopath = ttk.Labelframe(self, text="Audio File Directory")
        lfrm_audiopath.grid(
            row=20, 
            column=5, 
            **frame_options, 
            )

        # Matrix file browser
        lfrm_matrixpath = ttk.Labelframe(self, text='Matrix File Path')
        lfrm_matrixpath.grid(
            row=25, 
            column=5, 
            **frame_options, 
            )

        ###################
        # Session Widgets #
        ###################
        # Subject
        lbl_sub = ttk.Label(lfrm_session, text="Subject:")
        lbl_sub.grid(row=5, column=5, sticky='e', **widget_options)
        sub_tt = Hovertip(
            anchor_widget=lbl_sub,
            text="A unique subject identifier."+
                "\nCan be alpha, numeric, or both.",
            hover_delay=tt_delay
            )
        ttk.Entry(lfrm_session, 
            textvariable=self.settings['subject']
            ).grid(row=5, column=10, sticky='w', **widget_options)


        # Condition
        lbl_condition = ttk.Label(lfrm_session, text="Condition:")
        lbl_condition.grid(row=10, column=5, sticky='e', **widget_options)
        condition_tt = Hovertip(
            anchor_widget=lbl_condition,
            text="A unique condition name.\nCan be alpha, numeric, or both." +
                "\nSeparate words with underscores.",
            hover_delay=tt_delay
            )
        ttk.Entry(
            lfrm_session, 
            textvariable=self.settings['condition']
            ).grid(row=10, column=10, sticky='w', **widget_options)

        ###########################
        # Stimulus Option Widgets #
        ###########################
        # Randomize
        check_random = ttk.Checkbutton(
            lfrm_stimulus, 
            text="Randomize",
            takefocus=0, 
            variable=self.settings['randomize']
            )
        check_random.grid(
            row=5, 
            column=5, 
            columnspan=20, 
            sticky='w',
            **widget_options
            )
        
        # Repetitions
        ttk.Label(
            lfrm_stimulus, 
            text="Presentation(s):", 
            takefocus=0
            ).grid(
                row=10, 
                column=5, 
                sticky='e', 
                **widget_options
                )
        ttk.Entry(
            lfrm_stimulus, 
            width=5, 
            textvariable=self.settings['repetitions']
            ).grid(
                row=10,
                column=10,
                **widget_options
                )

        #################
        # Noise Widgets #
        #################
        # Noise level
        lbl_noise_level = ttk.Label(lfrm_noise, text="Level:")
        lbl_noise_level.grid(row=5, column=5, sticky='e', **widget_options)
        noise_level_tt = Hovertip(
            anchor_widget=lbl_noise_level,
            text="A single presentation level for the noise.",
            hover_delay=tt_delay
            )
        ttk.Entry(
            lfrm_noise, 
            width=7,
            textvariable=self.settings['noise_level_dB']
            ).grid(row=5, column=10, sticky='w', **widget_options)

        ###################
        # Audio Directory #
        ###################
        # Descriptive label
        ttk.Label(lfrm_audiopath, text="Path:").grid(
            row=5, column=5, sticky='e', **widget_options)

        # Create textvariable
        self.audio_var = tk.StringVar()

        # Fit path to label
        self._shorten_path(
            full_path=self.settings['import_audio_path'].get(),
            num_chars=45, 
            label_var=self.audio_var
            )

        # Audio directory label
        ttk.Label(
            lfrm_audiopath, 
            textvariable=self.audio_var, 
            borderwidth=2, 
            relief="solid", 
            width=40
            ).grid(row=5, column=10, sticky='w', **widget_options)
        ttk.Button(
            lfrm_audiopath, 
            text="Browse", 
            command=self._get_audio_directory,
            ).grid(row=10, column=10, sticky='w', **widget_options)

        ###############
        # Matrix File #
        ###############
        # Descriptive label
        ttk.Label(lfrm_matrixpath, text="Path:").grid(
            row=5, 
            column=5, 
            sticky='e', 
            **widget_options
            )

        # Create textvariable
        self.matrix_var = tk.StringVar()

        # Fit path to label
        self._shorten_path(
            full_path=self.settings['matrix_file_path'].get(),
            num_chars=45, 
            label_var=self.matrix_var
            )
        
        # Matrix file label
        ttk.Label(
            lfrm_matrixpath, 
            textvariable=self.matrix_var, 
            borderwidth=2, 
            relief="solid", 
            width=40
            ).grid(row=5, column=10, sticky='w', **widget_options)
        ttk.Button(
            lfrm_matrixpath, 
            text="Browse", 
            command=self._get_matrix_file,
            ).grid(row=10, column=10, sticky='w', **widget_options)
            

        # Submit button
        btn_submit = ttk.Button(
            self, 
            text="Submit", 
            command=self._on_submit
            )
        btn_submit.grid(row=30, column=5, columnspan=20, pady=(0, 10))

        # Center ImportView over root
        tmpy.tkgui_funcs.center_window_over_parent(self)

    #############
    # Functions #
    #############
    def _shorten_path(self, full_path, num_chars, label_var=None):
        # Truncate path
        short_path = tmpy.helper_funcs.truncate_path(
            full_path=full_path,
            num_chars=num_chars
        )
        if label_var:
            # Update label value with truncated path
            label_var.set(short_path)


    def _get_audio_directory(self):
        """ Get audio files directory from user via file browser. """
        # Get directory from user
        self.settings['import_audio_path'].set(
            filedialog.askdirectory(title="Audio File Directory")
        )
        # Fit path length to label
        self._shorten_path(
            full_path=self.settings['import_audio_path'].get(),
            num_chars=45,
            label_var=self.audio_var
            )


    def _get_matrix_file(self):
        """ Get matrix file path from user via file browser. """
        matrix_path = filedialog.askopenfilename(
                title="Matrix File",
                filetypes=(("CSV Files","*.csv"),)
                )
        self.settings['matrix_file_path'].set(matrix_path)
        # Fit path length to label
        self._shorten_path(
            full_path=self.settings['matrix_file_path'].get(),
            num_chars=45,
            label_var=self.matrix_var
            )

    def _on_submit(self):
        """ Send submit event to controller and close window. """
        logger.debug("Sending 'SUBMIT' event to controller")
        self.parent.event_generate('<<ImportViewSubmit>>')
        logger.debug("Destroying ImportView instance")
        self.destroy()


if __name__ == "__main__":
    pass
