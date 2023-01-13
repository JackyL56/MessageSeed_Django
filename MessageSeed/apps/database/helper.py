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
