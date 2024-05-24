""" Settings view for Speech Tasker. 

    Written by: Travis M. Moore
    Last edited: May 15, 2024
"""

###########
# Imports #
###########
# Standard library
import logging
import tkinter as tk
from idlelib.tooltip import Hovertip
from tkinter import ttk

# Custom
from views.importview import ImportView
from views.createview import CreateView

###########
# Logging #
###########
# Create new logger
logger = logging.getLogger(__name__)

################
# SettingsView #
################
class SettingsView(tk.Toplevel):
    """ View for setting session parameters. """
    def __init__(self, parent, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        logger.debug("Initializing SettingsView")

        # Assign attributes
        self.parent = parent
        self.settings = settings

        # Window setup
        self.withdraw()
        self.resizable(False, False)
        self.title("Settings")
        self.grab_set()

        # Populate view with widgets
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

        # Submit button frame
        frm_submit = ttk.Frame(self)
        frm_submit.grid(row=10, column=5)

        ###################
        # Notebook Widget #
        ###################
        # Create notebook tabs for various use cases
        notebook = ttk.Notebook(self, takefocus=0)
        notebook.grid(row=5, column=5, **frame_options)

        # Run with provided matrix file
        import_view = ImportView(notebook, self.settings)
        import_view.grid(row=5, column=5)
        import_tab = ttk.Frame(notebook, takefocus=0)
        notebook.add(import_view, text="Import")

        # Create matrix file from speech test
        create_view = CreateView(notebook, self.settings)
        create_view.grid(row=5, column=5)
        create_tab = ttk.Frame(notebook, takefocus=0)
        notebook.add(create_view, text="Create")


        # # Session info
        # lfrm_session = ttk.Labelframe(import_tab, text='Settings')
        # lfrm_session.grid(row=5, column=5, **frame_options)

        # # Sentence options
        # lfrm_sentence = ttk.Labelframe(create_matrix_file, text='Sentence Options')
        # lfrm_sentence.grid(row=10, column=5, **frame_options)

        # # Noise options
        # #lfrm_noise = ttk.Labelframe(self, text='Noise Options')
        # #lfrm_noise.grid(row=15, column=5, **frame_options, sticky='nsew')

        # # # Presentation options
        # # lfrm_present = ttk.Labelframe(self, text="Presentation Options")
        # # lfrm_present.grid(row=15, column=5, **frame_options)

        # # # Audio file browser
        # # lfrm_audiopath = ttk.Labelframe(self, text="Audio File Directory")
        # # lfrm_audiopath.grid(row=15, column=5, **frame_options, ipadx=5, 
        # #     ipady=5)

        # # # Matrix file browser
        # # lfrm_matrixpath = ttk.Labelframe(self, text='Matrix File Path')
        # # lfrm_matrixpath.grid(row=20, column=5, **frame_options, ipadx=5, 
        # #     ipady=5)

        # ###################
        # # Session Widgets #
        # ###################
        # # Subject
        # lbl_sub = ttk.Label(lfrm_session, text="Subject:")
        # lbl_sub.grid(row=5, column=5, sticky='e', **widget_options)
        # sub_tt = Hovertip(
        #     anchor_widget=lbl_sub,
        #     text="A unique subject identifier."+
        #         "\nCan be alpha, numeric, or both.",
        #     hover_delay=tt_delay
        #     )
        # ttk.Entry(lfrm_session, 
        #     textvariable=self.settings['subject']
        #     ).grid(row=5, column=10, sticky='w', **widget_options)


        # # Condition
        # lbl_condition = ttk.Label(lfrm_session, text="Condition:")
        # lbl_condition.grid(row=10, column=5, sticky='e', **widget_options)
        # condition_tt = Hovertip(
        #     anchor_widget=lbl_condition,
        #     text="A unique condition name.\nCan be alpha, numeric, or both." +
        #         "\nSeparate words with underscores.",
        #     hover_delay=tt_delay
        #     )
        # ttk.Entry(lfrm_session, 
        #     textvariable=self.settings['condition']
        #     ).grid(row=10, column=10, sticky='w', **widget_options)
        
        # ####################
        # # Sentence Widgets #
        # ####################
        # # Lists
        # lbl_lists = ttk.Label(lfrm_sentence,
        #           text="List(s):",
        #           takefocus=0
        #           )
        # lbl_lists.grid(row=5,
        #                  column=5,
        #                  sticky='e',
        #                  **widget_options
        #                  )
        # lists_tt = Hovertip(
        #     anchor_widget=lbl_lists,
        #     text="The list numbers to include in the session." +
        #         "\nSeparate multiple values with a comma and space: 1, 2, 3",
        #     hover_delay=tt_delay
        #     )
        # ttk.Entry(lfrm_sentence,
        #           textvariable=self.settings['sentence_lists']
        #           ).grid(row=5, column=10, **widget_options)
        

        # # Number of sentences per list
        # lbl_sentences_per_list = ttk.Label(lfrm_sentence,
        #           text="Sentences per List:",
        #           takefocus=0
        #           )
        # lbl_sentences_per_list.grid(row=10,
        #                  column=5,
        #                  sticky='e',
        #                  **widget_options
        #                  )
        # lbl_sentences_per_list_tt = Hovertip(
        #     anchor_widget=lbl_lists,
        #     text="The numbers of sentences to present from each list.",
        #     hover_delay=tt_delay
        #     )
        # ttk.Entry(lfrm_sentence,
        #           textvariable=self.settings['sentences_per_list']
        #           ).grid(row=10, column=10, **widget_options)


        # # Sentence level(s)
        # lbl_sentence_level = ttk.Label(lfrm_sentence, text="Level(s):")
        # lbl_sentence_level.grid(
        #     row=15, 
        #     column=5, 
        #     sticky='e', 
        #     **widget_options
        #     )
        # sentence_level_tt = Hovertip(
        #     anchor_widget=lbl_sentence_level,
        #     text="A single starting presentation level for the sentences.",
        #     hover_delay=tt_delay
        #     )
        # ttk.Entry(lfrm_sentence, width=7,
        #     textvariable=self.settings['sentence_levels']
        #     ).grid(row=15, column=10, sticky='w', **widget_options)


        # # Sentence speaker(s)
        # lbl_sentence_speakers = ttk.Label(lfrm_sentence, text="Speaker(s):")
        # lbl_sentence_speakers.grid(
        #     row=20,
        #     column=5, 
        #     sticky='e', 
        #     **widget_options
        #     )
        # sentence_speakers_tt = Hovertip(
        #     anchor_widget=lbl_sentence_speakers,
        #     text="Speakers to use for presenting sentences." +
        #         "\nSpeakers will be randomly assigned.",
        #     hover_delay=tt_delay
        #     )
        # ttk.Entry(lfrm_sentence, width=7,
        #     textvariable=self.settings['sentence_speakers']
        #     ).grid(row=20, column=10, sticky='w', **widget_options)

        # #################
        # # Noise Widgets #
        # #################
        # # # Noise level
        # # lbl_noise_level = ttk.Label(lfrm_noise, text="Level:")
        # # lbl_noise_level.grid(row=5, column=5, sticky='e', **widget_options)
        # # noise_level_tt = Hovertip(
        # #     anchor_widget=lbl_noise_level,
        # #     text="A single presentation level for the noise.",
        # #     hover_delay=tt_delay
        # #     )
        # # ttk.Entry(lfrm_noise, width=7,
        # #     textvariable=self.settings['noise_level_dB']
        # #     ).grid(row=5, column=10, sticky='w', **widget_options)


        # # # Randomize
        # # check_random = ttk.Checkbutton(lfrm_sentence, 
        # #                                text="Randomize",
        # #                                takefocus=0, 
        # #                                variable=self.settings['randomize']
        # #                                )
        # # check_random.grid(row=5, 
        # #                   column=5, 
        # #                   columnspan=20, 
        # #                   sticky='w',
        # #                   **widget_options
        # #                   )
        
        # # # Repetitions
        # # ttk.Label(lfrm_sentence, 
        # #           text="Presentation(s)", 
        # #           takefocus=0
        # #           ).grid(row=10, 
        # #                  column=5, 
        # #                  sticky='e', 
        # #                  **widget_options
        # #                  )
        # # ttk.Entry(lfrm_sentence, 
        # #           width=5, 
        # #           textvariable=self.settings['repetitions']
        # #           ).grid(row=10,
        # #                  column=10
        # #                  )



        # # ###################
        # # # Audio Directory #
        # # ###################
        # # # Descriptive label
        # # ttk.Label(lfrm_audiopath, text="Path:"
        # #     ).grid(row=20, column=5, sticky='e', **widget_options)

        # # # Retrieve and truncate previous audio directory
        # # short_audio_path = general.truncate_path(
        # #     self.settings['audio_files_dir'].get()
        # # )

        # # # Create textvariable
        # # self.audio_var = tk.StringVar(value=short_audio_path)

        # # # Audio directory label
        # # ttk.Label(lfrm_audiopath, textvariable=self.audio_var, 
        # #     borderwidth=2, relief="solid", width=60
        # #     ).grid(row=20, column=10, sticky='w')
        # # ttk.Button(lfrm_audiopath, text="Browse", 
        # #     command=self._get_audio_directory,
        # #     ).grid(row=25, column=10, sticky='w', pady=(0, 10))


        # Submit button
        btn_submit = ttk.Button(
            frm_submit, 
            text="Submit", 
            command=self._on_submit
            )
        btn_submit.grid(row=5, column=5, columnspan=2, pady=(0, 10))

        # Center the session dialog window
        self._center_window()


    #############
    # Functions #
    #############
    def _center_window(self):
        """ Center the TopLevel window over the root window. """
        logger.debug("Centering window over parent")
        # Get updated window size (after drawing widgets)
        self.update_idletasks()

        # Calculate the x and y coordinates to center the window
        x = self.parent.winfo_x() \
            + (self.parent.winfo_width() - self.winfo_reqwidth()) // 2
        y = self.parent.winfo_y() \
            + (self.parent.winfo_height() - self.winfo_reqheight()) // 2
        
        # Set the window position
        self.geometry("+%d+%d" % (x, y))

        # Display window
        self.deiconify()


    def _on_submit(self):
        """ Send submit event to controller and close window. """
        logger.debug("Sending 'SUBMIT' event to controller")
        self.parent.event_generate('<<SettingsSubmit>>')
        logger.debug("Destroying SettingsView instance")
        self.destroy()


if __name__ == "__main__":
    pass
