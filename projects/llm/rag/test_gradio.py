import gradio as gr
print(gr.__version__)

def greet(name, age):
    return f"你好, {name}！你今年 {age} 岁。"

# 创建界面
demo = gr.Interface(
    fn=greet,                     # 要包装的函数
    inputs=[gr.Textbox(label="姓名"), gr.Number(label="年龄")],  # 输入组件
    outputs=gr.Textbox(label="问候语")                          # 输出组件
)

# 启动
demo.launch()