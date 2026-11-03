"""Konstanta bersama untuk seluruh node"""

NUM_MEMBERS = 6
CYCLES = 2
TOTAL_NUMBERS = NUM_MEMBERS * CYCLES

TURN_TOPIC = '/relay/turn'

SET_PEN_SERVICE = '/turtle1/set_pen'
TELEPORT_SERVICE = '/turtle1/teleport_absolute'
CLEAR_SERVICE = '/clear'
POSE_TOPIC = '/turtle1/pose'

CANVAS_SIZE = 11.0


def member_of(number):
    """Anggota yang bertugas menggambar `number`"""
    return (number - 1) % NUM_MEMBERS + 1
