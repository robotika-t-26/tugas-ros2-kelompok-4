"""Bentuk angka 0-9 untuk digambar turtle.

Setiap angka digambar dalam kotak 1 x 1, dengan (0, 0) di kiri bawah.
Satu angka terdiri dari satu atau beberapa goresan. Satu goresan adalah
deretan titik yang disambung tanpa mengangkat pena.
"""

GLYPHS = {
    '0': [
        [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
    ],
    '1': [
        [(0.15, 0.75), (0.55, 1), (0.55, 0)],
    ],
    '2': [
        [(0, 1), (1, 1), (1, 0.5), (0, 0.5), (0, 0), (1, 0)],
    ],
    '3': [
        [(0, 1), (1, 1), (1, 0), (0, 0)],
        [(0, 0.5), (1, 0.5)],
    ],
    '4': [
        [(0, 1), (0, 0.5), (1, 0.5)],
        [(1, 1), (1, 0)],
    ],
    '5': [
        [(1, 1), (0, 1), (0, 0.5), (1, 0.5), (1, 0), (0, 0)],
    ],
    '6': [
        [(1, 1), (0, 1), (0, 0), (1, 0), (1, 0.5), (0, 0.5)],
    ],
    '7': [
        [(0, 1), (1, 1), (0.4, 0)],
    ],
    '8': [
        [(0, 0.5), (1, 0.5), (1, 1), (0, 1), (0, 0.5),
         (0, 0), (1, 0), (1, 0.5)],
    ],
    '9': [
        [(1, 0.5), (0, 0.5), (0, 1), (1, 1), (1, 0), (0, 0)],
    ],
}


def digit_strokes(char, x0, y0, width, height):
    """Ubah goresan angka ke koordinat kanvas.

    (x0, y0) adalah pojok kiri bawah angka di kanvas.
    """
    strokes = []
    for stroke in GLYPHS[char]:
        strokes.append([(x0 + px * width, y0 + py * height) for px, py in stroke])
    return strokes
