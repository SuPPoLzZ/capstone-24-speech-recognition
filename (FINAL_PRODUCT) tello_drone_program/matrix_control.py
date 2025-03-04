# matrix_control.py

from djitellopy import tello


def update_matrix(display_pattern):
    tello.set_matrix_pattern(display_pattern)
