from os import PathLike
import os
import csv
import json


# 处理参数
min_sleep_time = 60  # 60秒
min_active_interval = 5  # 5秒
min_snore_interval = 2  # 2秒
min_apnea_interval = 2  # 呼吸暂停的最小间隔时间为2秒
min_movement_interval = 5  # 5秒
min_bed_exit_interval = 5  # 5秒


def _load_csv_file(csv_file):
    # 读取 CSV 文件，跳过标题行
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            data.append([int(row[0]), float(row[1]), float(row[2])])
    return data


# 在床时间
def _get_time_in_bed(data):
    in_bed = [(row[0] != 1) and (row[0] != 4) for row in data]
    valid_times = []
    count = 0
    for i in range(len(in_bed)):
        if in_bed[i]:
            count += 1
        else:
            if count >= min_bed_exit_interval:
                valid_times.append(count)
            count = 0
    if count >= min_bed_exit_interval:
        valid_times.append(count)
    return sum(valid_times)


# 睡眠时长
def _get_sleep_duration(data):
    sleeping = [(row[0] != 1) and (row[0] != 2) and (row[0] != 4)for row in data]
    valid_sleep_times = []
    count = 0
    beg, ed = -1, -1
    for i in range(len(sleeping)):
        if sleeping[i]:
            ed = i
        else:
            if ed - beg >= min_sleep_time:
                valid_sleep_times.append((beg, ed))
                count += ed - beg
            beg = i
    if ed - beg >= min_sleep_time:
        valid_sleep_times.append((beg, ed))
    return count, valid_sleep_times


# 体动次数
def _get_movement_count(data):
    movement = [row[0] == 2 for row in data]  # 获取状态为体动的布尔列表
    valid_movement_counts = 0  # 有效体动次数
    last_movement_time = -min_movement_interval  # 用于存储上一次有效体动的时间，初始化为一个负值

    for i in range(len(movement)):
        if movement[i]:  # 当前状态为体动
            # 仅在当前体动的时间与上一次有效体动的时间间隔大于等于5秒时，才计为新的体动
            if i - last_movement_time >= min_movement_interval:
                valid_movement_counts += 1  # 计入一次有效体动
            last_movement_time = i  # 更新上一次有效体动的时间为当前的i
        # 这里不需要 else，因为如果不是体动，继续遍历即可
    return valid_movement_counts


# 打鼾次数
def _get_snoring_count_per_hour(data):
    # 打鼾次数
    snoring = [row[0] == 5 for row in data]
    movement = [row[0] == 2 for row in data]  # 获取状态为体动的布尔列表
    # sleeping = [(row[0] != 1) and (row[0] != 2) and (row[0] != 4) for row in data]
    # count = 0
    # sleep_started = False
    valid_snoring_counts = 0  # 有效打鼾次数
    last_snore_time = -min_snore_interval  # 用于存储上一次有效体动的打鼾，初始化为一个负值

    # 检查有效的打鼾次数
    for i in range(len(snoring)):
        # # 判断是否进入了有效的睡眠状态（即连续睡眠超过60秒）
        # if sleeping[i]:  # 在床、打鼾、弱呼吸状态视为睡眠
        #     count += 1
        #     if count >= min_sleep_time:  # 进入有效的睡眠状态
        #         sleep_started = True
        # else:
        #     count = 0
        #     sleep_started = False  # 退出睡眠状态

        # # 如果没有进入有效睡眠状态，跳过打鼾检测
        # if not sleep_started:
        #     continue

        # 如果进入了有效睡眠状态，继续统计打鼾次数
        if snoring[i]:
            # 检查前后6秒是否有体动，若有则不计入打鼾
            if (i >= 6 and any(movement[j] for j in range(i - 6, i))) or (
                    i <= len(data) - 7 and any(movement[j] for j in range(i + 1, i + 7))):
                continue
            
            # 仅在当前打鼾的时间与上一次有效打鼾的时间间隔大于等于2秒时，才计为新的打鼾
            if i - last_snore_time >= last_snore_time:
                valid_snoring_counts += 1  # 计入一次有效打鼾
            last_snore_time = i  # 更新上一次有效打鼾的时间为当前的i
        # 这里不需要 else，因为如果不是打鼾，继续遍历即可

    # # 过滤打鼾次数
    # if valid_snoring_counts < 10:
    #     snoring_filtered.append(0)  # 打鼾少于10次
    # elif valid_snoring_counts <= 30:
    #     snoring_filtered.append(1)  # 打鼾少于等于30次
    # elif valid_snoring_counts <= 200:
    #     snoring_filtered.append(2)  # 打鼾少于等于200次
    # else:
    #     snoring_filtered.append(3)  # 打鼾超过200次
    return valid_snoring_counts


# 离床次数
def _get_bed_exit_count(data):
    bed_exit = [row[0] == 1 for row in data]
    valid_bed_exit_counts = []
    count = 0
    beg, ed = -1, -1

    for i in range(len(bed_exit)):
        if bed_exit[i]:
            ed = i
        else:
            if ed - beg >= min_bed_exit_interval:
                valid_bed_exit_counts.append((beg, ed))
            beg = i

    # 检查结束时的计数
    if ed - beg >= min_bed_exit_interval:
        valid_bed_exit_counts.append((beg, ed))
    return len(valid_bed_exit_counts), valid_bed_exit_counts


# 呼吸暂停次数
def _get_apnea_count(data):
    apnea = [row[0] == 3 for row in data]  # 假设状态3表示呼吸暂停
    apnea_count = 0  # 呼吸暂停次数
    last_apnea_time = -min_apnea_interval  # 用于存储上一次呼吸暂停的时间，初始化为一个负值

    # 遍历每一秒的数据
    for i in range(len(apnea)):
        if apnea[i]:  # 当前秒是呼吸暂停状态
            # 如果当前呼吸暂停和上一次呼吸暂停的间隔大于等于2秒，则计为新的呼吸暂停
            if i - last_apnea_time >= min_apnea_interval:
                apnea_count += 1
            # 更新上一次呼吸暂停的时间
            last_apnea_time = i
    return apnea_count


# 心率和呼吸率
def _get_heart_and_respiration_rate(data):
    minutes = (len(data) + 59) // 60  # 计算分钟数
    minute_heart_rate = [0] * minutes
    minute_respiration_rate = [0] * minutes
    minute_counts = [0] * minutes
    # 计算每分钟的心率和呼吸率
    for i in range(len(data)):
        minute = i // 60
        # 统计每分钟的心率和呼吸率
        minute_heart_rate[minute] += data[i][1]
        minute_respiration_rate[minute] += data[i][2]
        minute_counts[minute] += 1

    # 计算每分钟的平均心率和呼吸率
    for i in range(minutes):
        if minute_counts[i] > 0:
            minute_heart_rate[i] /= minute_counts[i]
            minute_respiration_rate[i] /= minute_counts[i]

    # 零值处理：如果某分钟有离床状态，则该分钟心率/呼吸率设置为零
    for i in range(minutes):
        if any(row[0] == 1 for row in data[i * 60:(i + 1) * 60]):
            minute_heart_rate[i] = 0  # 心率进行零值处理
            minute_respiration_rate[i] = 0  # 呼吸率进行零值处理

    # 替换心率/呼吸率中的零值为前一个非零值
    for i in range(1, minutes):
        if minute_heart_rate[i] == 0:
            if minute_heart_rate[i - 1] is not None:  # 确保前一个值不是 None
                minute_heart_rate[i] = minute_heart_rate[i - 1]
        if minute_respiration_rate[i] == 0:
            if minute_respiration_rate[i - 1] is not None:
                minute_respiration_rate[i] = minute_respiration_rate[i - 1]

    # 处理前导零
    for i in range(minute - 1, -1, -1):
        if minute_heart_rate[i] == 0:
            if i + 1 < len(minute_heart_rate):
                minute_heart_rate[i] = minute_heart_rate[i + 1]
        if minute_respiration_rate[i] == 0:
            if i + 1 < len(minute_respiration_rate):
                minute_respiration_rate[i] = minute_respiration_rate[i + 1]

    # 平滑滤波函数
    def smooth(series, window):
        smoothed = []
        for i in range(len(series)):
            valid_series = [x for x in series[max(0, i - window + 1):i + 1] if x is not None]
            if valid_series:
                smoothed.append(sum(valid_series) / len(valid_series))
            else:
                smoothed.append(0)  # 如果没有有效数据，则设为 0
        return smoothed

    # 应用平滑滤波
    minute_heart_rate = smooth(minute_heart_rate, 5)
    minute_respiration_rate = smooth(minute_respiration_rate, 5)  # 呼吸率平滑处理，但不考虑离床状态

    # 重新将所有应为零的心率/呼吸率点置零
    for i in range(minutes):
        if any(row[0] == 1 for row in data[i * 60:(i + 1) * 60]):
            minute_heart_rate[i] = 0
            minute_respiration_rate[i] = 0

    # 计算去掉零的部分后的平均心率（考虑离床状态）
    filtered_heart_rate = [x for x in minute_heart_rate if x > 0]
    avg_heart_rate = sum(filtered_heart_rate) / len(filtered_heart_rate) if len(filtered_heart_rate) > 0 else 0.0

    # 计算平均呼吸率（考虑离床状态）
    filtered_respiration_rate = [x for x in minute_respiration_rate if x > 0]
    avg_respiration_rate = sum(filtered_respiration_rate) / len(filtered_respiration_rate) if len(filtered_respiration_rate) > 0 else 0.0

    return minute_heart_rate, \
        minute_respiration_rate, \
        avg_heart_rate, \
        avg_respiration_rate


# 计算睡眠效率
def _get_sleep_efficiency(sleep_duration, time_in_bed):
    return sleep_duration / time_in_bed if time_in_bed > 0 else 0.0


# 计算夜间醒来次数
def _get_wake_up_times(sleep_duration_beg_ed, beg_exit_beg_ed):
    count = 0
    for bebe in beg_exit_beg_ed:
        bbeg, bed = bebe
        for i in range(len(sleep_duration_beg_ed)-1):
            # print(sleep_duration_beg_ed[i])
            # print(sleep_duration_beg_ed[i+1])
            # print((bbeg, bed))
            _, sed1 = sleep_duration_beg_ed[i]
            sbeg2, _ = sleep_duration_beg_ed[i+1]
            if sed1 < bbeg and bed < sbeg2:
                count += 1
                break
    return count


def _get_fall_asleep_time(sleep_duration_beg_ed):
    if len(sleep_duration_beg_ed) == 0: return None
    else: return sleep_duration_beg_ed[0][0]


# 生成json文件
def _generate_json(time_in_bed: int,
                   sleep_duration: int,
                   movement_count: int,
                   snoring_count_per_hour: int,
                   bed_exit_count: int,
                   apnea_count: int,
                   avg_respiration_rate: float,
                   avg_heart_rate: float,
                   sleep_efficiency: float,
                   real_time_heart_rate: list,
                   real_time_respiration_rate: list,
                   output_file: PathLike,
                   wake_up_times: list,
                   fall_asleep_time: int):
    json_data = {
        'time_in_bed': time_in_bed,
        'sleep_duration': sleep_duration,
        'movement_count': movement_count,
        'snoring_count_per_hour': snoring_count_per_hour,
        'bed_exit_count': bed_exit_count,
        'apnea_count': apnea_count,
        'avg_respiration_rate': avg_respiration_rate,
        'avg_heart_rate': avg_heart_rate,
        'sleep_efficiency': sleep_efficiency,
        'real_time_heart_rate': real_time_heart_rate,
        'real_time_respiration_rate': real_time_respiration_rate,
        'wake_up_times': wake_up_times,
        'fall_asleep_time': fall_asleep_time
    }
    # 输出到 JSON 文件
    with open(output_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def prerprocess(id, folder_path="media"):
    csv_file = os.path.join(folder_path, id+".csv")
    data = _load_csv_file(csv_file)

    time_in_bed = _get_time_in_bed(data)
    sleep_duration, sleep_duration_beg_ed = _get_sleep_duration(data)
    movement_count = _get_movement_count(data)
    snoring_count_per_hour = _get_snoring_count_per_hour(data)
    bed_exit_count, bed_exit_beg_ed = _get_bed_exit_count(data)
    apnea_count = _get_apnea_count(data)
    real_time_heart_rate, real_time_respiration_rate, \
    avg_heart_rate, avg_respiration_rate = _get_heart_and_respiration_rate(data)
    sleep_efficiency = _get_sleep_efficiency(sleep_duration=sleep_duration,
                                             time_in_bed=time_in_bed)
    wake_up_times = _get_wake_up_times(sleep_duration_beg_ed, bed_exit_beg_ed)
    fall_asleep_time = _get_fall_asleep_time(sleep_duration_beg_ed)
    
    output_file = os.path.join(folder_path, id+".json")
    _generate_json(time_in_bed=time_in_bed,
                   sleep_duration=sleep_duration,
                   movement_count=movement_count,
                   snoring_count_per_hour=snoring_count_per_hour,
                   bed_exit_count=bed_exit_count,
                   apnea_count=apnea_count,
                   avg_respiration_rate=avg_respiration_rate,
                   avg_heart_rate=avg_heart_rate,
                   sleep_efficiency=sleep_efficiency,
                   real_time_heart_rate=real_time_heart_rate,
                   real_time_respiration_rate=real_time_respiration_rate,
                   output_file=output_file,
                   wake_up_times=wake_up_times,
                   fall_asleep_time=fall_asleep_time)


if __name__ == "__main__":
    UPLOAD_FOLDER = "../media"
    prerprocess(id="10002", folder_path=UPLOAD_FOLDER)
