from utils.conversation import generate_input, createChatCompletion, get_model_response, processStream
from datetime import date
import json


# 处理参数
heart_rate_range = [[50, 70], [60, 70], [45, 50]]   # 男/女/老人、经常运动的人睡眠时正常心率范围
resipration_rate_range = [12, 20]   # 睡眠时正常呼吸率范围
sleep_time_range = [25200, 32400]   # 正常睡眠时长范围
colors = ["#FDDD60", "#10E117", "#FF6E76"]  # 过慢/正常/过快对应的颜色


def _get_sleep_quality(data):
    def sleep_duration_score(sleep_duration):
        if sleep_duration > 7 * 3600:
            return 0
        elif sleep_duration > 6 * 3600:
            return 1
        elif sleep_duration > 5 * 3600:
            return 2
        else:
            return 3
    
    def sleep_efficiency_score(sleep_efficiency):
        if sleep_efficiency > 0.85:
            return 0
        elif sleep_efficiency > 0.75:
            return 1
        elif sleep_efficiency > 0.65:
            return 2
        else:
            return 3
        
    def fall_asleep_time_score(fall_asleep_time):
        if fall_asleep_time is None:
            return 3
        if fall_asleep_time <= 15 * 60:
            return 0
        elif fall_asleep_time <= 30 * 60:
            return 1
        elif fall_asleep_time <= 60 * 60:
            return 2
        else:
            return 3
        
    def sleep_quality_score(sleep_quality):
        if sleep_quality < 2:
            return 3
        elif sleep_quality < 4:
            return 2
        elif sleep_quality < 6:
            return 1
        else:
            return 0
    
    def sleep_disorder_score(sleep_disorder, wake_up_times, apnea_count):
        score = 0
        if sleep_disorder != "无": score += 1
        if wake_up_times != 0: score += 1
        if apnea_count != 0: score += 1
        return score
        
    form_data, json_data = data
    score = 0
    score += sleep_duration_score(json_data["sleep_duration"])
    score += sleep_efficiency_score(json_data["sleep_efficiency"])
    score += fall_asleep_time_score(json_data["fall_asleep_time"])
    score += sleep_quality_score(int(form_data["sleep_quality"]))
    score += sleep_disorder_score(form_data["disorder"], json_data["wake_up_times"], json_data["apnea_count"])

    score = (15 - score) / 15
    return score


def _get_hms(seconds, formstr="%02d:%02d:%02d"):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)				    
    return (formstr % (h, m, s))


def _get_heartbeat_list(real_time_heart_rate):
    real_time_heart_rate = [int(heart_rate) for heart_rate in real_time_heart_rate if heart_rate]
    heartbeat_list = list()
    date_today = date.today()
    total = len(real_time_heart_rate)
    min_num = heart_rate_range[0][0]
    max_num = heart_rate_range[0][1]
    i = 0
    while i < total:
        sub_list = []
        sub_color = ""
        if real_time_heart_rate[i] < min_num:
            sub_color = colors[0]
            while i < total and real_time_heart_rate[i] < min_num:
                sub_list.append([f"{date_today} {_get_hms(i)}",
                                 real_time_heart_rate[i]])
                i += 1                
        elif real_time_heart_rate[i] > max_num:
            sub_color = colors[2]
            while i < total and real_time_heart_rate[i] > max_num:
                sub_list.append([f"{date_today} {_get_hms(i)}",
                                 real_time_heart_rate[i]])
                i += 1
        else:
            sub_color = colors[1]
            while i < total \
                and real_time_heart_rate[i] >= min_num \
                and real_time_heart_rate[i] <= max_num:
                sub_list.append([f"{date_today} {_get_hms(i)}",
                                 real_time_heart_rate[i]])
                i += 1
        heartbeat_list.append([sub_color, sub_list])
    return heartbeat_list


def _get_breath_list(real_time_respiration_rate):
    real_time_respiration_rate = [int(respiration_rate) for respiration_rate in real_time_respiration_rate if respiration_rate]
    breath_list = list()
    date_today = date.today()
    total = len(real_time_respiration_rate)
    min_num = resipration_rate_range[0]
    max_num = resipration_rate_range[1]
    i = 0

    while i < total:
        sub_list = []
        sub_color = ""
        if real_time_respiration_rate[i] < min_num:
            sub_color = colors[0]
            while i < total and real_time_respiration_rate[i] < min_num:
                sub_list.append([f"{date_today} {_get_hms(i)}",
                                 real_time_respiration_rate[i]])
                i += 1                
        elif real_time_respiration_rate[i] > max_num:
            sub_color = colors[2]
            while i < total and real_time_respiration_rate[i] > max_num:
                sub_list.append([f"{date_today} {_get_hms(i)}",
                                 real_time_respiration_rate[i]])
                i += 1
        else:
            sub_color = colors[1]
            while i < total \
                and real_time_respiration_rate[i] >= min_num \
                and real_time_respiration_rate[i] <= max_num:
                sub_list.append([f"{date_today} {_get_hms(i)}",
                                 real_time_respiration_rate[i]])
                i += 1
        breath_list.append([sub_color, sub_list])
    return breath_list


def _get_onbed_duration(time_in_bed):
    h, m, _ = _get_hms(time_in_bed, formstr="%d:%d:%d").split(":")
    return f"{h}小时{m}分钟"


def _get_sleep_duration(sleep_duration):
    h, m, _ = _get_hms(sleep_duration, formstr="%d:%d:%d").split(":")
    return f"{h}小时{m}分钟"


def _get_action_num(movement_count):
    return f"{movement_count}次"


def _get_snore_num(snoring_count_per_hour):
    return f"{int(snoring_count_per_hour)}次/小时"


def _get_leave_num(bed_exit_count):
    return f"{bed_exit_count}次"


def _get_apnoea_num(apnea_count):
    return f"{apnea_count}次"


def _get_avg_breath_rate(avg_respiration_rate):
    return f"{int(avg_respiration_rate)}次/分"


def _get_avg_heartbeat_rate(avg_heart_rate):
    return f"{int(avg_heart_rate)}次/分"


def _get_sleep_efficency(sleep_efficiency):
    return f"{int(sleep_efficiency*100)}%"


def _get_conversation(id, data):
    form_data, json_data = data
    input_data = generate_input(gender=form_data["gender"],
                                age=form_data["age"],
                                occupation=form_data["profession"],
                                duration=round(json_data["sleep_duration"]/3600,1),
                                quality=form_data["sleep_quality"],
                                stress=form_data["pressure_extent"],
                                breath=round(json_data["avg_respiration_rate"],1),
                                heartrate=round(json_data["avg_heart_rate"],1),
                                step=form_data["step"],
                                disorder=form_data["disorder"])
    server_req = createChatCompletion(id=id, user_req=input_data)
    model_res = get_model_response(id=id, server_req=server_req)
    input_data = input_data["message"]
    model_res = processStream(model_res)
    return {"user": input_data,
            "assistant": model_res}


def generate_response_data(id, form_file, json_file, output_file):
    with open(form_file, "r", encoding="utf8") as f:
        form_data = json.load(f)
    with open(json_file, "r", encoding="utf8") as f:
        json_data = json.load(f)

    js_data = dict()    
    js_data["sleep_quality"] = _get_sleep_quality(data=[form_data, json_data])
    js_data["heartbeat_list"] = _get_heartbeat_list(real_time_heart_rate=json_data["real_time_heart_rate"])
    js_data["breath_list"] = _get_breath_list(real_time_respiration_rate=json_data["real_time_respiration_rate"])
    js_data["onbed_duration"] = _get_onbed_duration(time_in_bed=json_data["time_in_bed"])
    js_data["sleep_duration"] = _get_sleep_duration(sleep_duration=json_data["sleep_duration"])
    js_data["action_num"] = _get_action_num(movement_count=json_data["movement_count"])
    js_data["snore_num"] = _get_snore_num(snoring_count_per_hour=json_data["snoring_count_per_hour"])
    js_data["leave_num"] = _get_leave_num(bed_exit_count=json_data["bed_exit_count"])
    js_data["apnoea_num"] = _get_apnoea_num(apnea_count=json_data["apnea_count"])
    js_data["avg_breath_rate"] = _get_avg_breath_rate(avg_respiration_rate=json_data["avg_respiration_rate"])
    js_data["avg_heartbeat_rate"] = _get_avg_heartbeat_rate(avg_heart_rate=json_data["avg_heart_rate"])
    js_data["sleep_efficency"] = _get_sleep_efficency(sleep_efficiency=json_data["sleep_efficiency"])
    js_data["conversation"] = _get_conversation(id, data=[form_data, json_data])

    with open(output_file, 'w') as js_file:
        json.dump(js_data, js_file, indent=4)


if __name__ == "__main__":
    import os


    id, folder = "10001", "../media"
    json_file = os.path.join(folder, id+".json")
    output_file = os.path.join(folder, id+"js.json")
    generate_response_data(json_file, output_file)
