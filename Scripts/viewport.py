import pygame

def check_if_out_of_area(viewport, maxcornerx, mincornerx, maxcornery, mincornery):
    result_list = [False, False, False, False]
    if viewport.pos_x > maxcornerx:
        result_list[0] = True
    else:
        result_list[0] = False
    if viewport.pos_x < mincornerx:
        result_list[1] = True
    else:
        result_list[1] = False
    if viewport.pos_y < maxcornery:
        result_list[2] = True
    else:
        result_list[2] = False
    if viewport.pos_y < mincornery:
        result_list[3] = True
    else:
        result_list[3] = False

    return result_list


class ViewPort:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
