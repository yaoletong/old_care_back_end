# 实时视频模块逻辑
import smtplib

from email.mime.text import MIMEText

from random import random

from app import db
from app.models import MoodInfo, InteractInfo, FallInfo, StrangerInfo, InvadeInfo


# 获取老人心情所有数据
def get_all_mooddata():
    return MoodInfo.query.all()


# 获取老人摔倒所有数据
def get_all_falldata():
    return FallInfo.query.all()


# 获取老人与义工交互所有数据
def get_all_interactdata():
    return InteractInfo.query.all()


# 获取陌生人出现所有数据
def get_all_strangerdata():
    return StrangerInfo.query.all()


# 获取入侵的所有数据
def get_all_invadedata():
    return InvadeInfo.query.all()


# 更新或者新增数据
def update_insert_data(data):
    # if (data.id == 0):
    db.session.add(data)
    # data.imgset_dir = data.imgset_dir+'\\'+str(data.id)
    db.session.commit()
    # else:
    #     _data = data.__dict__
    #
    #     _data.pop('_sa_instance_state')
    #
    #     MoodInfo.query.filter_by(id=data.id).update(_data)
    #     db.session.commit()


# 发送陌生人警告
def send_emailStranger():
        email = "19301100@bjtu.edu.cn"
        print(email)
        mail_host = 'smtp.163.com'
        # 163用户名
        mail_user = '13723723013' 
        # 密码(部分邮箱为授权码)
        mail_pass = 'ZY20001206tyl'
        # 邮件发送方邮箱地址
        sender = '13723723013@163.com'

        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]

        content = '【智慧养老系统警告】有陌生人闯入！小心！'

        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '智慧养老系统警告提示'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            print(2)
            smtpObj.connect(mail_host, 25)
            # 登录到服务器
            print(3)
            smtpObj.login(mail_user, mail_pass)
            # 发送
            print(4)
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print(1)
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误


# 发送入侵信息
def send_emailInvade():
        email = "19301100@bjtu.edu.cn"
        print(email)
        mail_host = 'smtp.163.com'
        # 163用户名
        mail_user = '13723723013'
        # 密码(部分邮箱为授权码)
        mail_pass = 'ZY20001206tyl'
        # 邮件发送方邮箱地址
        sender = '13723723013@163.com'

        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]

        content = '【智慧养老系统警告】有人闯入禁区！请及时留意并查看监控！小心！'

        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '智慧养老系统警告提示'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            print(2)
            smtpObj.connect(mail_host, 25)
            # 登录到服务器
            print(3)
            smtpObj.login(mail_user, mail_pass)
            # 发送
            print(4)
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print(1)
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误


# 发送摔倒信息
def send_emailFall():
        email = "19301100@bjtu.edu.cn"
        print(email)
        mail_host = 'smtp.163.com'
        # 163用户名
        mail_user = '13723723013'
        # 密码(部分邮箱为授权码)
        mail_pass = 'ZY20001206tyl'
        # 邮件发送方邮箱地址
        sender = '13723723013@163.com'

        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]

        content = '【智慧养老系统警告】有老人摔倒！请及时留意并查看监控！小心！'

        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '智慧养老系统警告提示'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            print(2)
            smtpObj.connect(mail_host, 25)
            # 登录到服务器
            print(3)
            smtpObj.login(mail_user, mail_pass)
            # 发送
            print(4)
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print(1)
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误