import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from relay_interfaces.msg import Turn

from . import layout
from .config import member_of, TOTAL_NUMBERS, TURN_TOPIC
from .turtle_driver import TurtleDriver


class BaseMember(Node):

    def __init__(self, member_id, pen_rgb, pen_width=3):
        super().__init__(f'member_{member_id}')
        self.member_id = member_id
        self.pen_rgb = pen_rgb
        self.pen_width = pen_width

        self._ready = False
        self._last_number = 0
        self._pending_turn = None

        self.driver = TurtleDriver(self)

        qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self._turn_pub = self.create_publisher(Turn, TURN_TOPIC, qos)
        self.create_subscription(Turn, TURN_TOPIC, self._on_turn, qos)

        self._ready_timer = self.create_timer(0.2, self._check_ready)

    def on_ready(self):
        pass

    def before_draw(self, number, proceed):
        proceed()

    def on_last_number(self, number):
        self.get_logger().warn(
            f'Angka terakhir {number} selesai, tetapi on_last_number '
            f'belum diimplementasikan di member_{self.member_id}.')

    def publish_turn(self, number):
        msg = Turn()
        msg.current_number = number
        msg.active_member = member_of(number)
        msg.finished = False
        self._turn_pub.publish(msg)

    def publish_finished(self, last_number):
        msg = Turn()
        msg.current_number = last_number
        msg.active_member = 0
        msg.finished = True
        self._turn_pub.publish(msg)

    def pass_turn(self, number):
        if number >= TOTAL_NUMBERS:
            self.on_last_number(number)
            return
        self.get_logger().info(
            f'Angka {number} selesai -> giliran member_{member_of(number + 1)}')
        self.publish_turn(number + 1)

    def _check_ready(self):
        if not self.driver.ready():
            return
        self._ready_timer.cancel()
        self._ready = True
        self.get_logger().info('Turtlesim siap, menunggu giliran.')
        self.on_ready()
        if self._pending_turn is not None:
            msg, self._pending_turn = self._pending_turn, None
            self._on_turn(msg)

    def _on_turn(self, msg):
        if msg.finished:
            self.get_logger().info('Relay selesai, node idle.')
            return
        if msg.active_member != self.member_id:
            return
        if msg.current_number <= self._last_number:
            return
        if not self._ready:
            self._pending_turn = msg
            return

        number = msg.current_number
        self._last_number = number
        self.get_logger().info(f'Giliran saya: menggambar angka {number}')
        self.before_draw(number, lambda: self._draw(number))

    def _draw(self, number):
        strokes = layout.strokes_for_number(number, self.member_id)
        self.driver.draw_polylines(
            strokes, self.pen_rgb, self.pen_width,
            on_done=lambda: self.pass_turn(number))


def run_member(member_cls, args=None):
    rclpy.init(args=args)
    node = member_cls()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
