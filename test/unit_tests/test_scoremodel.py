""" Automated tests for the ScoreModel of the automated HINT. 

    Written by: Travis M. Moore
    Last edited: May 10, 2024
"""

###########
# Imports #
###########
# Standard library
import pytest
import sys

# Custom
sys.path.append("..")
from models.scoremodel import ScoreModel

############
# Fixtures #
############
@pytest.fixture
def scoremodel():
    return ScoreModel()

##############
# Unit Tests #
##############
def test__init(scoremodel):
    # Assert
    assert scoremodel.outcome == None

################
# Module Guard #
################
if __name__ == '__main__':
    pass
