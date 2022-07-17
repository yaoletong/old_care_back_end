# 实时视频模块视图
from flask import Blueprint, jsonify
# !/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

from app.mod_camera.camera_fall import Camera_fall
from app.mod_camera.camera_invade import Camera_invade
import app.mod_camera.camera_mood as mood
from app.mod_camera.camera_interact import Camera_interact
import app.mod_camera.comtrollers as c
from app.mod_camera.collectingfaces import Camera_face
from app.mod_user.controllers import login_required

camera = Blueprint('camera', __name__)


# import camera driver

# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from app.mod_camera.camera_mood import Camera_mood


# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera


# 跳转前端视频检测页面
@camera.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:

        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# 检测老人心情
@camera.route('/camera/mood', methods=['GET', 'POST'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # return Response(gen(Camera_mood()),
    #                 mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(mood.frames(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

# # 检测老人心情
# @camera.route('/camera/mood1', methods=['GET', 'POST'])
# def video_feed1():
#    gen(Camera_mood())



# 义工交互
@camera.route('/camera/interact', methods=['GET', 'POST'])
def interact(): 
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera_interact()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 人脸采集
@camera.route('/camera/getface', methods=['GET', 'POST'])
def getface():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera_face()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 检测摔倒
@camera.route('/camera/fall', methods=['GET', 'POST'])
def fall():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera_fall()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 检测入侵
@camera.route('/camera/invade', methods=['GET', 'POST'])
def invade():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera_invade()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 展示所有关于老人心情的信息
@camera.route('/camera/moodInfolist')
@login_required
def list_all_moodinfo():
    item = []
    _listdata = c.get_all_mooddata()
    columns = [
        {
            'title': 'id',
            'slot': 'id'
        },
        {
            'title': '老人不同心情信息',
            'key': 'mood_info'
        },
        {
            'title': '截取日期',
            'key': 'date'
        },
        {
            'title': '截取地点',
            'key': 'address'
        },
        {
            'title': '截取截图',
            'slot': 'record',
            'key': 'record'
        },
        {
            'title': '相关老人id',
            'key': 'oldperson_id'
        },
    ]
    for obj in _listdata:
        item.append(obj.to_json())

    print(item)
    return jsonify({"code": 0, "items": item, "columns": columns})


# 展示所有关于老人摔倒的信息
@camera.route('/camera/fallInfolist')
@login_required
def list_all_fallinfo():
    item = []
    _listdata = c.get_all_falldata()
    columns = [
        {
            'title': 'id',
            'slot': 'id'
        },
        {
            'title': '摔倒信息',
            'key': 'fall_info'
        },
        {
            'title': '摔倒日期',
            'key': 'date'
        },
        {
            'title': '摔倒地点',
            'key': 'address'
        },
        {
            'title': '摔倒回放',
            'slot': 'record',
            'key': 'record'
        },
        {
            'title': '摔倒老人id',
            'key': 'oldperson_id'
        },
    ]
    for obj in _listdata:
        item.append(obj.to_json())

    return jsonify({"code": 0, "items": item, "columns": columns})


# 展示所有关于入侵危险区域的信息
@camera.route('/camera/invadeInfolist')
@login_required
def list_all_invadeinfo():
    item = []
    _listdata = c.get_all_invadedata()
    columns = [
        {
            'title': 'id',
            'slot': 'id'
        },
        {
            'title': '入侵信息',
            'key': 'invade_info'
        },
        {
            'title': '入侵日期',
            'key': 'date'
        },
        {
            'title': '入侵地点',
            'key': 'address'
        },
        {
            'title': '入侵回放',
            'slot': 'record',
            'key': 'record'
        }
    ]
    for obj in _listdata:
        item.append(obj.to_json())

    return jsonify({"code": 0, "items": item, "columns": columns})


# 展示所有关于老人与义工交互的信息
@camera.route('/camera/interactInfolist')
@login_required
def list_all_interactinfo():
    item = []
    _listdata = c.get_all_interactdata()
    columns = [
        {
            'title': 'id',
            'slot': 'id'
        },
        {
            'title': '交互信息',
            'key': 'interact_info'
        },
        {
            'title': '交互日期',
            'key': 'date'
        },
        {
            'title': '交互距离',
            'key': 'distance'
        },
        {
            'title': '交互回放',
            'slot': 'record',
            'key': 'record'
        },
        {
            'title': '相关老人姓名',
            'key': 'oldperson_name'
        }
    ]
    for obj in _listdata:
        item.append(obj.to_json())

    return jsonify({"code": 0, "items": item, "columns": columns})