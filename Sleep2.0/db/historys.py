from datetime import datetime
from db.tables import db


class Historys(db.Model):
    __tablename__ = "Historys"
    id = db.Column(db.String(8), primary_key=True)
    num = db.Column(db.DateTime, default=datetime.now, primary_key=True)
    user = db.Column(db.String(1024), default="")
    assistant = db.Column(db.String(1024), default="")


# 更新最新一条对话记录
def update_history(id, role, message):
    db.session.begin()
    # 查询数据库
    history = Historys.query.filter(Historys.id == id) \
                            .order_by(Historys.num.desc()) \
                            .first()     
    if role.lower() == "user":
        history.user = message
    elif role.lower() == "assistant":
        history.assistant = message
    db.session.commit()
    db.session.close()


# 插入一条对话记录
def insert_history(id, num, user="", assistant=""):
    db.session.begin()
    history = Historys(id=id, num=num, user=user, assistant=assistant)  # 创建Historys表的一个记录
    db.session.add(history)
    db.session.commit()
    db.session.close()


# 获取对话记录
def get_history(id, conversation_len):
    db.session.begin()
    lines = Historys.query.filter(Historys.id == id) \
                          .order_by(Historys.num.desc()) \
                          .limit(conversation_len) \
                          .all()
    lines.reverse()
    db.session.close()
    return lines


# 清空对话记录
def clear_history(id):
    raise NotImplementedError
