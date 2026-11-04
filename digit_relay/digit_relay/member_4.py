"""Anggota 4."""
from .common.base_member import BaseMember, run_member


class Member4(BaseMember):
    def __init__(self):
        super().__init__(member_id=4, pen_rgb=(0, 220, 90), pen_width=3)


def main(args=None):
    run_member(Member4, args)


if __name__ == '__main__':
    main()
