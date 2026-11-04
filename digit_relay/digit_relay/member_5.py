from .common.base_member import BaseMember, run_member


class Member5(BaseMember):
    def __init__(self):
        super().__init__(member_id=5, pen_rgb=(255, 255, 255), pen_width=3)


def main(args=None):
    run_member(Member5, args)


if __name__ == '__main__':
    main()
