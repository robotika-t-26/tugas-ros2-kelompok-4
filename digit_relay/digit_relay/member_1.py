from .common.base_member import BaseMember, run_member
from .common.config import NUM_MEMBERS


class Member1(BaseMember):
    def __init__(self):
        super().__init__(member_id=1, pen_rgb=(255, 70, 70), pen_width=3)

    def on_ready(self):
        # buat angka 1
        self.get_logger().info('Memulai relay dengan angka 1.')
        self.publish_turn(1)

    def before_draw(self, number, proceed):
        # Awal siklus berikutnya (angka N+1, 2N+1, ...): bersihkan kanvas dulu.
        if number > 1 and (number - 1) % NUM_MEMBERS == 0:
            self.get_logger().info('Awal siklus baru: memanggil /clear.')
            self.driver.clear(on_done=proceed)
        else:
            proceed()


def main(args=None):
    run_member(Member1, args)


if __name__ == '__main__':
    main()