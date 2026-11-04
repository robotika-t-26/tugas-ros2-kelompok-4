"""Anggota 3."""
from .common.base_member import BaseMember, run_member


class Member3(BaseMember):
    def __init__(self):
        super().__init__(member_id=3, pen_rgb=(255, 230, 0), pen_width=3)


def main(args=None):
    run_member(Member3, args)


if __name__ == '__main__':
    main()
