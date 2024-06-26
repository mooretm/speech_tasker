""" Settings variables for Speech Tasker. """

# Define dictionary items
fields = {
    # Session variables
    'Subject': {'type': 'str', 'value': '999'},
    'Condition': {'type': 'str', 'value': "test"},
    
    # Stimulus variables
    'Randomize': {'type': 'int', 'value': 0},
    'Presentations': {'type': 'int', 'value': 1},
    'Sentence Lists': {'type': 'str', 'value': '1, 2'},
    'Sentences per List': {'type': 'int', 'value': 5},
    'import_audio_path': {'type': 'str', 'value': "Please select a path"},
    'matrix_file_path': {'type': 'str', 'value': "Please select a path"},
    'sentence_file_path': {'type': 'str', 'value': 'Please select a file'},
    'write_matrix': {'type': 'int', 'value': 0},

    # Presentation variables
    'Sentence Levels': {'type': 'str', 'value': '70, 75'},
    'Noise Level': {'type': 'float', 'value': 65},
    'Sentence Speakers': {'type': 'str', 'value': '1, 2, 3'},
    
    # Internal level variables
    'adjusted_level_dB': {'type': 'float', 'value': -25.0},
    'desired_level_dB': {'type': 'float', 'value': 65},

    # Audio device variables
    'audio_device': {'type': 'int', 'value': 999},
    'channel_routing': {'type': 'str', 'value': '1'},

    # Calibration variables
    'cal_file': {'type': 'str', 'value': 'cal_stim.wav'},
    'cal_level_dB': {'type': 'float', 'value': -30.0},
    'slm_reading': {'type': 'float', 'value': 70.0},
    'slm_offset': {'type': 'float', 'value': 100.0},

    # Version control variables
    'check_for_updates': {'type': 'str', 'value': 'yes'},
    'version_lib_path': {'type': 'str', 'value': r'\\starfile\Public\Temp\MooreT\Personal Files\admin\versions.xlsx'},
}
