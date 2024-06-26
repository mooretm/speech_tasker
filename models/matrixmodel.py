""" Classes for handling matrix files for specific apps. 

    Written by: Travis M. Moore
    Last edited: June 24, 2024
"""

###########
# Imports #
###########
# Standard library
import logging
import os
import sys

# Add custom path
try:
    sys.path.append(os.environ['TMPY'])
except KeyError:
    sys.path.append('C:\\Users\\MooTra\\Code\\Python')

# Custom
from tmpy.handlers import MatrixFile

##########
# Logger #
##########
# Create new logger
logger = logging.getLogger(__name__)

############################
# ImportSpeechTaskerMatrix #
############################
class ImportSpeechTaskerMatrix(MatrixFile):
    """ Import a matrix file for use during session. """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def import_matrix_file(self):
        """ Import matrix file. """
        try:
            # Import matrix file
            matrix_df = self.import_file(self.kwargs['filepath'])
            # Repeat trials
            repeated = self.repeat_trials(matrix_df, self.kwargs['presentations'])
            # Randomize trials
            if self.kwargs['randomize'] == 1:
                randomized = self.randomize(repeated)
                if self.kwargs['write'] == 1:
                    randomized.to_csv("matrix_file.csv", index=False)
                return randomized
            else:
                if self.kwargs['write'] == 1:
                    repeated.to_csv("matrix_file.csv", index=False)
                return repeated
        except TypeError as e:
            logger.error(e)

############################
# CreateSpeechTaskerMatrix #
############################
class CreateSpeechTaskerMatrix(MatrixFile):
    """ Create a matrix file from the Speech Tasker. """

    def __init__(self, **kwargs):
        """ Expects a dictionary of arguments. """
        self.kwargs = kwargs

    def create_matrix_file(self):
        """ Create the final matrix file dataframe. """
        try:
            # Import speech task stimuli
            stimulus_file = self.import_file(self.kwargs['filepath'])
            # Grab only selected lists
            subset = self.subset_lists(stimulus_file, self.kwargs['lists'])
            # Grab only n sentences per list
            truncated = self.truncate_lists(subset, self.kwargs['sentences_per_list'])
            # Add level column
            added_levels = self.assign_values(truncated, self.kwargs['levels'], 'level')
            # Add speaker column
            added_speakers = self.assign_values(added_levels, self.kwargs['speakers'], 'speaker')
            # Repeat trials
            repeated = self.repeat_trials(added_speakers, self.kwargs['presentations'])
            # Randomize trials
            if self.kwargs['randomize'] == 1:
                randomized = self.randomize(repeated)
                if self.kwargs['write'] == True:
                    randomized.to_csv("matrix_file.csv", index=False)
                return randomized
            else:
                if self.kwargs['write'] == True:
                    repeated.to_csv("matrix_file.csv", index=False)
                return repeated
        except TypeError as e:
            logger.error(e)

################
# Module Guard #
################
if __name__ == "__main__":
    pass
    # _path = r'C:\Users\MooTra\Code\Python\automated_hint\stimuli\sentences\matrix_HINT.csv'
    # pars = {
    #     'filepath': _path,
    #     'lists': [2, 7],
    #     'sentences_per_list': 7,
    #     'levels': [60, 70],
    #     'speakers': [3, 6],
    #     'repetitions': 3,
    #     'randomize': 1,
    #     'write': True
    # }

    # mf = CreateSpeechTaskerMatrix(**pars)
    # mfile = mf.create_matrix_file()
    # print(mfile)
