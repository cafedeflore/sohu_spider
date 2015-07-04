# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This the engine
"""
import logging
from engine import UrlParse
from engine import sohu_video_parse
from engine import video_service

class SpiderEngine(object):
    """
    the engine of spider.
    set_config to setup spider.
    start_work to power on
    """

    def __init__(self):
        self.url_list_file = "urls"
        self.output_directory = "output"
        self.origin_url = "http://tv.sohu.com/hotdrama/"
        return

    def __str__(self):
        return self.__getattribute__('url_list_file')

    def start_work(self):
        """
        start to work
        :return: nothing
        """
        content = UrlParse.UrlParse.get_html_content(self.origin_url)
        url_list = sohu_video_parse.SohuVideoParse.get_sub_type_url(content)
        s = video_service.VideoService()
        for url in url_list:
            print "parsing " + url
            video_list = sohu_video_parse.SohuVideoParse.get_video_detail(url)
            for video in video_list:
                print "doing " + video.name
                s.add_or_update_video(video)
                UrlParse.UrlParse.download(self.output_directory, video.pic)
        return