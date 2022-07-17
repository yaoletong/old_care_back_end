# 老人摔倒模块

# 导入包
import mediapipe as mp
import joblib
import os
import cv2
from app.mod_camera.base_camera import BaseCamera
import time
import numpy as np
import app.mod_camera.comtrollers as c
from app.models import FallInfo


class Camera_fall(BaseCamera):
    video_source = 'F:\\study\\small_semester3\\back\\KNN-Fall-Detection-main\\KNN-Fall-Detection-main\\qikeji1.mp4'

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera_fall.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera_fall, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera_fall.video_source = source

    @staticmethod
    def frames():

        pose_knn = joblib.load('./app/mod_camera/models/PoseKeypoint.joblib')
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        prevTime = 0
        keyXYZ = [
            "nose_x",
            "nose_y",
            "nose_z",
            "left_eye_inner_x",
            "left_eye_inner_y",
            "left_eye_inner_z",
            "left_eye_x",
            "left_eye_y",
            "left_eye_z",
            "left_eye_outer_x",
            "left_eye_outer_y",
            "left_eye_outer_z",
            "right_eye_inner_x",
            "right_eye_inner_y",
            "right_eye_inner_z",
            "right_eye_x",
            "right_eye_y",
            "right_eye_z",
            "right_eye_outer_x",
            "right_eye_outer_y",
            "right_eye_outer_z",
            "left_ear_x",
            "left_ear_y",
            "left_ear_z",
            "right_ear_x",
            "right_ear_y",
            "right_ear_z",
            "mouth_left_x",
            "mouth_left_y",
            "mouth_left_z",
            "mouth_right_x",
            "mouth_right_y",
            "mouth_right_z",
            "left_shoulder_x",
            "left_shoulder_y",
            "left_shoulder_z",
            "right_shoulder_x",
            "right_shoulder_y",
            "right_shoulder_z",
            "left_elbow_x",
            "left_elbow_y",
            "left_elbow_z",
            "right_elbow_x",
            "right_elbow_y",
            "right_elbow_z",
            "left_wrist_x",
            "left_wrist_y",
            "left_wrist_z",
            "right_wrist_x",
            "right_wrist_y",
            "right_wrist_z",
            "left_pinky_x",
            "left_pinky_y",
            "left_pinky_z",
            "right_pinky_x",
            "right_pinky_y",
            "right_pinky_z",
            "left_index_x",
            "left_index_y",
            "left_index_z",
            "right_index_x",
            "right_index_y",
            "right_index_z",
            "left_thumb_x",
            "left_thumb_y",
            "left_thumb_z",
            "right_thumb_x",
            "right_thumb_y",
            "right_thumb_z",
            "left_hip_x",
            "left_hip_y",
            "left_hip_z",
            "right_hip_x",
            "right_hip_y",
            "right_hip_z",
            "left_knee_x",
            "left_knee_y",
            "left_knee_z",
            "right_knee_x",
            "right_knee_y",
            "right_knee_z",
            "left_ankle_x",
            "left_ankle_y",
            "left_ankle_z",
            "right_ankle_x",
            "right_ankle_y",
            "right_ankle_z",
            "left_heel_x",
            "left_heel_y",
            "left_heel_z",
            "right_heel_x",
            "right_heel_y",
            "right_heel_z",
            "left_foot_index_x",
            "left_foot_index_y",
            "left_foot_index_z",
            "right_foot_index_x",
            "right_foot_index_y",
            "right_foot_index_z"
        ]
        res_point = []

        countTime = 0
        camera = cv2.VideoCapture(Camera_fall.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        with mp_pose.Pose(
                static_image_mode=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as pose:
            while True:
                success, frame = camera.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # continue
                    break
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)
                if results.pose_landmarks:
                    for index, landmarks in enumerate(results.pose_landmarks.landmark):
                        # print(index, landmarks.x, landmarks.y, landmarks.z)
                        res_point.append(landmarks.x)
                        res_point.append(landmarks.y)
                        res_point.append(landmarks.z)
                    shape1 = int(len(res_point) / len(keyXYZ))
                    res_point = np.array(res_point).reshape(shape1, len(keyXYZ))
                    pred = pose_knn.predict(res_point)
                    res_point = []
                    print(pred)
                    if pred == 0:
                        # 插入摔倒数据
                        if countTime % 10 == 0:
                            output_stranger_path = './app/static/smile'
                            cv2.imwrite(os.path.join(output_stranger_path,
                                                     'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                                        frame)  # snapshot
                            fall = FallInfo()
                            fall.fall_info = '老人摔倒了'
                            fall.date = time.strftime('%Y-%m-%d %H:%M:%S',
                                                             time.localtime(time.time()))
                            fall.address = '房间'
                            fall.oldperson_id = 3
                            fall.record = 'http://192.168.0.100:8085/static/smile/' + 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))
                            c.update_insert_data(fall)
                            c.send_emailFall()
                        countTime = countTime + 1
                        cv2.putText(frame, "FALL", (600, 80), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 2)
                    else:
                        cv2.putText(frame, "NORMAL", (600, 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 2)
                # Draw the pose annotation on the image.
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                # Flip the image horizontally for a selfie-view display.
                currTime = time.time()
                fps = 1 / (currTime - prevTime)
                prevTime = currTime
                cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
                # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
                yield cv2.imencode('.jpg', frame)[1].tobytes()
                # cv2.imshow('MediaPipe Pose', image)
                if cv2.waitKey(1) & 0xFF == 27:
                    break



# cap = cv2.VideoCapture("Fall_Trim.mp4")
# cap = cv2.VideoCapture("q.mp4")
# cap = cv2.VideoCapture("qian.mp4")
# cap = cv2.VideoCapture("hou.mp4")
# cap = cv2.VideoCapture("ce.mp4")
# cap = cv2.VideoCapture("F:\\study\\small_semester3\\back\\KNN-Fall-Detection-main\\KNN-Fall-Detection-main\\qikeji1.mp4")
# cap = cv2.VideoCapture(0)


# cap.release()
