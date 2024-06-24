""" Import matrix file view for Speech Tasker. 

    Written by: Travis M. Moore
    Last edited: June 19, 2024
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

        """ This is getting silly. Maybe just rename control variables
        as they should appear in error messages.

        That still leaves the issue of updating variables when filling
        out the form... But maybe those values aren't written to file?
            Actually, is this really a problem? Might not be. 
        """
        # Control variable dict
        self._vars = {
            'Subject': ('subject', tk.StringVar(
                value=self.settings['subject'].get()
            )),
            'Condition': ('condition', tk.StringVar()),
            'Presentations': ('repetitions', tk.IntVar()),
            'Randomize': ('randomize', tk.IntVar()),
            'Noise Level': ('noise_level_dB', tk.DoubleVar())
        }
        
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
        # Shared frame options
        frame_options = {
            'padx': 10, 
            'pady': 10, 
            'ipadx': 5, 
            'ipady': 5,
            'sticky': 'nsew'
            }
        # Shared widget options
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

        # AskPathWidgets
        lfrm_path = ttk.Labelframe(self, text="File Locations")
        lfrm_path.grid(row=5, rowspan=16, column=10, **frame_options)

        # Audio file browser
        lfrm_audiopath = ttk.Labelframe(lfrm_path, text="Audio File Directory")
        lfrm_audiopath.grid(row=5, column=5, **frame_options)

        # Matrix file browser
        lfrm_matrixpath = ttk.Labelframe(lfrm_path, text='Matrix File Path')
        lfrm_matrixpath.grid(row=10, column=5, **frame_options)

        ###################
        # Session Widgets #
        ###################
        # Subject
        w.LabelInput(
            lfrm_session,
            label="Subject",
            var=self._vars['Subject'][1], #self.settings['subject'],
            input_class=w.RequiredEntry,
            tool_tip="A unique subject identifier."
                + "\nCan be alpha, numeric, or both."
        ).grid(row=5, column=5, padx=5, pady=(5,0))

        # Condition
        w.LabelInput(
            lfrm_session,
            label="Condition",
            var=self._vars['Condition'][1], #self.settings['condition'],
            input_class=w.RequiredEntry,
            tool_tip="A unique condition name."
                + "\nCan be alpha, numeric, or both."
                + "\nSeparate words with underscores."
        ).grid(row=5, column=10, padx=5, pady=(5,0))

        ###########################
        # Stimulus Option Widgets #
        ###########################
        # Presentations
        w.LabelInput(
            lfrm_stimulus,
            label="Presentations",
            var=self._vars['Presentations'][1], #self.settings['repetitions'],
            input_class=w.RequiredEntry,
            tool_tip="Number of times to present the trials in the "
                + "matrix file."
        ).grid(row=5, column=5, padx=5, pady=(5,0))

        # Randomize
        w.LabelInput(
            lfrm_stimulus,
            label="Randomize",
            var=self._vars['Randomize'][1], #self.settings['randomize'],
            input_class=ttk.Checkbutton,
            input_args={'takefocus': 0},
            tool_tip="Randomize trials in provided matrix file."
        ).grid(row=5, column=10, padx=5, pady=(5,0), sticky='n')

        #################
        # Noise Widgets #
        #################
        # Noise level
        w.LabelInput(
            lfrm_noise,
            label="Level",
            var=self._vars['Noise Level'][1], #self.settings['noise_level_dB'],
            input_class=w.RequiredEntry,
            tool_tip="Level of the noise."
        ).grid(row=5, column=5, padx=5, pady=(5,0), sticky='n')

        #####################
        # File Path Widgets #
        #####################
        self.columnconfigure(5, weight=1)
        
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
            parent=lfrm_matrixpath,
            var=self.settings['matrix_file_path'],
            title_args={'text': 'Matrix File'},
            type='file',
            tool_tip="Path to the matrix file."
        ).grid(row=5, column=5)

        # Save matrix file checkbutton
        ttk.Checkbutton(
            lfrm_matrixpath, 
            text="Write matrix file to CSV",
            variable=self.settings['write_matrix'],
            onvalue=1,
            offvalue=-1,
            takefocus=0
            ).grid(
                row=15, 
                column=5, 
                columnspan=15, 
                **widget_options, 
                sticky='w'
                )

        #################
        # Submit Button #
        #################
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
    def _on_submit(self):
        """ Send submit event to controller and close window. """
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
        self.parent.event_generate('<<ImportViewSubmit>>')
        logger.info("Destroying ImportView instance")
        self.destroy()

################
# Module Guard #
################
if __name__ == "__main__":
    pass
