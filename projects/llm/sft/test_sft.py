import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoTokenizer,AutoModelForCausalLM,TrainingArguments,Trainer,DataCollatorForLanguageModeling

# 加载数据
def load_data(train_data_path, test_data_path):

    return dataset

# promote模板
def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['input'])):
        text = f"""
            ### Instruction:\n{example['instruction'][i]}\n
            ### Input:\n{example['input'][i]}\n
            ### Response:\n{example['output'][i]}{tokenizer.eos_token}"""
        output_texts.append(text)
    return output_texts

# token编码
def tokenize_function(examples):
    # 注意：不要在这里 return_tensors="pt"，Trainer 会自动处理
    return tokenizer(
        formatting_prompts_func(examples),
        truncation=True,
        max_length=512,
        padding=False,  # 改为动态填充（由 DataCollator 处理）
        add_special_tokens=True,
    )

# 加载模型
def load_model(model_name, device):
    # 加载 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        padding_side="right"
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 加载模型（注意：MPS 不支持 device_map="auto" + float16 同时使用）
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,  # 仅用于加载权重，训练时可能转为 float32
        trust_remote_code=True,
        device_map={"": device},  # 显式指定设备，避免 auto 冲突
    )

    # 启用梯度检查点以节省显存（对大模型至关重要）
    model.gradient_checkpointing_enable()
    return tokenizer, model

def lora_trainer(model, output_dir):
    # 配置 LoRA
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 训练配置
    training_args = TrainingArguments(
        output_dir = output_dir,
        per_device_train_batch_size=1,  # MPS 显存有限，建议从 1 开始
        gradient_accumulation_steps=8,  # 模拟 batch_size=8
        learning_rate=2e-4,
        num_train_epochs=3,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        optim="adamw_torch",
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        weight_decay=0.01,
        # ⚠️ 关键：MPS 不支持 fp16/bf16 训练！
        fp16=False,  # 必须设为 False
        bf16=False,  # 同样不支持
        # 其他 MPS 适配设置
        dataloader_pin_memory=False,  # MPS 不支持 pin_memory
        dataloader_drop_last=True,  # 避免最后小 batch 引发问题
        remove_unused_columns=False,  # 防止 Trainer 删除 input_ids 等字段
        report_to="none",
        ignore_data_skip=True,  # 跳过中断恢复时的数据对齐问题
    )

    # 使用动态填充的 collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
        pad_to_multiple_of=8,  # 可选：对齐到 8 的倍数提升效率
    )

    # 训练
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        data_collator=data_collator,
        tokenizer=tokenizer,  # 传递 tokenizer 用于日志等
    )

    return trainer


if __name__ == '__main__':

    # 检查设备
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    # 加载模型
    model_name = "Qwen/Qwen3-8B"
    tokenizer, model = load_model(model_name, device)

    # 加载数据：
    dataset = load_dataset("csv", data_files={"train": "test_data.csv"})
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset["train"].column_names,
        num_proc=4,  # 可选：多进程加速
    )

    # 开始训练
    trainer = lora_trainer(model, output_dir="./qwen3-8b-lora-sft")
    trainer.train()

    # 保存 LoRA 适配器
    model.save_pretrained("./qwen3-8b-lora-sft-final")
    tokenizer.save_pretrained("./qwen3-8b-lora-sft-final")
