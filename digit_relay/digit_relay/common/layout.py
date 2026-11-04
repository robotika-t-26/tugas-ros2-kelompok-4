"""

    +-----------+-----------+-----------+
    | Slot 1    | Slot 2    | Slot 3    |   
    +-----------+-----------+-----------+
    | Slot 4    | Slot 5    | Slot 6    |   
    +-----------+-----------+-----------+

"""
from .config import CANVAS_SIZE, NUM_MEMBERS
from .glyphs import digit_strokes

MARGIN = 0.5      # jarak aman dari dinding kanvas
COLUMNS = 3
ROWS = (NUM_MEMBERS + COLUMNS - 1) // COLUMNS

DIGIT_W = 1.3     
DIGIT_H = 3.0     
DIGIT_GAP = 0.4   


def slot_bounds(member_id):
    """(x_min, y_min, x_max, y_max) slot milik `member_id`."""
    if not 1 <= member_id <= NUM_MEMBERS:
        raise ValueError(f'member_id harus 1..{NUM_MEMBERS}, dapat {member_id}')
    row = (member_id - 1) // COLUMNS
    col = (member_id - 1) % COLUMNS
    slot_w = (CANVAS_SIZE - 2 * MARGIN) / COLUMNS
    slot_h = (CANVAS_SIZE - 2 * MARGIN) / ROWS
    x_min = MARGIN + col * slot_w
    y_max = CANVAS_SIZE - MARGIN - row * slot_h
    return x_min, y_max - slot_h, x_min + slot_w, y_max


def slot_center(member_id):
    x_min, y_min, x_max, y_max = slot_bounds(member_id)
    return (x_min + x_max) / 2, (y_min + y_max) / 2


def digit_boxes(number, member_id):
    """Kotak tiap digit: daftar (char, x0, y0, x1, y1) dalam koordinat kanvas."""
    text = str(number)
    cx, cy = slot_center(member_id)
    total_w = len(text) * DIGIT_W + (len(text) - 1) * DIGIT_GAP
    x = cx - total_w / 2
    y = cy - DIGIT_H / 2
    boxes = []
    for char in text:
        boxes.append((char, x, y, x + DIGIT_W, y + DIGIT_H))
        x += DIGIT_W + DIGIT_GAP
    return boxes


def strokes_for_number(number, member_id):
    """Semua goresan (polyline) untuk menggambar `number` di slot `member_id`."""
    strokes = []
    for char, x0, y0, x1, y1 in digit_boxes(number, member_id):
        strokes.extend(digit_strokes(char, x0, y0, x1 - x0, y1 - y0))
    return strokes
