""" Speech Tasker. 

    A flexible app for presenting a number of standardized
    speech tests (e.g., HINT). The Speech Tasker can either
    import a matrix file or create one based on provided
    speech stimuli.  

    Written by: Travis M. Moore
    Created: May 15, 2024
"""

###########
# Imports #
###########
# Standard library
import datetime
import importlib
import logging.config
import logging.handlers
import os
import sys
import tkinter as tk
from tkinter import font
import webbrowser
from pathlib import Path
from tkinter import messagebox

# Third party
import markdown
import numpy as np

# Add custom path
try:
    sys.path.append(os.environ['TMPY'])
except KeyError:
    sys.path.append('C:\\Users\\MooTra\\Code\\Python')

# Custom
import app_assets
import menus
import models
import setup
import tmpy
import views
from tmpy import tkgui
from tmpy.functions import helper_funcs

##########
# Logger #
##########
# Create new logger
logger = logging.getLogger(__name__)

#################
# Splash Screen #
#################
class Splash(tk.Toplevel):
    def __init__(self, parent, text):
        tk.Toplevel.__init__(self, parent)
        #logger.info("Initializing splash screen")
        self.withdraw()
        self.title("Please wait")
        self.geometry("300x200")
        self.resizable(False, False)
        tk.Label(self, text=text).pack()
        self.center_splashscreen()
        self.update()
        

    def center_splashscreen(self):
        """ Center the splash screen. """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        #print(f"\n\nscreen width, height: {screen_width}, {screen_height}")
        #print(f"geometry: {self.geometry()}")
        self.deiconify()

###############
# Application #
###############
class Application(tk.Tk):
    """ Application root window. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #splash_screen = Splash(parent=self, text="Loading Automated HINT")

        self.withdraw() # Hide root window during setup

        #############
        # Constants #
        #############
        self.REF = __name__
        self.NAME = 'Speech Tasker'
        self.VERSION = '0.1.2'
        self.EDITED = 'June 05, 2024'

        ################
        # Window setup #
        ################
        self.resizable(False, False)
        self.title(self.NAME)
        self.taskbar_icon = tk.PhotoImage(
            file=tkgui.shared_assets.images.LOGO_FULL_PNG
            )
        self.iconphoto(True, self.taskbar_icon)

        # Update default font
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.option_add("*Font", default_font)

        # Custom styles
        from tkinter import ttk
        style = ttk.Style()
        style.configure('Bold.TLabel', font=('TKDefaultFont', 12, 'bold'))
        style.configure('Gray.TLabel', foreground="gray")
        style.configure('TLabelframe.Label', foreground='blue', font=('TkDefaultFont', 13))

        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Load current settings from file
        # or load defaults if file does not exist yet
        self.settings_model = tkgui.models.SettingsModel(
            parent=self,
            settings_vars=setup.settings_vars.fields,
            app_name=self.NAME
            )
        self._load_settings()

        # Set up custom logger as soon as config dir is created
        # (i.e., after settings model has been initialized)
        config = tmpy.functions.logging_funcs.setup_logging(self.NAME)
        logging.config.dictConfig(config)
        logger.info("Started custom logger")

        # Default public attributes
        self.level_data = []
        logger.info("Setting controller 'start' flag to True")
        self.start_flag = True

        # Assign special quit function on window close
        self.protocol('WM_DELETE_WINDOW', self._quit)

        # Load calibration model
        self.calibration_model = tkgui.models.CalibrationModel(self.settings)

        # Load main view
        self.main_view = views.MainView(self, self.settings)
        self.main_view.grid(row=5, column=5)

        # Create menu settings dictionary
        self._app_info = {
            'name': self.NAME,
            'version': self.VERSION,
            'last_edited': self.EDITED
        }
        # Load menus
        self.menu = menus.MainMenu(self, self._app_info)
        self.config(menu=self.menu)

        # Create data handler
        self.dh = tmpy.handlers.DataHandler()

        # Create score model
        self.sm = models.ScoreModel()

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileImportMatrixFile>>': lambda _: self._import_mfile_view(),
            '<<FileCreateMatrixFile>>': lambda _: self._create_mfile_view(),
            '<<FileStart>>': lambda _: self.on_start(),
            '<<FileQuit>>': lambda _: self._quit(),

            # CreateView window
            '<<CreateViewSubmit>>': lambda _: self._create_mfile(),

            # ImportView window
            '<<ImportViewSubmit>>': lambda _: self._save_settings(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),

            # Help menu
            '<<HelpREADME>>': lambda _: self._show_help(),
            '<<HelpChangelog>>': lambda _: self._show_changelog(),

            # Settings window
            '<<SettingsSubmit>>': lambda _: self._save_settings(),

            # Calibration window
            '<<CalPlay>>': lambda _: self.play_calibration_file(),
            '<<CalStop>>': lambda _: self.stop_audio(),
            '<<CalibrationSubmit>>': lambda _: self._calc_offset(),

            # Audio settings window
            '<<AudioViewSubmit>>': lambda _: self._save_settings(),

            # Main View
            '<<MainNext>>': lambda _: self.on_next(),
            '<<MainRepeat>>': lambda _: self.play(),
        }

        # Bind callbacks to sequences
        logger.info("Binding callbacks to controller")
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        ###################
        # Version Control #
        ###################
        # Check for updates
        if self.settings['check_for_updates'].get() == 'yes':
            _filepath = self.settings['version_lib_path'].get()
            u = tkgui.models.VersionModel(_filepath, self.NAME, self.VERSION)
            if u.status == 'mandatory':
                logger.critical("This version: %s", self.VERSION)
                logger.critical("Mandatory update version: %s", u.new_version)
                messagebox.showerror(
                    title="New Version Available",
                    message="A mandatory update is available. Please install " +
                        f"version {u.new_version} to continue.",
                    detail=f"You are using version {u.app_version}, but " +
                        f"version {u.new_version} is available."
                )
                logger.critical("Application failed to initialize")
                self.destroy()
                return
            elif u.status == 'optional':
                messagebox.showwarning(
                    title="New Version Available",
                    message="An update is available.",
                    detail=f"You are using version {u.app_version}, but " +
                        f"version {u.new_version} is available."
                )
            elif u.status == 'current':
                pass
            elif u.status == 'app_not_found':
                messagebox.showerror(
                    title="Update Check Failed",
                    message="Cannot retrieve version number!",
                    detail=f"'{self.NAME}' does not exist in the version library."
                 )
            elif u.status == 'library_inaccessible':
                messagebox.showerror(
                    title="Update Check Failed",
                    message="The version library is unreachable!",
                    detail="Please check that you have access to Starfile."
                )

        # Temporarily disable Help menu until documents are written
        self.menu.help_menu.entryconfig('README...', state='disabled')

        # Destroy splash screen
        if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
            import pyi_splash
            pyi_splash.update_text('UI Loaded ...')
            pyi_splash.close()
            logger.info('Splash screen closed.')

        # Center main window
        self.center_window()

        # Initialization successful
        logger.info('Application initialized successfully')

    #####################
    # General Functions #
    #####################
    def center_window(self):
        """ Center the root window. """
        self.update_idletasks()
        logger.info("Centering root window after drawing widgets")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    # def center_window2(self, window):
    #     """ Center the root window. """
    #     logger.info("Centering root window after drawing widgets")
    #     window.update_idletasks()
    #     screen_width = window.winfo_screenwidth()
    #     screen_height = window.winfo_screenheight()
    #     size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    #     x = screen_width/2 - size[0]/2
    #     y = screen_height/2 - size[1]/2
    #     window.geometry("+%d+%d" % (x, y))
    #     window.deiconify()


    def _create_filename(self):
        """ Create file name and path. """
        logger.info("Creating file name with date stamp")
        datestamp = datetime.datetime.now().strftime("%Y_%b_%d_%H%M")
        sub = self.settings['subject'].get()
        cond = self.settings['condition'].get()
        filename = '_'.join([sub, cond, datestamp, ".csv"])
        return filename


    def _quit(self):
        """ Exit the application. """
        logger.info("User ended the session")
        self.destroy()

    ###################
    # File Menu Funcs #
    ###################
    def _import_mfile_view(self):
        """ Show import matrix file window. """
        logger.info("Calling ImportView window")
        self.import_view = views.ImportView(self, self.settings)
        self.import_view.title("Import Matrix File")

    def _create_mfile_view(self):
        """ Show create matrix file window. """
        logger.info("Calling CreateView window")
        self.create_view = views.CreateView(self, self.settings)
        self.create_view.title("Create Matrix File")

    def _prepare_trials(self):
        """ Import matrix file and organize trials. """
        # Get values from TkVars
        vals = tmpy.functions.tkgui_funcs.get_tk_values(self.settings)
        # Create dict of arguments
        pars = {
            'filepath': vals['matrix_file_path'],
            'repetitions': vals['repetitions'],
            'randomize': vals['randomize'],
            'write': self.settings['write_matrix'].get()
        }
        # Create and write matrix CSV file
        mf = models.ImportSpeechTaskerMatrix(**pars)
        return mf.import_matrix_file()

    def on_start(self):
        """ Import matrix file and create TrialHandler. """
        logger.info("Start button pressed")
        # Create filename with time stamp
        self.filename = self._create_filename()
        # Prepare trials
        trials = self._prepare_trials()
        # Create trial handler
        self.th = tmpy.handlers.TrialHandler(
            trials_df=trials
            )
        # Disable "Start" from File menu
        self.menu.file_menu.entryconfig('Start', state='disabled')
        # Enable user controls
        self.main_view.enable_user_controls(text="Next")
        # Start first trial
        self.on_next()

    #######################
    # Main View Functions #
    #######################
    def _prepare_stimulus(self):
        """ Prepare audio for playback. """
        logger.info("Preparing audio for playback")
        # Calculate level based on SLM offset
        """ WARNING: Use a separate 'starting level' variable to avoid
            automatically using the last presented level on startup.

            Do NOT use: self.settings['desired_level_dB'].get()
        """
        self._calc_level(self.th.trial_info['level'])
        # Add directory to file name
        #self.settings['import_audio_path'].get(),
        stim = Path(os.path.join(
            self.settings['import_audio_path'].get(),
            self.th.trial_info['file']
            )
            )
        return stim

    def play(self):
        """ Begin audio playback. """
        # Prepare audio for playback
        stim = self._prepare_stimulus()
        # Present WGN
        self.present_audio(
            audio=stim,
            pres_level=self.settings['adjusted_level_dB'].get()
            )

    def _end_of_task(self):
        """ Present message to user and destroy root. """
        messagebox.showinfo(
            title="Task Complete",
            message="You have completed the task!"
            )
        logger.info("Closing application")
        self.quit()

    def _save(self, responses):
        """ Save data to CSV, on a per trial basis, after scoring 
        each trial. 
        """
        # Add directory to filename
        directory = 'Data'
        fullpath = os.path.join(directory, self.filename)
        # Define items to include in CSV
        order = ['trial',
                 'subject',
                 'condition',
                 'file',
                 'list_num',
                 'sentence_num',
                 'speaker',
                 'desired_level_dB',
                 'correct',
                 'incorrect',
                 'total_words',
                 'num_correct'
                 ]
        try:
            self.dh.save_data(
                filepath=fullpath,
                dict_list=[self.settings, responses, self.th.trial_info],
                order=order
            )
        except PermissionError as e:
            logger.exception(e)
            messagebox.showerror(
                title="Access Denied",
                message="Data not saved! Cannot write to file!",
                detail=e
            )
            return
        except OSError as e:
            logger.exception(e)
            messagebox.showerror(
                title="File Not Found",
                message="Cannot find file or directory!",
                detail=e
            )
            return
        
    def on_next(self):
        """ Get and present next trial. """
        logger.info("Fetching next trial")
        # Score and save responses
        if not self.start_flag:
            # Score response
            scored_words = self.sm.score(
                words=self.main_view.words_dict,
                button_states=self.main_view.buttonstates_dict
            )
            # Write response to CSV
            self._save(scored_words)
            # Append trial level to level_data
            self.level_data.append(self.settings['desired_level_dB'].get())
        if self.start_flag:
            # Set start flag to False after intitial trial
            logger.info("Setting 'start' flag to False")
            self.start_flag = False
        # Get next trial
        try:
            self.th.next()
        except IndexError:
            logger.warning("End of trials!")
            self._end_of_task()
            return
        # Display sentence with checkbuttons
        self.main_view.update_main_label(
            sentence=self.th.trial_info['sentence'])
        # Update trial label
        self.main_view.update_info_labels(
            trial=self.th.trial_num,
            speaker=self.th.trial_info['speaker']
            )
        # Disable user controls during playback
        self.main_view.disable_user_controls(text="Presenting")
        # Present audio
        self.play()
        # Enable user controls after playback
        self.after(int(np.ceil(self.a.dur*1000)), 
                   lambda: self.main_view.enable_user_controls(text="Next")
                   )

    ########################
    # CreateView Functions #
    ########################
    def _create_mfile(self):
        """ Create a matrix file and write to CSV. """
        # Get values from TkVars
        vals = tmpy.functions.tkgui_funcs.get_tk_values(self.settings)

        # Create dict of arguments
        pars = {
            'filepath': vals['sentence_file_path'],
            'lists': helper_funcs.string_to_list(vals['sentence_lists'], 'int'),
            'sentences_per_list': vals['sentences_per_list'],
            'levels': helper_funcs.string_to_list(vals['sentence_levels'], 'int'),
            'speakers': helper_funcs.string_to_list(vals['sentence_speakers'], 'int'),
            'repetitions': vals['repetitions'],
            'randomize': vals['randomize'],
            'write': True
        }

        # Create and write matrix CSV file
        mf = models.CreateSpeechTaskerMatrix(**pars)
        mf.create_matrix_file()

    ###########################
    # Settings View Functions #
    ###########################
    def _load_settings(self):
        """ Load parameters into self.settings dict. """
        # Variable types
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create runtime dict from settingsmodel fields
        self.settings = dict()
        for key, data in self.settings_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])
        logger.info("Loaded settings model fields into " +
            "running settings dict")


    def _save_settings(self, *_):
        """ Save current runtime parameters to file. """
        logger.info("Calling settings model set and save funcs")
        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
            self.settings_model.save()

    ########################
    # Tools Menu Functions #
    ########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog. """
        logger.info("Calling audio device window")
        tkgui.views.AudioView(self, self.settings)


    def _show_calibration_dialog(self):
        """ Display the calibration dialog window. """
        logger.info("Calling calibration window")
        tkgui.views.CalibrationView(self, self.settings)

    ################################
    # Calibration Dialog Functions #
    ################################
    def play_calibration_file(self):
        """ Load calibration file and present. """
        logger.info("Play calibration file called")
        # Get calibration file
        try:
            self.calibration_model.get_cal_file()
        except AttributeError:
            logger.exception("Cannot find internal calibration file!")
            messagebox.showerror(
                title="File Not Found",
                message="Cannot find internal calibration file!",
                detail="Please use a custom calibration file."
            )
        # Present calibration signal
        self.present_audio(
            audio=Path(self.calibration_model.cal_file), 
            pres_level=self.settings['cal_level_dB'].get()
        )


    def _calc_offset(self):
        """ Calculate offset based on SLM reading. """
        # Calculate new presentation level
        self.calibration_model.calc_offset()
        # Save level - this must be called here!
        self._save_settings()


    def _calc_level(self, desired_spl):
        """ Calculate new dB FS level using slm_offset. """
        # Calculate new presentation level
        self.calibration_model.calc_level(desired_spl)
        # Save level - this must be called here!
        self._save_settings()

    #######################
    # Help Menu Functions #
    #######################
    def _show_help(self):
        """ Create html help file and display in default browser. """
        logger.info("Calling README file (will open in browser)")
        # Read markdown file and convert to html
        with open(app_assets.README.README_MD, 'r') as f:
            text = f.read()
            html = markdown.markdown(text)

        # Create html file for display
        with open(app_assets.README.README_HTML, 'w') as f:
            f.write(html)

        # Open README in default web browser
        webbrowser.open(app_assets.README.README_HTML)


    def _show_changelog(self):
        """ Create html CHANGELOG file and display in default browser. """
        logger.info("Calling CHANGELOG file (will open in browser)")
        # Read markdown file and convert to html
        with open(app_assets.CHANGELOG.CHANGELOG_MD, 'r') as f:
            text = f.read()
            html = markdown.markdown(text)

        # Create html file for display
        with open(app_assets.CHANGELOG.CHANGELOG_HTML, 'w') as f:
            f.write(html)

        # Open CHANGELOG in default web browser
        webbrowser.open(app_assets.CHANGELOG.CHANGELOG_HTML)

    ###################
    # Audio Functions #
    ###################
    def _create_audio_object(self, audio, **kwargs):
        # Create audio object
        try:
            self.a = tmpy.audio_handlers.AudioPlayer(
                audio=audio,
                **kwargs
            )
        except FileNotFoundError:
            logger.exception("Cannot find audio file!")
            messagebox.showerror(
                title="File Not Found",
                message="Cannot find the audio file!",
                detail="Go to File>Session to specify a valid audio path."
            )
            #self._show_settings_view()
            return
        except tmpy.audio_handlers.InvalidAudioType:
            raise
        except tmpy.audio_handlers.MissingSamplingRate:
            raise


    # def _format_routing(self, routing):
    #     """ Convert space-separated string to list of ints
    #         for speaker routing.
    #     """
    #     logger.info("Formatting channel routing string as list")
    #     routing = routing.split()
    #     routing = [int(x) for x in routing]
    #     return routing


    def _format_routing(self, routing):
        """ Convert string of ", " separated items to list of ints 
        for speaker routing.
        """
        logger.info("Formatting channel routing")
        return helper_funcs.string_to_list(routing, 'int')
    

    def _play(self, pres_level):
        """ Format channel routing, present audio and catch exceptions. """
        # Get routing either from a trial handler or settings
        try:
            routing=[self.th.trial_info['speaker']]
        except AttributeError:
            routing = helper_funcs.string_to_list(
                self.settings['channel_routing'].get(), 'int')
            
        # Attempt to present audio
        try:
            self.a.play(
                level=pres_level,
                device_id=self.settings['audio_device'].get(),
                routing=routing
            )
        except tmpy.audio_handlers.InvalidAudioDevice as e:
            logger.error("Invalid audio device: %s", e)
            messagebox.showerror(
                title="Invalid Device",
                message="Invalid audio device! Go to Tools>Audio Settings " +
                    "to select a valid audio device.",
                detail = e
            )
            # Open Audio Settings window
            self._show_audio_dialog()
        except tmpy.audio_handlers.InvalidRouting as e:
            logger.error("Invalid routing: %s", e)
            messagebox.showerror(
                title="Invalid Routing",
                message="Speaker routing must correspond with the " +
                    "number of channels in the audio file! Go to " +
                    "Tools>Audio Settings to update the routing.",
                detail=e
            )
            # Open Audio Settings window
            self._show_audio_dialog()
        except tmpy.audio_handlers.Clipping:
            logger.error("Clipping has occurred - aborting!")
            messagebox.showerror(
                title="Clipping",
                message="The level is too high and caused clipping.",
                detail="The waveform will be plotted when this message is " +
                    "closed for visual inspection."
            )
            self.a.plot_waveform("Clipped Waveform")


    def present_audio(self, audio, pres_level, **kwargs):
        # Load audio
        try:
            self._create_audio_object(audio, **kwargs)
        except tmpy.audio_handlers.InvalidAudioType as e:
            logger.error("Invalid audio format: %s", e)
            messagebox.showerror(
                title="Invalid Audio Type",
                message="The audio type is invalid!",
                detail=f"{e} Please provide a Path or ndarray object."
            )
            return
        except tmpy.audio_handlers.MissingSamplingRate as e:
            logger.error("Missing sampling rate: %s", e)
            messagebox.showerror(
                title="Missing Sampling Rate",
                message="No sampling rate was provided!",
                detail=f"{e} Please provide a Path or ndarray object."
            )
            return

        # Play audio
        self._play(pres_level)


    def stop_audio(self):
        """ Stop audio playback. """
        logger.info("User stopped audio playback")
        try:
            self.a.stop()
        except AttributeError:
            logger.info("Stop called, but there is no audio object!")

################
# Module Guard #
################
if __name__ == "__main__":
    app = Application()
    app.mainloop()
