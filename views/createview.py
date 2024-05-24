""" Create matrix file view for Speech Tasker. 

    Written by: Travis M. Moore
    Last edited: May 17, 2024
"""

###########
# Imports #
###########
# Standard library
import logging
import tkinter as tk
from idlelib.tooltip import Hovertip
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

# Custom
import tmpy

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
        logger.debug("Initializing CreateView")

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
        lfrm_sentence = ttk.Labelframe(self, text='Sentence Options')
        lfrm_sentence.grid(row=10, column=5, rowspan=20, **frame_options)

        # Noise options
        lfrm_noise = ttk.Labelframe(self, text='Noise Options')
        #lfrm_noise.grid(row=15, column=5, **frame_options)
        lfrm_noise.grid(row=15, column=20, **frame_options)

        # Audio file browser
        lfrm_audiopath = ttk.Labelframe(self, text="Audio File Directory")
        lfrm_audiopath.grid(
            row=5,#20, 
            column=20,#5, 
            **frame_options, 
            )

        # Sentence file browser
        lfrm_sentencepath = ttk.Labelframe(self, text="Sentence CSV File")
        lfrm_sentencepath.grid(
            row=10,
            column=20,
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
        
        ####################
        # Sentence Widgets #
        ####################
        # Lists
        lbl_lists = ttk.Label(
            lfrm_sentence,
            text="List(s):",
            )
        lbl_lists.grid(
            row=5,
            column=5,
            sticky='e',
            **widget_options
            )
        lists_tt = Hovertip(
            anchor_widget=lbl_lists,
            text="The list numbers to include in the session." +
                "\nSeparate multiple values with a comma and space: 1, 2, 3",
            hover_delay=tt_delay
            )
        ttk.Entry(
            lfrm_sentence,
            textvariable=self.settings['sentence_lists']).grid(
                row=5, column=10, sticky='ew', **widget_options)
        

        # Sentence level(s)
        lbl_sentence_level = ttk.Label(lfrm_sentence, text="Level(s):")
        lbl_sentence_level.grid(
            row=10, 
            column=5, 
            sticky='e', 
            **widget_options
            )
        sentence_level_tt = Hovertip(
            anchor_widget=lbl_sentence_level,
            text="A single starting presentation level for the sentences.",
            hover_delay=tt_delay
            )
        ttk.Entry(
            lfrm_sentence, 
            textvariable=self.settings['sentence_levels']).grid(
                row=10, column=10, sticky='w', **widget_options)


        # Sentence speaker(s)
        lbl_sentence_speakers = ttk.Label(lfrm_sentence, text="Speaker(s):")
        lbl_sentence_speakers.grid(
            row=15,
            column=5, 
            sticky='e', 
            **widget_options
            )
        sentence_speakers_tt = Hovertip(
            anchor_widget=lbl_sentence_speakers,
            text="Speakers to use for presenting sentences." +
                "\nSpeakers will be randomly assigned.",
            hover_delay=tt_delay
            )
        ttk.Entry(lfrm_sentence,
            textvariable=self.settings['sentence_speakers']
            ).grid(row=15, column=10, sticky='w', **widget_options)
        

        # Number of sentences per list
        lbl_sentences_per_list = ttk.Label(
            lfrm_sentence,
            text="Sentences per List:",
            takefocus=0
            )
        lbl_sentences_per_list.grid(
            row=20,
            column=5,
            sticky='e',
            **widget_options
            )
        lbl_sentences_per_list_tt = Hovertip(
            anchor_widget=lbl_lists,
            text="The number of sentences to present from each list.",
            hover_delay=tt_delay
            )
        ttk.Entry(
            lfrm_sentence,
            width=5,
            textvariable=self.settings['sentences_per_list']).grid(
                row=20, column=10, sticky='w', **widget_options)


        # Number of repetitions
        lbl_repetitions = ttk.Label(
            lfrm_sentence,
            text="Repetitions:",
            takefocus=0
            )
        lbl_repetitions.grid(
            row=25,
            column=5,
            sticky='e',
            **widget_options
            )
        lbl_repetitions_tt = Hovertip(
            anchor_widget=lbl_repetitions,
            text="The number of times to repeat each stimulus."\
                +"\nFor no repetitions enter '1'.",
            hover_delay=tt_delay
            )
        ttk.Entry(
            lfrm_sentence,
            width=5,
            textvariable=self.settings['repetitions']).grid(
                row=25, column=10, sticky='w', **widget_options)


        # Randomize
        check_random = ttk.Checkbutton(
            lfrm_sentence, 
            text="Randomize",
            takefocus=0, 
            variable=self.settings['randomize']
            )
        check_random.grid(
            row=30, 
            column=5,  
            sticky='e',
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

        ######################
        # Sentence Directory #
        ######################
        # Path label
        ttk.Label(lfrm_sentencepath, text="Path:").grid(
            row=5, column=5, sticky='e', **widget_options)

        # Create textvariable
        self.sentence_var = tk.StringVar()

        # Fit path to label
        self._shorten_path(
            full_path=self.settings['sentence_file_path'].get(),
            num_chars=45, 
            label_var=self.sentence_var
            )

        # Sentence directory label
        ttk.Label(
            lfrm_sentencepath, 
            textvariable=self.sentence_var, 
            borderwidth=2, 
            relief="solid", 
            width=40
            ).grid(row=5, column=10, sticky='w', **widget_options)
        ttk.Button(
            lfrm_sentencepath, 
            text="Browse", 
            command=self._get_sentence_directory,
            ).grid(row=10, column=10, sticky='w', **widget_options)


        # Submit button
        btn_submit = ttk.Button(
            self, 
            text="Submit", 
            command=self._on_submit
            )
        btn_submit.grid(row=30, column=5, columnspan=20, pady=(0, 10))

        # Center CreateView over root
        tmpy.functions.tkgui_funcs.center_window_over_parent(self)

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


    def _get_sentence_directory(self):
        """ Get sentence CSV file from user via file browser. """
        # Get file
        self.settings['sentence_file_path'].set(
            filedialog.askopenfilename(title="Sentence CSV File")
        )
        # Fit path length to label
        self._shorten_path(
            full_path=self.settings['sentence_file_path'].get(),
            num_chars=45,
            label_var=self.sentence_var
        )


    def _chk_lengths(self):
        """ Validate the number of entered lists and presentations levels.
            If an invalid number exists, display an error message and return 
            invalid flag.
        """
        lists = self.settings['sentence_lists'].get()
        lists = tmpy.functions.helper_funcs.string_to_list(lists, 'int')

        levels = self.settings['sentence_levels'].get()
        levels = tmpy.functions.helper_funcs.string_to_list(levels, 'int')

        if (len(levels) != len(lists)) and (len(levels) != 1):
            messagebox.showerror(
                title="Invalid Parameters",
                message="Invalid number of levels!",
                detail="Either provide a single level, or an equal number of levels and lists."
            )
            return False
        else:
            return True
        

    def _on_submit(self):
        """ Send submit event to controller and close window. """
        # Validate number of lists and levels
        if not self._chk_lengths():
            return

        logger.debug("Sending 'SUBMIT' event to controller")
        self.parent.event_generate('<<CreateViewSubmit>>')
        logger.debug("Destroying CreateView instance")
        self.destroy()


if __name__ == "__main__":
    pass
