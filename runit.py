from flask import jsonify, request, render_template
import pymysql

from app import app, config, db
from app.mod_camera.forms import camera
from app.mod_employee.forms import employee
from app.mod_oldperson.forms import oldperson
from app.mod_user.forms import user
from app.mod_volunteer.forms import volunteer
from flask_cors import CORS

# 配置数据库

db.init_app(app)  # 绑定到我们到应用程序
CORS(app, supports_credentials=True)  # 跨域

# 蓝图
# 连接老人、义工、工作人员以及系统管理员蓝图
app.register_blueprint(oldperson)
app.register_blueprint(volunteer)
app.register_blueprint(employee)
app.register_blueprint(user)
app.register_blueprint(camera)


# 运行系统
if __name__ == '__main__':
    # 服务器运行
    app.run(host='0.0.0.0', port=8085, debug=True)

    # 本地运行
    # db.init_app(app)  # 绑定到我们到应用程序
    # app.run(host='127.0.0.1', port=8080, debug=True)