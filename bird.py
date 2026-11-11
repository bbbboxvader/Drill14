"""새 스프라이트와 반복 비행."""
from pico2d import get_canvas_width, load_image
import game_framework

SHEET_WIDTH = 918
SHEET_HEIGHT = 506
SHEET_COLUMNS = 5
SHEET_ROWS = 3
FRAME_COUNT = 14

# 화면의 거리 축척은 기존 소년과 동일하다.
PIXEL_PER_METER = 10.0 / 0.3
FLIGHT_SPEED_KMPH = 7.0
FLIGHT_SPEED_MPS = FLIGHT_SPEED_KMPH * 1000.0 / 3600.0
FLIGHT_SPEED_PPS = FLIGHT_SPEED_MPS * PIXEL_PER_METER

# 가정: 새가 0.8m 이동할 때 날갯짓 1회(14프레임)를 재생한다.
DISTANCE_PER_WINGBEAT_M = 0.8
WINGBEAT_SECONDS = DISTANCE_PER_WINGBEAT_M / FLIGHT_SPEED_MPS
ANIMATION_FPS = FRAME_COUNT / WINGBEAT_SECONDS

DRAW_WIDTH = 100
DRAW_HEIGHT = 92

class Bird:
    image = None

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.direction = 1
        self.frame = 0.0
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

    @staticmethod
    def frame_rect(frame):
        index = int(frame) % FRAME_COUNT
        row, column = divmod(index, SHEET_COLUMNS)
        left = column * SHEET_WIDTH // SHEET_COLUMNS
        right = (column + 1) * SHEET_WIDTH // SHEET_COLUMNS
        top = SHEET_HEIGHT - row * SHEET_HEIGHT // SHEET_ROWS
        bottom = SHEET_HEIGHT - (row + 1) * SHEET_HEIGHT // SHEET_ROWS
        return left, bottom, right - left, top - bottom

    def draw(self):
        left, bottom, width, height = self.frame_rect(self.frame)
        self.image.clip_composite_draw(
            left, bottom, width, height, 0, '',
            self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT)
