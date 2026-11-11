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
