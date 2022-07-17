# import time
# from app.mod_camera.base_camera import BaseCamera
# import numpy as np
# import cv2
#
#
# class Camera(BaseCamera):
#     """An emulated camera implementation that streams a repeated sequence of"""
#
#     @staticmethod
#     def frames():
#         # 在这里实现自己视频帧的获取和处理
#         i = 0
#         while True:
#             time.sleep(0.5)
#             img = np.ones((640, 1080, 3), np.uint8) * 188
#             cv2.putText(img, str(i), (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
#             img_encode = cv2.imencode('.jpg', img)[1]
#             img_byte = img_encode.tobytes()
#
#             yield img_byte
#             i = i + 1
#             i = i % 1000



# 树莓派
# import io
# import time
# import picamera
# from base_camera import BaseCamera
#
#
# class Camera(BaseCamera):
#     @staticmethod
#     def frames():
#         with picamera.PiCamera() as camera:
#             # let camera warm up
#             time.sleep(2)
#
#             stream = io.BytesIO()
#             for _ in camera.capture_continuous(stream, 'jpeg',
#                                                use_video_port=True):
#                 # return current frame
#                 stream.seek(0)
#                 yield stream.read()
#
#                 # reset stream for next frame
#                 stream.seek(0)
#                 stream.truncate()


# opencv
import os
import cv2

from app import db
from app.mod_camera.base_camera import BaseCamera
# 导入包
import argparse

import face_recognition

from app.mod_camera.oldcare.facial import FaceUtil
from PIL import Image, ImageDraw, ImageFont
from app.mod_camera.oldcare.utils import fileassistant
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import app.mod_camera.comtrollers as c
import time
import numpy as np
import imutils
import subprocess
import datetime

from app.models import MoodInfo, StrangerInfo


# class Camera_mood(BaseCamera):
#     video_source = 'F:/study/small_semester3/back/2/WIN_20220713_17_16_03_Pro.mp4'
#     # video_source = 0
#
#     def __init__(self):
#         if os.environ.get('OPENCV_CAMERA_SOURCE'):
#             Camera_mood.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
#         super(Camera_mood, self).__init__()
#
#     @staticmethod
#     def set_video_source(source):
#         Camera_mood.video_source = source
#
#     @staticmethod
#     def frames():
#
#         # 得到当前时间
#         current_time = time.strftime('%Y-%m-%d %H:%M:%S',
#                                      time.localtime(time.time()))
#         print('[INFO] %s 陌生人检测程序和表情检测程序启动了.' % current_time)
#
#         # 传入参数
#         ap = argparse.ArgumentParser()
#         ap.add_argument("-f", "--filename", required=False, default='',
#                         help="")
#         args = vars(ap.parse_args())
#         input_video = args['filename']
#
#         # 全局变量
#         facial_recognition_model_path = './app/mod_camera/models/face_recognition_hog.pickle'
#         facial_expression_model_path = './app/mod_camera/models/face_expression.hdf5'
#
#         emotion_model_path = './app/mod_camera/models/emotion_model.hdf5'
#         emotion_classifier = load_model(emotion_model_path)
#
#         # test_emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
#         # emotion_classifier = load_model(test_emotion_model_path, compile=False)
#         EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
#                     "neutral"]
#
#         output_stranger_path = './app/mod_camera/supervision/strangers'
#         output_smile_path = './app/mod_camera/supervision/smile'
#
#         # people_info_path = 'F:/学习1/妈妈的软件/pythonProject/app/mod_camera/info/people_info.csv'
#         people_info_path = './app/mod_camera/info/people_info.csv'
#         facial_expression_info_path = './app/mod_camera/info/facial_expression_info.csv'
#         # your python path
#         python_path = 'E:\\Python\\anaconda\\envs\\pytorch11\\python'
#
#         # 全局常量
#
#         FACIAL_EXPRESSION_TARGET_WIDTH = 64
#         FACIAL_EXPRESSION_TARGET_HEIGHT = 64
#
#         VIDEO_WIDTH = 640
#         VIDEO_HEIGHT = 480
#
#         ANGLE = 20
#
#         # 得到 ID->姓名的map 、 ID->职位类型的map、
#         # 摄像头ID->摄像头名字的map、表情ID->表情名字的map
#         id_card_to_name, id_card_to_type = fileassistant.get_people_info(
#             people_info_path)
#         facial_expression_id_to_name = fileassistant.get_facial_expression_info(
#             facial_expression_info_path)
#
#         # 控制陌生人检测
#         strangers_timing = 0  # 计时开始
#         strangers_start_time = 0  # 开始时间
#         strangers_limit_time = 2  # if >= 2 seconds, then he/she is a stranger.
#
#         # 控制微笑检测
#         facial_expression_timing = 0  # 计时开始
#         facial_expression_start_time = 0  # 开始时间
#         facial_expression_limit_time = 2  # if >= 2 seconds, he/she is smiling
#
#         # 初始化人脸识别模型
#         faceutil = FaceUtil(facial_recognition_model_path)
#         facial_expression_model = load_model(facial_expression_model_path)
#
#         print('[INFO] 开始检测陌生人和表情...')
#         # 不断循环
#
#         counter = 0
#
#         countTime = 0
#         countMoodTime = 0
#         jump = 0
#
#         camera = cv2.VideoCapture(Camera_mood.video_source)
#         if not camera.isOpened():
#             raise RuntimeError('Could not start camera.')
#
#         while True:
#             counter += 1
#             # grab the current frame
#             (grabbed, frame) = camera.read()
#
#             # if we are viewing a video and we did not grab a frame, then we
#             # have reached the end of the video
#             if input_video and not grabbed:
#                 break
#
#             if not input_video:
#                 frame = cv2.flip(frame, 1)
#
#             frame = imutils.resize(frame, width=VIDEO_WIDTH,
#                                    height=VIDEO_HEIGHT)  # 压缩，加快识别速度
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale，表情识别
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#             face_location_list, names = faceutil.get_face_location_and_name(
#                 frame)
#
#             # 得到画面的四分之一位置和四分之三位置，并垂直划线
#             one_fourth_image_center = (int(VIDEO_WIDTH / 4),
#                                        int(VIDEO_HEIGHT / 4))
#             three_fourth_image_center = (int(VIDEO_WIDTH / 4 * 3),
#                                          int(VIDEO_HEIGHT / 4 * 3))
#
#             cv2.line(frame, (one_fourth_image_center[0], 0),
#                      (one_fourth_image_center[0], VIDEO_HEIGHT),
#                      (0, 255, 255), 1)
#             cv2.line(frame, (three_fourth_image_center[0], 0),
#                      (three_fourth_image_center[0], VIDEO_HEIGHT),
#                      (0, 255, 255), 1)
#
#             # if jump % 20 == 0:
#             # 处理每一张识别到的人脸
#             for ((left, top, right, bottom), name) in zip(face_location_list,
#                                                           names):
#                 # 将人脸框出来
#                 rectangle_color = (0, 0, 255)
#                 if id_card_to_type[name] == 'old_people':
#                     rectangle_color = (0, 0, 128)
#                 elif id_card_to_type[name] == 'employee':
#                     rectangle_color = (255, 0, 0)
#                 elif id_card_to_type[name] == 'volunteer':
#                     rectangle_color = (0, 255, 0)
#                 else:
#                     pass
#                 cv2.rectangle(frame, (left, top), (right, bottom),
#                               rectangle_color, 2)
#
#                 if jump % 20 == 0:
#                     # 陌生人检测逻辑
#                     if 'Unknown' in names:  # alert
#                         if strangers_timing == 0:  # just start timing
#                             strangers_timing = 1
#                             strangers_start_time = time.time()
#                         else:  # already started timing
#                             strangers_end_time = time.time()
#                             difference = strangers_end_time - strangers_start_time
#
#                             current_time = time.strftime('%Y-%m-%d %H:%M:%S',
#                                                          time.localtime(time.time()))
#
#                             if difference < strangers_limit_time:
#                                 print('[INFO] %s, 房间, 陌生人仅出现 %.1f 秒. 忽略.' % (current_time, difference))
#                             else:  # strangers appear
#                                 event_desc = '陌生人出现!!!'
#                                 event_location = '房间'
#                                 print('[EVENT] %s, 房间, 陌生人出现!!!' % (current_time))
#
#
#                                 # insert into database
#
#                                 if countTime % 10 == 0:
#                                     # 截图
#                                     cv2.imwrite(os.path.join(output_stranger_path,
#                                                              'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
#                                                 frame)  # snapshot
#                                     stranger = StrangerInfo()
#                                     stranger.date = current_time
#                                     # stranger.oldperson_id = int(name)
#                                     stranger.stranger_info = event_desc
#                                     stranger.address = event_location
#                                     stranger.record = 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))
#                                     # db.session.add(stranger)
#                                     # # data.imgset_dir = data.imgset_dir+'\\'+str(data.id)
#                                     # db.session.commit()
#                                     c.update_insert_data(stranger)
#                                 # 控制插入数据库时间
#                                 countTime = countTime + 1
#                                 # time.sleep(1)
#
#
#                                 # 开始陌生人追踪
#                                 unknown_face_center = (int((right + left) / 2),
#                                                        int((top + bottom) / 2))
#
#                                 cv2.circle(frame, (unknown_face_center[0],
#                                                    unknown_face_center[1]), 4, (0, 255, 0), -1)
#
#                                 direction = ''
#                                 # face locates too left, servo need to turn right,
#                                 # so that face turn right as well
#                                 if unknown_face_center[0] < one_fourth_image_center[0]:
#                                     direction = 'right'
#                                 elif unknown_face_center[0] > three_fourth_image_center[0]:
#                                     direction = 'left'
#
#
#                     else:  # everything is ok
#                         strangers_timing = 0
#
#                     # 表情检测逻辑
#                     # 如果不是陌生人，且对象是老人
#                     if name != 'Unknown' and id_card_to_type[name] == 'old_people':
#                         # 表情检测逻辑
#                         roi = gray[top:bottom, left:right]
#                         roi = cv2.resize(roi, (FACIAL_EXPRESSION_TARGET_WIDTH,
#                                                FACIAL_EXPRESSION_TARGET_HEIGHT))
#                         roi = roi.astype("float") / 255.0
#                         roi = img_to_array(roi)
#                         roi = np.expand_dims(roi, axis=0)
#
#                         emotion_prediction = emotion_classifier.predict(roi)
#                         emotion_probability = np.max(emotion_prediction)
#                         emotion_label_arg = np.argmax(emotion_prediction)
#                         print(emotion_label_arg)
#                         facial_expression_label = EMOTIONS[emotion_label_arg]
#                         print(facial_expression_label)
#
#                         # preds = emotion_classifier.predict(roi)[0]
#                         # facial_expression_label = EMOTIONS[preds.argmax()]
#                         # print(facial_expression_label)
#
#                         if facial_expression_label == 'happy':  # alert
#                             if facial_expression_timing == 0:  # just start timing
#                                 facial_expression_timing = 1
#                                 facial_expression_start_time = time.time()
#                             else:  # already started timing
#                                 facial_expression_end_time = time.time()
#                                 difference = facial_expression_end_time - facial_expression_start_time
#
#                                 current_time = time.strftime('%Y-%m-%d %H:%M:%S',
#                                                              time.localtime(time.time()))
#                                 if difference < facial_expression_limit_time:
#                                     print('[INFO] %s, 房间, %s仅笑了 %.1f 秒. 忽略.' % (
#                                     current_time, id_card_to_name[name], difference))
#                                 else:  # he/she is really smiling
#                                     event_desc = '%s正在笑' % (id_card_to_name[name])
#                                     event_location = '房间'
#                                     print('[EVENT] %s, 房间, %s正在笑.' % (current_time, id_card_to_name[name]))
#
#                                     # 将数据插入到数据库中
#                                     if countMoodTime % 60 == 0:
#                                         cv2.imwrite(os.path.join(output_smile_path,
#                                                                  'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
#                                                     frame)  # snapshot
#                                         mood = MoodInfo()
#                                         mood.mood_info = event_desc
#                                         mood.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                                         mood.address = event_location
#                                         mood.oldperson_id = int(name)
#                                         mood.record = 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))
#                                         c.update_insert_data(mood)
#                                     countMoodTime = countMoodTime + 1
#                                     time.sleep(1)
#
#
#                         else:  # everything is ok
#                             facial_expression_timing = 0
#
#                     else:  # 如果是陌生人，则不检测表情
#                         facial_expression_label = ''
#
#                 # 人脸识别和表情识别都结束后，把表情和人名写上
#                 # (同时处理中文显示问题)
#                 img_PIL = Image.fromarray(cv2.cvtColor(frame,
#                                                        cv2.COLOR_BGR2RGB))
#
#                 draw = ImageDraw.Draw(img_PIL)
#                 final_label = id_card_to_name[name] + ': ' + facial_expression_id_to_name[
#                     facial_expression_label] if facial_expression_label else id_card_to_name[name]
#                 draw.text((left, top - 30), final_label,
#                           font=ImageFont.truetype('./app/mod_camera/models/simsun.ttc', 40),
#                           fill=(255, 0, 0))  # windows
#
#                 # 转换回OpenCV格式
#                 frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
#             yield cv2.imencode('.jpg', frame)[1].tobytes()
#             # else:
#             #     yield cv2.imencode('.jpg', frame)[1].tobytes()
#             jump = jump + 1
#             # show our detected faces along with smiling/not smiling labels
#             # cv2.imshow("Checking Strangers and Ole People's Face Expression",
#             #            frame)
#
#             # Press 'ESC' for exiting video
#
#             # k = cv2.waitKey(100) & 0xff
#             # if k == 27:
#             #     break


def frames():

    # 得到当前时间
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))
    print('[INFO] %s 陌生人检测程序和表情检测程序启动了.' % current_time)

    # 传入参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required=False, default='',
                    help="")
    args = vars(ap.parse_args())
    input_video = args['filename']

    # 全局变量
    facial_recognition_model_path = './app/mod_camera/models/face_recognition_hog.pickle'
    facial_expression_model_path = './app/mod_camera/models/face_expression.hdf5'

    emotion_model_path = './app/mod_camera/models/emotion_model.hdf5'
    emotion_classifier = load_model(emotion_model_path)

    # test_emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
    # emotion_classifier = load_model(test_emotion_model_path, compile=False)
    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
                "neutral"]

    output_stranger_path = './app/static/smile'
    output_smile_path = './app/static/smile'

    # people_info_path = 'F:/学习1/妈妈的软件/pythonProject/app/mod_camera/info/people_info.csv'
    people_info_path = './app/mod_camera/info/people_info.csv'
    facial_expression_info_path = './app/mod_camera/info/facial_expression_info.csv'
    # your python path
    python_path = 'E:\\Python\\anaconda\\envs\\pytorch11\\python'

    # 全局常量

    FACIAL_EXPRESSION_TARGET_WIDTH = 64
    FACIAL_EXPRESSION_TARGET_HEIGHT = 64

    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480

    ANGLE = 20

    # 得到 ID->姓名的map 、 ID->职位类型的map、
    # 摄像头ID->摄像头名字的map、表情ID->表情名字的map
    id_card_to_name, id_card_to_type = fileassistant.get_people_info(
        people_info_path)
    facial_expression_id_to_name = fileassistant.get_facial_expression_info(
        facial_expression_info_path)

    # 控制陌生人检测
    strangers_timing = 0  # 计时开始
    strangers_start_time = 0  # 开始时间
    strangers_limit_time = 2  # if >= 2 seconds, then he/she is a stranger.

    # 控制微笑检测
    facial_expression_timing = 0  # 计时开始
    facial_expression_start_time = 0  # 开始时间
    facial_expression_limit_time = 2  # if >= 2 seconds, he/she is smiling

    # 初始化人脸识别模型
    faceutil = FaceUtil(facial_recognition_model_path)
    facial_expression_model = load_model(facial_expression_model_path)

    print('[INFO] 开始检测陌生人和表情...')
    # 不断循环

    counter = 0

    countTime = 0
    countMoodTime = 0
    countMoodTime2 = 0
    countMoodTime3 = 0
    jump = 0

    camera = cv2.VideoCapture('F:/study/small_semester3/back/2/WIN_20220713_17_16_03_Pro.mp4')
    # camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError('Could not start camera.')

    while True:
        counter += 1
        # grab the current frame
        (grabbed, frame) = camera.read()

        # if we are viewing a video and we did not grab a frame, then we
        # have reached the end of the video
        if input_video and not grabbed:
            break

        if not input_video:
            frame = cv2.flip(frame, 1)

        frame = imutils.resize(frame, width=VIDEO_WIDTH,
                               height=VIDEO_HEIGHT)  # 压缩，加快识别速度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale，表情识别
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_location_list, names = faceutil.get_face_location_and_name(
            frame)

        # 得到画面的四分之一位置和四分之三位置，并垂直划线
        one_fourth_image_center = (int(VIDEO_WIDTH / 4),
                                   int(VIDEO_HEIGHT / 4))
        three_fourth_image_center = (int(VIDEO_WIDTH / 4 * 3),
                                     int(VIDEO_HEIGHT / 4 * 3))

        cv2.line(frame, (one_fourth_image_center[0], 0),
                 (one_fourth_image_center[0], VIDEO_HEIGHT),
                 (0, 255, 255), 1)
        cv2.line(frame, (three_fourth_image_center[0], 0),
                 (three_fourth_image_center[0], VIDEO_HEIGHT),
                 (0, 255, 255), 1)

        # if jump % 20 == 0:
        # 处理每一张识别到的人脸
        for ((left, top, right, bottom), name) in zip(face_location_list,
                                                      names):
            # 将人脸框出来
            rectangle_color = (0, 0, 255)
            if id_card_to_type[name] == 'old_people':
                rectangle_color = (0, 0, 128)
            elif id_card_to_type[name] == 'employee':
                rectangle_color = (255, 0, 0)
            elif id_card_to_type[name] == 'volunteer':
                rectangle_color = (0, 255, 0)
            else:
                pass
            cv2.rectangle(frame, (left, top), (right, bottom),
                          rectangle_color, 2)

            if jump % 20 == 0:
                # 陌生人检测逻辑
                if 'Unknown' in names:  # alert
                    if strangers_timing == 0:  # just start timing
                        strangers_timing = 1
                        strangers_start_time = time.time()
                    else:  # already started timing
                        strangers_end_time = time.time()
                        difference = strangers_end_time - strangers_start_time

                        current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(time.time()))

                        if difference < strangers_limit_time:
                            print('[INFO] %s, 房间, 陌生人仅出现 %.1f 秒. 忽略.' % (current_time, difference))
                        else:  # strangers appear
                            event_desc = '陌生人出现!!!'
                            event_location = '房间'
                            print('[EVENT] %s, 房间, 陌生人出现!!!' % (current_time))


                            # insert into database

                            if countTime % 10 == 0:
                                # 截图
                                cv2.imwrite(os.path.join(output_stranger_path,
                                                         'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                                            frame)  # snapshot
                                stranger = StrangerInfo()
                                stranger.date = current_time
                                # stranger.oldperson_id = int(name)
                                stranger.stranger_info = event_desc
                                stranger.address = event_location
                                stranger.record = 'http://192.168.0.100:8085/static/smile/' + 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))
                                # db.session.add(stranger)
                                # # data.imgset_dir = data.imgset_dir+'\\'+str(data.id)
                                # db.session.commit()
                                c.update_insert_data(stranger)
                                c.send_emailStranger()
                            # 控制插入数据库时间
                            countTime = countTime + 1
                            # time.sleep(1)


                            # 开始陌生人追踪
                            unknown_face_center = (int((right + left) / 2),
                                                   int((top + bottom) / 2))

                            cv2.circle(frame, (unknown_face_center[0],
                                               unknown_face_center[1]), 4, (0, 255, 0), -1)

                            direction = ''
                            # face locates too left, servo need to turn right,
                            # so that face turn right as well
                            if unknown_face_center[0] < one_fourth_image_center[0]:
                                direction = 'right'
                            elif unknown_face_center[0] > three_fourth_image_center[0]:
                                direction = 'left'


                else:  # everything is ok
                    strangers_timing = 0

                # 表情检测逻辑
                # 如果不是陌生人，且对象是老人
                if name != 'Unknown' and id_card_to_type[name] == 'old_people':
                    # 表情检测逻辑
                    roi = gray[top:bottom, left:right]
                    roi = cv2.resize(roi, (FACIAL_EXPRESSION_TARGET_WIDTH,
                                           FACIAL_EXPRESSION_TARGET_HEIGHT))
                    roi = roi.astype("float") / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    emotion_prediction = emotion_classifier.predict(roi)
                    emotion_probability = np.max(emotion_prediction)
                    emotion_label_arg = np.argmax(emotion_prediction)
                    print(emotion_label_arg)
                    facial_expression_label = EMOTIONS[emotion_label_arg]
                    print(facial_expression_label)

                    # preds = emotion_classifier.predict(roi)[0]
                    # facial_expression_label = EMOTIONS[preds.argmax()]
                    # print(facial_expression_label)

                    if facial_expression_label == 'happy':  # alert
                        if facial_expression_timing == 0:  # just start timing
                            facial_expression_timing = 1
                            facial_expression_start_time = time.time()
                        else:  # already started timing
                            facial_expression_end_time = time.time()
                            difference = facial_expression_end_time - facial_expression_start_time

                            current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(time.time()))
                            if difference < facial_expression_limit_time:
                                print('[INFO] %s, 房间, %s仅笑了 %.1f 秒. 忽略.' % (
                                current_time, id_card_to_name[name], difference))
                            else:  # he/she is really smiling
                                event_desc = '%s正在笑' % (id_card_to_name[name])
                                event_location = '房间'
                                print('[EVENT] %s, 房间, %s正在笑.' % (current_time, id_card_to_name[name]))

                                # 将数据插入到数据库中
                                if countMoodTime % 3 == 0:
                                    cv2.imwrite(os.path.join(output_smile_path,
                                                             'happysnapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                                                frame)  # snapshot
                                    mood = MoodInfo()
                                    mood.mood_info = event_desc
                                    mood.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    mood.address = event_location
                                    mood.oldperson_id = int(name)
                                    mood.record = 'http://192.168.0.101:8085/static/smile/' + 'happysnapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))
                                    c.update_insert_data(mood)
                            countMoodTime = countMoodTime + 1
                                # time.sleep(1)


                    elif facial_expression_label == 'scared':  # everything is ok
                        facial_expression_end_time = time.time()
                        difference = facial_expression_end_time - facial_expression_start_time

                        current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(time.time()))
                        if difference < facial_expression_limit_time:
                            print('[INFO] %s, 房间, %s仅笑了 %.1f 秒. 忽略.' % (
                                current_time, id_card_to_name[name], difference))
                        else:  # he/she is really smiling
                            event_desc = '%s正在害怕' % (id_card_to_name[name])
                            event_location = '房间'
                            print('[EVENT] %s, 房间, %s正在害怕.' % (current_time, id_card_to_name[name]))

                            # 将数据插入到数据库中
                            if countMoodTime3 % 10 == 0:
                                cv2.imwrite(os.path.join(output_smile_path,
                                                         'scalesnapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                                            frame)  # snapshot
                                mood = MoodInfo()
                                mood.mood_info = event_desc
                                mood.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                mood.address = event_location
                                mood.oldperson_id = int(name)
                                mood.record = 'http://192.168.0.101:8085/static/smile/' + 'scalesnapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))
                                c.update_insert_data(mood)
                        countMoodTime3 = countMoodTime3 + 1

                    elif facial_expression_label == 'neutral':  # everything is ok
                        facial_expression_end_time = time.time()
                        difference = facial_expression_end_time - facial_expression_start_time

                        current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(time.time()))
                        if difference < facial_expression_limit_time:
                            print('[INFO] %s, 房间, %s仅笑了 %.1f 秒. 忽略.' % (
                                current_time, id_card_to_name[name], difference))
                        else:  # he/she is really smiling
                            event_desc = '%s正常表情' % (id_card_to_name[name])
                            event_location = '房间'
                            print('[EVENT] %s, 房间, %s正常表情.' % (current_time, id_card_to_name[name]))

                            # 将数据插入到数据库中
                            if countMoodTime2 % 3 == 0:
                                cv2.imwrite(os.path.join(output_smile_path,
                                                         'nsnapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                                            frame)  # snapshot
                                mood = MoodInfo()
                                mood.mood_info = event_desc
                                mood.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                mood.address = event_location
                                mood.oldperson_id = int(name)
                                mood.record = 'http://192.168.0.101:8085/static/smile/' + 'nsnapshot_%s.jpg' % (
                                    time.strftime('%Y%m%d_%H%M%S'))
                                c.update_insert_data(mood)
                        countMoodTime2 = countMoodTime2 + 1

                else:  # 如果是陌生人，则不检测表情
                    facial_expression_label = ''

            # 人脸识别和表情识别都结束后，把表情和人名写上
            # (同时处理中文显示问题)
            img_PIL = Image.fromarray(cv2.cvtColor(frame,
                                                   cv2.COLOR_BGR2RGB))

            draw = ImageDraw.Draw(img_PIL)
            final_label = id_card_to_name[name] + ': ' + facial_expression_id_to_name[
                facial_expression_label] if facial_expression_label else id_card_to_name[name]
            draw.text((left, top - 30), final_label,
                      font=ImageFont.truetype('./app/mod_camera/models/simsun.ttc', 40),
                      fill=(255, 0, 0))  # windows

            # 转换回OpenCV格式
            frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
        # yield cv2.imencode('.jpg', frame)[1].tobytes()
        jump = jump + 1
        frame =  cv2.imencode('.jpg', frame)[1].tobytes()
        g = cv2.waitKey(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # else:
        #     yield cv2.imencode('.jpg', frame)[1].tobytes()
