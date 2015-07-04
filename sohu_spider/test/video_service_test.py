# coding=utf-8
__author__ = 'cafedeflore'

"""
This module is the test class
"""
import log
import logging
import unittest
from engine import video_service

class VideoServiceTest(unittest.TestCase):
    """
    Test UrlPars
    """
    def test_get_video(self):
        s = video_service.VideoService()
        print s.get_video('1')

    def test_add_or_update_video(self):
        s = video_service.VideoService()
        video = s.get_video('1')
        video.name = "kkk"
        print s.add_or_update_video(video)
