"""Anggota 6: menutup relay setelah angka terakhir (2N) digambar."""
from .common.base_member import BaseMember, run_member


class Member6(BaseMember):
    def __init__(self):
        super().__init__(member_id=6, pen_rgb=(255, 80, 220), pen_width=3)

    def on_last_number(self, number):
        # Angka 2N selesai: umumkan relay selesai. Semua node kembali idle,
        # turtlesim tetap hidup sehingga hasil gambar masih bisa dilihat.
        self.get_logger().info(
            f'Angka terakhir ({number}) selesai. Relay berakhir.')
        self.publish_finished(number)


def main(args=None):
    run_member(Member6, args)


if __name__ == '__main__':
    main()
