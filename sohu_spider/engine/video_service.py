# coding=utf-8
__author__ = 'cafedeflore'

import sqlite3

class Video(object):
    def __init__(self):
        self.vid = ""
        self.name = ""
        self.type = ""
        self.pic = ""
        self.actors = ""
        self.detail = ""
        self.play_count = ""
        self.delta = ""
        self.delta_type = 0
        #trace

    def __str__(self):
        return "name:%s" % self.name


class VideoService(object):
    """
    the engine of spider.
    set_config to setup spider.
    start_work to power on
    """

    def __init__(self):
        self.db = sqlite3.connect("D:/test/test.db")
        self.cur = self.db.cursor()
        return

    def get_video(self, name, delta_type=0):
        res_dict = dict()
        video = Video()
        sql = "select id, name, type, pic, actors, detail, vid, play_count, delta, delta_type from video where name = '%s' and delta_type='%d'" % (name, delta_type)
        # print sql
        self.cur.execute(sql)
        res = self.cur.fetchall()
        desc = self.cur.description
        if len(res) < 1:
            return None

        for i in xrange(len(desc)):
            res_dict[desc[i][0]] = res[0][i]

        video.name = res_dict['name']
        video.type = res_dict['type']
        video.pic = res_dict['pic']
        video.actors = res_dict['actors']
        video.detail = res_dict['detail']

        return video

    def add_or_update_video(self, video):
        if self.get_video(video.name, video.delta_type):
            sql = "update video set type='%s', pic='%s', actors='%s', detail='%s',vid='%s', play_count='%s', delta='%s' where name='%s' and delta_type='%d'"\
                  % (video.type, video.pic, video.actors, video.detail, video.vid, video.play_count, video.delta, video.name, video.delta_type)
            # print sql
            self.cur.execute(sql)
            self.db.commit()
        else:
            sql = "insert into video(name, type, pic, actors, detail, vid, play_count, delta, delta_type) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" \
                  % (video.name, video.type, video.pic, video.actors, video.detail, video.vid, video.play_count, video.delta, video.delta_type)
            self.cur.execute(sql)
            self.db.commit()
        return