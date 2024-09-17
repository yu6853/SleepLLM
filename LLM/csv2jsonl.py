import pandas as pd
import json

# 读取CSV数据
df = pd.read_csv('.\\csvfiles\\Sleep_health_and_lifestyle_dataset.csv')

# 将数据转为JSONL格式
with open('.\\output\\data_1.jsonl', 'w', encoding='utf-8') as jsonl_file:
    for index, row in df.iterrows():
        if pd.isna(row['Sleep Disorder']) or row['Sleep Disorder'] == 'None':
            sleep_disorder_info = "没有睡眠障碍"
        else:
            sleep_disorder_info = f"有{row['Sleep Disorder']}睡眠障碍"

        prompt = f"性别{row['Gender']}，职业{row['Occupation']}，{row['Age']}岁，" \
                 f"日常运动量{row['Physical Activity Level']}，压力水平{row['Stress Level']}，" \
                 f"血压{row['Blood Pressure']}，心率{row['Heart Rate']}，" \
                 f"每日步数{row['Daily Steps']}，睡眠时长{row['Sleep Duration']}小时。" \
                 f"{sleep_disorder_info}"

        sleep_quality = row['Quality of Sleep']
        if sleep_quality >= 7:
            sleep_evaluation = "较好"
        elif sleep_quality >= 5:
            sleep_evaluation = "一般"
        else:
            sleep_evaluation = "较差"

        label = f"睡眠质量{sleep_quality}分，{sleep_evaluation}"

        # 将 Prompt 和 Label 写入 JSONL 文件
        jsonl_file.write(json.dumps({"prompt": prompt, "label": label}, ensure_ascii=False) + '\n')

    print("数据转换完成！")
