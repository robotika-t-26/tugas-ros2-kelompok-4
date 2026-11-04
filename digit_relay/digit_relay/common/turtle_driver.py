"""Helper untuk menggerakkan turtle di turtlesim tanpa memblokir executor.

Perintah dijalankan berurutan oleh sebuah timer:
  - ('pen', r, g, b, width, off)   -> panggil /turtle1/set_pen
  - ('goto', x, y, step)           -> teleport bertahap (step per tick) ke (x, y)

Setelah tiap teleport, driver menunggu /turtle1/pose benar-benar mencapai
titik tujuan. Ini memastikan turtlesim sudah memproses teleport (dan menggambar
garisnya) sebelum status pena diubah oleh perintah berikutnya.
"""
import math
from collections import deque

from std_srvs.srv import Empty
from turtlesim.msg import Pose
from turtlesim.srv import SetPen, TeleportAbsolute

from .config import (CLEAR_SERVICE, POSE_TOPIC, SET_PEN_SERVICE,
                     TELEPORT_SERVICE)


class TurtleDriver:
    def __init__(self, node, tick=0.02, draw_step=0.08, travel_step=0.4,
                 tolerance=0.02):
        self._node = node
        self._tick = tick
        self.draw_step = draw_step      # jarak per tick saat menggambar
        self.travel_step = travel_step  # jarak per tick saat pindah slot
        self._tol = tolerance

        self._pose = None
        self._pen_client = node.create_client(SetPen, SET_PEN_SERVICE)
        self._teleport_client = node.create_client(
            TeleportAbsolute, TELEPORT_SERVICE)
        self._clear_client = node.create_client(Empty, CLEAR_SERVICE)
        node.create_subscription(Pose, POSE_TOPIC, self._on_pose, 10)

        self._queue = deque()
        self._on_done = None
        self._running = False
        self._pending = None      # future service yang sedang ditunggu
        self._await_pose = None   # (x, y) yang harus dicapai pose
        self._goto = None         # (tx, ty, step) yang sedang berjalan
        self._timer = node.create_timer(tick, self._on_tick)

    # ---------------------------------------------------------- status
    def ready(self):
        """True jika service turtlesim tersedia dan pose pertama sudah diterima."""
        return (self._pen_client.service_is_ready()
                and self._teleport_client.service_is_ready()
                and self._clear_client.service_is_ready()
                and self._pose is not None)

    def _on_pose(self, msg):
        self._pose = (msg.x, msg.y)

    # ---------------------------------------------------------- API publik
    def clear(self, on_done):
        """Panggil /clear lalu jalankan `on_done()`."""
        future = self._clear_client.call_async(Empty.Request())
        future.add_done_callback(lambda _f: on_done())

    def draw_polylines(self, polylines, rgb, width, on_done):
        """Gambar semua polyline: pena naik saat pindah, turun saat menggambar."""
        r, g, b = rgb
        commands = []
        for line in polylines:
            commands.append(('pen', r, g, b, width, 1))
            commands.append(('goto', line[0][0], line[0][1], self.travel_step))
            commands.append(('pen', r, g, b, width, 0))
            for x, y in line[1:]:
                commands.append(('goto', x, y, self.draw_step))
        commands.append(('pen', r, g, b, width, 1))
        self.run(commands, on_done)

    def run(self, commands, on_done):
        if self._running:
            raise RuntimeError('TurtleDriver masih menjalankan perintah')
        self._queue = deque(commands)
        self._on_done = on_done
        self._running = True

    # ---------------------------------------------------------- mesin status
    def _on_tick(self):
        if not self._running:
            return

        if self._pending is not None:
            if not self._pending.done():
                return
            if self._pending.exception() is not None:
                self._node.get_logger().error(
                    f'Service gagal: {self._pending.exception()}')
            self._pending = None

        if self._await_pose is not None:
            if not self._reached(self._await_pose):
                return
            self._await_pose = None

        if self._goto is not None:
            self._step_goto()
            return

        if not self._queue:
            self._running = False
            on_done, self._on_done = self._on_done, None
            if on_done is not None:
                on_done()
            return

        cmd = self._queue.popleft()
        if cmd[0] == 'pen':
            self._send_pen(*cmd[1:])
        elif cmd[0] == 'goto':
            self._goto = (cmd[1], cmd[2], cmd[3])
            self._step_goto()

    def _reached(self, target):
        if self._pose is None:
            return False
        return math.hypot(self._pose[0] - target[0],
                          self._pose[1] - target[1]) <= self._tol

    def _send_pen(self, r, g, b, width, off):
        req = SetPen.Request()
        req.r, req.g, req.b = int(r), int(g), int(b)
        req.width = int(width)
        req.off = int(off)
        self._pending = self._pen_client.call_async(req)

    def _step_goto(self):
        tx, ty, step = self._goto
        x, y = self._pose
        dx, dy = tx - x, ty - y
        dist = math.hypot(dx, dy)
        if dist <= self._tol:
            self._goto = None
            return
        if dist <= step:
            nx, ny = tx, ty
        else:
            nx, ny = x + dx / dist * step, y + dy / dist * step

        req = TeleportAbsolute.Request()
        req.x, req.y = float(nx), float(ny)
        req.theta = float(math.atan2(dy, dx))
        self._pending = self._teleport_client.call_async(req)
        self._await_pose = (nx, ny)
