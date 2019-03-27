#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: test.py 
@time: 3/15/19 11:45 
@description：TODO
"""

import itchat


itchat.auto_login(True)


def send_to_person(username, file_names):
    """
    发送给某个人
    :param username: 发送对象的昵称
    :param filename: 文件名
    :return:
    """
    room = itchat.search_friends(name=r'%s' % username)

    userName = room[0]['UserName']

    try:
        if isinstance(file_names, list):
            # 多个图片
            for file_name in file_names:
                itchat.send_image(file_name, toUserName=userName)
        else:
            # 一个图片
            itchat.send_image(file_names, toUserName=userName)
        print('发送完毕！')
    except:
        print('发送出错！')


def send_to_group_chat(target_group_chat_name, file_names):
    """
    群聊
    :param target_group_chat_name:
    :param file_name:
    :return:
    """
    rooms = itchat.get_chatrooms(update=True)

    # 目标群聊对象
    target_room = None
    for room in rooms:
        group_chat_name = room.get('NickName')
        if target_group_chat_name == group_chat_name:
            target_room = room
            break

    if target_room:
        if isinstance(file_names, list):
            for file_name in file_names:
                target_room.send_image(file_name)
        else:
            target_room.send_image(file_names)

        print('发送完毕！')
    else:
        print('抱歉，不存在这个群聊')
