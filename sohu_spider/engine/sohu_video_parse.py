# coding=utf-8
__author__ = 'cafedeflore'

from engine import UrlParse
from bs4 import BeautifulSoup
from engine import video_service
import json


class SohuVideoParse(object):

    @staticmethod
    def get_sub_type_url(input):
        """
        get the sub type's urls
        :param input: the html of origin web
        :return:the list of urls
        """
        list = []
        try:
            bs = BeautifulSoup(input)
            menu = bs.findAll(class_='rList_menu1')[0]
            for item in menu.findAll("a"):
                # print item
                list.append(item['href'])
            return list
        except Exception as err:
            # print err
            return list

    @staticmethod
    def deal_with_the_callback(input):
        if input.startswith('callback') and input.endswith(')'):
            res = input[9:-1]
            js = json.loads(res)
            # print js['data']['tv_cont_cate']
            return js
        return None

    @staticmethod
    def get_video_detail(url):
        # url = "http://tv.sohu.com/hotdrama/"
        video_list = []
        try:
            content = UrlParse.UrlParse.get_html_content(url)
            bs = BeautifulSoup(content)
            nodes = bs.findAll(class_="vNameIn")
            for video_node in nodes:
                try:
                    video = video_service.Video()
                    vid = video_node['data-plid']
                    info_all_node = video_node.parent.parent
                    # print info_all_node
                    video.name = info_all_node.findAll(class_="at")[0].get_text()
                    video.play_count = info_all_node.findAll(class_="vTotal")[0].get_text()
                    video.delta = info_all_node.findAll(class_="vRank")[0].get_text()
                    delta_type_name = info_all_node.findAll(class_="vRank")[0]['title']
                    if '日' in delta_type_name.encode('utf8'):
                        video.delta_type = 0
                    elif '周' in delta_type_name.encode('utf8'):
                        video.delta_type = 1
                    else:
                        video.delta_type = 2

                    # url = "http://feedback.vrs.sohu.com/api/ugc/video.json?vid=%s" % vid
                    url = "http://feedback.vrs.sohu.com/api/vrs/album.jsonp?albumId=%s" % vid
                    # print url
                    more = UrlParse.UrlParse.get_html_content(url)
                    js = SohuVideoParse.deal_with_the_callback(more)
                    if js:
                        video.detail = js['data']['tv_desc']
                        video.pic = js['data']['tv_ver_small_pic']

                        #actor
                        actor_str = ""
                        for actor in js['data']['actor']:
                            if actor_str == "":
                                actor_str += actor['FIELD_VALUE']
                            else:
                                actor_str += "/" + actor['FIELD_VALUE']
                        video.actors = actor_str

                        #type
                        type_str = ""
                        for type in js['data']['tv_cont_cate']:
                            if type_str == "":
                                type_str += type['tv_cont_cate_name']
                            else:
                                type_str += "/"+ type['tv_cont_cate_name']
                        video.type = type_str

                    video.vid = vid
                    # print video.name
                    video_list.append(video)
                except Exception as err:
                    print err
                    continue
                # break
            return video_list
        except Exception as err:
            print err
            return video_list

# url = "http://tv.sohu.com/hotdrama/"
# url = UrlParse.UrlParse.get_html_content(url)
# print SohuVideoParse.get_sub_type_url(url)