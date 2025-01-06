from flask import Flask
from flask import render_template, send_file, redirect, make_response
from flask import send_from_directory, abort, jsonify, url_for
from flask import request, session, Response
from datetime import timedelta
from db import dbconfig
from db.tables import db
from utils.conversation import createChatCompletion, get_model_response, createStream
from cls.login import Login
from utils.preprocess import prerprocess
from utils.genjsdata import generate_response_data
import json
import os


SERVER_IP = "127.0.0.1"             # 配置服务器IP地址
UPLOAD_FOLDER = 'media'                 # 配置上传文件根目录
STATIC_FOLDER = 'static'                # 配置静态文件根目录
TEMPLATE_FOLDER = 'templates'           # 配置HTML文件根目录
REDIS_URL = 'redis://localhost'         # 配置REDIS服务地址
PROMPT_PATH = "D:\pythonProject\Sleep\media\Prompt.txt"     # 配置提示词文件地址
MAX_CONTEXT_LEN = 5                     # 配置最大上下文长度
SECRET_KEY = os.urandom(24)             # 配置Session密钥
EXPIRE_DAYS = 7                         # 配置Session失效时长
ALLOWED_EXTENSIONS = set(['csv'])


app = Flask(__name__,
            static_folder=STATIC_FOLDER,             
            template_folder=TEMPLATE_FOLDER)        
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER     
app.config['REDIS_URL'] = REDIS_URL   
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=EXPIRE_DAYS)
app.config.from_object(dbconfig)                # 导入数据库配置文件
db.init_app(app)    # 初始化一个SQLAlchemy对象


# 判断上传的文件是否是允许的后缀
def _allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(404)
def handle_404_error(err):
    return render_template("code404.html")


def download_data():
    print("get_echart call")
    return send_file('static/js/echarts.js', mimetype='text/javascript')


@app.route("/getalldata")
def getalldata():
    id = session.get("id")
    form_file = os.path.join(UPLOAD_FOLDER, id+"_form.json")
    json_file = os.path.join(UPLOAD_FOLDER, id+".json")
    output_file = os.path.join(UPLOAD_FOLDER, id+"js.json")
    generate_response_data(id, form_file, json_file, output_file)
    with open(output_file, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    response = make_response(json.dumps(data, ensure_ascii=False))
    response.mimetype = 'application/json'
    return response


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('uploadfile.html')
    else:
        form_data = request.form.to_dict()  # 获取表单数据
        file = request.files.get('file')  # 获取文件
        if file and _allowed_file(file.filename):
            user_id = session.get('id')
            with open(os.path.join(app.config['UPLOAD_FOLDER'], user_id+"_form.json"), 'w') as f: 
                json.dump(form_data, f, indent=4)    # 保存表单
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], user_id+".csv"))  # 保存文件
            prerprocess(id=session.get("id"), folder_path=UPLOAD_FOLDER)
            return redirect(url_for('index'))
        else:
            data = {"Failed": True, "Message": "Type of file is not allowed."}
            response = make_response(json.dumps(data, ensure_ascii=False))
            response.mimetype = 'application/json'
            return response


@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/streamResponse", methods=['post'])
def streamResponse():
    user_req = json.loads(request.data)
    server_req = createChatCompletion(session.get("id"), user_req=user_req)
    
    model_res = get_model_response(server_req)
    server_res = Response(createStream(session.get("id"), model_res),content_type='text/html')
    return server_res


# 启动一个本地开发服务器，激活该网页
if __name__ == '__main__':
    app.add_url_rule(rule='/login', view_func=Login.as_view('login'))
    app.run(host=SERVER_IP, debug=True)
