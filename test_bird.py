import unittest
from unittest.mock import Mock, patch

import bird


class BirdTest(unittest.TestCase):
    def setUp(self):
        bird.Bird.image = None
        self.image = Mock()
        self.loader = patch.object(bird, 'load_image', return_value=self.image)
        self.loader.start()
        self.addCleanup(self.loader.stop)

    def test_all_fourteen_frames_stay_inside_sheet(self):
        rects = [bird.Bird.frame_rect(i) for i in range(14)]
        self.assertEqual(len(set(rects)), 14)
        for x, y, width, height in rects:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + width, bird.SHEET_WIDTH)
            self.assertLessEqual(y + height, bird.SHEET_HEIGHT)
        self.assertEqual(bird.Bird.frame_rect(14), rects[0])

    def test_images_are_shared(self):
        first, second = bird.Bird(100, 200), bird.Bird(200, 200)
        self.assertIs(first.image, second.image)
        bird.load_image.assert_called_once_with('bird_animation.png')

    def test_frame_uses_distance_based_fps(self):
        one = bird.Bird(100, 200)
        with patch.object(bird, 'get_canvas_width', return_value=1600), patch.object(bird.game_framework, 'frame_time', bird.WINGBEAT_SECONDS / 2):
            one.update()
        self.assertAlmostEqual(one.frame, 7.0)
        self.assertAlmostEqual(bird.ANIMATION_FPS, 14 * (7 * 1000 / 3600) / 0.8)

    def test_bounces_at_both_edges(self):
        one = bird.Bird(1549, 200)
        with patch.object(bird, 'get_canvas_width', return_value=1600), patch.object(bird.game_framework, 'frame_time', 1.0):
            one.update()
            self.assertEqual(one.direction, -1)
            self.assertGreaterEqual(one.x, 50)
            self.assertLessEqual(one.x, 1550)
            one.x = 51
            one.update()
            self.assertEqual(one.direction, 1)
            self.assertGreaterEqual(one.x, 50)

    def test_draw_flips_only_when_flying_left(self):
        one = bird.Bird(100, 200)
        one.direction = -1
        one.draw()
        self.assertEqual(self.image.clip_composite_draw.call_args.args[5], 'h')
        one.direction = 1
        one.draw()
        self.assertEqual(self.image.clip_composite_draw.call_args.args[5], '')


if __name__ == '__main__':
    unittest.main()
