# coding=utf-8
__author__ = 'cafedeflore'

import unittest
from engine import sohu_video_parse
from engine import  video_service

class SohuVideoParseTest(unittest.TestCase):
    def test_parse(self):
        s = video_service.VideoService()
        url = "http://tv.sohu.com/hotdrama/"
        list = sohu_video_parse.SohuVideoParse.get_video_detail(url)
        print len(list)
        for video in list:
            s.add_or_update_video(video)
