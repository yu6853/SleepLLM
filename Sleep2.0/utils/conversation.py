from datetime import datetime
from db.historys import get_history, insert_history, update_history
import json
import requests


MODEL_URL = "http://localhost:8000/v1/chat/completions"     # 配置Chat服务地址
PROMPT_PATH = "D:\pythonProject\Sleep\media\Prompt.txt"     # 配置提示词文件地址
MAX_CONTEXT_LEN = 5                     # 配置最大上下文长度


def generate_input(gender,
                   age,
                   occupation,
                   duration, 
                   quality,
                   stress,
                   breath,
                   heartrate,
                   step,
                   disorder):
    return {"role": "user",
            "message": ("性别{}，职业{}，年龄{}岁，" + \
                        "睡眠质量得分{}（满分10分），" + \
                        "压力指数得分{}（满分10分），" + \
                        "呼吸率{}，心率{}，每日步数{}，" + \
                        "睡眠时长{}小时，{}。").format(
                            gender, occupation, age, \
                            quality, stress, \
                            breath, heartrate, step, duration, disorder
                        )
            }


def _encapsule_message(role, content):
    return {
        "role": role,
        "content": content
    }


def _get_history(id):
    ret = list()
    lines = get_history(id=id, conversation_len=MAX_CONTEXT_LEN)
    for line in lines:
        ret.append(_encapsule_message(role="user", content=line.user))
        ret.append(_encapsule_message(role="assistant", content=line.assistant))
    return ret


def _get_system_prompt():
    with open(PROMPT_PATH, 'r', encoding="utf8") as f:
        system_prompt = f.read()
    return _encapsule_message(role="system", content=system_prompt)


def createChatCompletion(id, user_req):
    messages = list()
    messages.append(_get_system_prompt())       # 系统提示
    messages.extend(_get_history(id=id))        # 历史记录
    messages.append(_encapsule_message(role="user", content=user_req["message"]))   # 用户请求

    insert_history(id=id, num=datetime.now())
    update_history(id=id, role="user", message=user_req["message"])

    server_req = {
        "model": "ChatGLM2-6B",
        "messages": messages,
        "temperature": 0,
        "top_p": 0,
        "max_length": 1024,
        "stream": "true"
    }
    print(server_req)
    return server_req


def createStream(model_res):
    model_res = model_res.content.decode()
    # print(model_res)
    lines = model_res.split("\r\n\r\n")
    lines = [line.strip() for line in lines]
    lines.pop(0)    # {"role": "assistent"}
    for chunk in lines:
        chunk = chunk.replace("data: ", "")
        chunk = json.loads(chunk)
        # print(chunk)
        mychoice = chunk['choices'][0]
        if mychoice.get("finish_reason") is None:   # 判断是否结束
            content = mychoice['delta']['content']
            yield content
        else:
            break


def processStream(model_res):
    sum_content = ""
    for content in createStream(model_res):
        sum_content += content
    return sum_content


def get_model_response(id, server_req):
    model_res = requests.post(url=MODEL_URL, json=server_req)

    # 更新对话记录
    update_history(id=id, role="assistant", message=processStream(model_res))

    return model_res
