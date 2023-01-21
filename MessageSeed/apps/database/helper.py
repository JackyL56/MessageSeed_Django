from django.db import models
####################################################################################
#######                        HELPER FUNCTIONS                            #########
####################################################################################
def get_level_with_exp(exp):
    """ Function to convert experience to the according level. """
    if exp <= 0:
        return 1
    return 1 + (1.5 / 11) * pow(exp + 1, .51)


def get_exp_with_level(level):
    """ Function to convert level to experience. """
    xp = 49.7358406536 * pow(max(0, level-1), 1.960784431373)
    return max(0, xp)


class Helper:
    EXPERIENCE_CREATED_MESSAGE = 20
    EXPERIENCE_I_LIKE = 10
    EXPERIENCE_GOT_LIKED = 50
    EXPERIENCE_EVOLVED_TO_SAPLING = 200
    EXPERIENCE_EVOLVED_TO_TREE = 1000

    DEFAULT_LIFETIME = 2  # In Days
    ADDED_LIFE_PER_LIKE = 12  # Hours

    SEEDLING = 0
    SAPLING = 1
    TREE = 2
    DEAD = 3

    MESSAGE_STATE = {
        (SEEDLING, 'Seedling'),
        (SAPLING, 'Sapling'),
        (TREE, 'Tree'),
        (DEAD, 'Dead'),
    }

    STATE_EVOLVE_THRESHOLD = {
        0: 1,
        1: 21,
        2: 9999,
        3: 9999
    }
