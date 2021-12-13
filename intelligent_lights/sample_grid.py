from intelligent_lights.cells.device import Device
from intelligent_lights.cells.empty import Empty
from intelligent_lights.cells.wall import Wall
from intelligent_lights.light import Light

_grid = """
####################################################################################################
#                                          ##                                                      #
#      D                             D     ##     D                                         D      #
#                                          ##                                                      #
#                                    D     ##                                                      #
#                                          ##                                                      #
#                                          ##     D                                         D      #
#      D                             D     ##                                                      #
#                                          ##                                                      #
#                                          ##                                                      #
#                                    D     ##     D                                       D        #
#                                          ##                                                      #
#      D                                   ##                                                      #
#                                    D     ##                                                      #
#                                          ##                                             D        #
#                                          ##     D                                                #
#      D                              D    ##                                                      #
#                                          ##                                                      #
#                                          ##                                                      #
#      D                             D     ##     D                                        D       #
#                                          ##                                                      #
#################     #############################################    #############################
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
#                                                                                                  #
########################################                 ###########################################
##                                    ##                 ##                                        #
##                                    ##                 ##    D                            D      #
##        D                           ##                 ##                                        #
##                              D     ##                 ##                                        #
##                                    ##                 ##                                        #
##                                    ##                 ##                                D       #
##                                    ##                 ##                                        #
##                                                                                                 #
##                                                                                                 #
##      D                                                                                          #
##                                    ##                 ##                               D        #
##                                    ##                 ##                                        #
##                              D     ##                 ##   D                                    #
##      D                             ##                 ##                                        #
##                                    ##                 ##                                        #
##                                    ##                 ##                                        #
##       D                      D     ##                 ##   D                             D      #
##                                    ##                 ##                                        #
#############################################     ##################################################
"""

SAMPLE_GRID = []
for line in filter(None, _grid.strip().split('\n')):
    line2 = []
    for c in line:
        if c == '#':
            line2.append(Wall())
        elif c == "D":
            line2.append(Device())
        elif c == " ":
            line2.append(Empty())
    SAMPLE_GRID.append(line2)


SAMPLE_LIGHTS = [
    Light(22, 4),
    Light(22, 12),
    Light(70, 4),
    Light(22, 12),
    Light(20, 26),
    Light(70, 26),
    Light(47, 40),
    Light(18, 40),
    Light(77, 40),
]

SAMPLE_PERSONS = [
    (20, 20),
    (70, 20),
    (22, 40),
    (50, 30),
    (90, 40),
]
