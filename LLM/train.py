import os
import bitsandbytes as bnb

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, BitsAndBytesConfig
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, PeftModel, TaskType, PeftConfig

# 检查是否有GPU可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Bitsandbytes config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# 加载微调前的模型和tokenizer
model_name = "THUDM/glm-4-9b-chat"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map='auto',
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# for name, module in model.named_modules():
#     print(name)

# 量化模型不支持直接进行微调,使用PEFT进行微调(LoRA)
peft_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=['self_attention.query_key_value'],
    lora_dropout=0.05,
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, peft_config)


train_dataset = load_dataset("json", data_files="jsondata\\data_1.json")['train']

# 定义训练参数
training_args = TrainingArguments(
    output_dir='.\\output',  # 模型输出路径
    num_train_epochs=1,  # 训练周期
    per_device_train_batch_size=1,  # 每个设备上的批量大小，减小显存占用
    gradient_accumulation_steps=8,  # 梯度累积步数
    learning_rate=5e-5,  # 学习率
    fp16=True,  # 混合精度训练（减少显存占用）
    logging_dir='.\\logs',  # 日志路径
    logging_steps=10,  # 日志记录频率
    save_steps=500,  # 保存模型频率
    save_total_limit=2,  # 最多保存模型数量
    load_best_model_at_end=False,
    save_strategy="steps"
)


# 定义数据处理函数，将输入文本转换为模型输入
def preprocess_function(examples):
    inputs = tokenizer(examples['input'], padding="max_length", truncation=True, max_length=512)
    labels = tokenizer(examples['target'], padding="max_length", truncation=True, max_length=512)
    inputs["labels"] = labels["input_ids"]
    return inputs


# 处理数据集
tokenized_dataset = train_dataset.map(preprocess_function, batched=True)

# 使用Trainer进行训练
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer
)

# 开始训练
trainer.train()

# 保存模型
trainer.save_model('.\\output')
