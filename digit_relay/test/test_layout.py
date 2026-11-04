"""Tes tata letak dan glyph. Tidak butuh ROS: hanya Python murni."""
from itertools import combinations

from digit_relay.common import config, glyphs, layout

EDGE = 0.2  # jarak minimum goresan dari dinding kanvas


def _boxes_overlap(a, b):
    return not (a[3] <= b[1] or b[3] <= a[1] or a[2] <= b[0] or b[2] <= a[0])


def test_all_digits_defined_and_normalized():
    for char in '0123456789':
        assert char in glyphs.GLYPHS
        for stroke in glyphs.GLYPHS[char]:
            assert len(stroke) >= 2
            for x, y in stroke:
                assert 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0


def test_member_of_cycles():
    assert [config.member_of(n) for n in range(1, config.TOTAL_NUMBERS + 1)] == \
        list(range(1, config.NUM_MEMBERS + 1)) * config.CYCLES


def test_strokes_inside_canvas():
    for number in range(1, config.TOTAL_NUMBERS + 1):
        member = config.member_of(number)
        for stroke in layout.strokes_for_number(number, member):
            for x, y in stroke:
                assert EDGE <= x <= config.CANVAS_SIZE - EDGE
                assert EDGE <= y <= config.CANVAS_SIZE - EDGE


def test_numbers_stay_inside_own_slot():
    for number in range(1, config.TOTAL_NUMBERS + 1):
        member = config.member_of(number)
        sx0, sy0, sx1, sy1 = layout.slot_bounds(member)
        for _, x0, y0, x1, y1 in layout.digit_boxes(number, member):
            assert sx0 <= x0 and x1 <= sx1
            assert sy0 <= y0 and y1 <= sy1


def test_no_overlap_within_a_cycle():
    for cycle in range(config.CYCLES):
        boxes = []
        for i in range(1, config.NUM_MEMBERS + 1):
            number = cycle * config.NUM_MEMBERS + i
            for _, x0, y0, x1, y1 in layout.digit_boxes(number, i):
                boxes.append((x0, y0, x1, y1))
        for a, b in combinations(boxes, 2):
            assert not _boxes_overlap(a, b)
