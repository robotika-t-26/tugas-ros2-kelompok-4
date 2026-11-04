"""ryan"""
from .common.base_member import BaseMember, run_member


class Member2(BaseMember):
    def __init__(self):
        super().__init__(member_id=2, pen_rgb=(255, 150, 0), pen_width=3)


def main(args=None):
    run_member(Member2, args)


if __name__ == '__main__':
    main()
