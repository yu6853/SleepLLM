from flask import views
from flask import render_template, redirect, make_response, url_for
from flask import session, request
from db.passwords import get_password
import json


class Login(views.MethodView):
    def __init__(self):
        super(Login, self).__init__()

    def get(self):
        return render_template("login.html")

    def post(self):
        id = request.form.get('id')
        pwd = request.form.get('pwd')
        ret = get_password(id=id)
        if ret is not None and ret.pwd == pwd:
            session.permanent = True
            session['id'] = id
            return redirect(url_for('upload'))
        else:
            data = {"Failed": True, "Message": "Authentication Failed."}
            response = make_response(json.dumps(data, ensure_ascii=False))
            response.mimetype = 'application/json'
            return response
