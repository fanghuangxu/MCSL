import os
import tkinter as tk
import sys
import io
import subprocess
import threading

class RedirectText(io.TextIOBase):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # 滚动到最底部

    def flush(self):
        pass  # flush 方法可以留空

def run_command(command,mcsL_art=None):
    if not mcsL_art:
        mcsL_art = r"""
         M     M    CCCCC     SSSSS     L
        MM   MM    C         S        L
       M M M M    C          SSSSS   L
      M  M  M    C             S   L
     M     M    CCCCC     SSSSS    LLLLL


        MCSL-minecraft serverlauncher 
        """
    print(mcsL_art)

    # 使用 Popen 执行命令并实时输出
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    # 读取输出
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line, end="")  # 输出到 text widget
    process.stdout.close()
    process.wait()  # 等待子进程结束

def on_run_button_click(command,text):

    # 使用线程来运行命令，以避免阻塞主线程
    threading.Thread(target=run_command, args=(command,text), daemon=True).start()
def window(command,title,text=None):
    # 创建主窗口
    root = tk.Tk()
    root.title(title)

    # 创建文本框
    text_box = tk.Text(root, wrap='word', height=20, width=80)
    text_box.pack(expand=True, fill='both')

    # 重定向 stdout 到 Text 控件
    redirected_output = RedirectText(text_box)
    sys.stdout = redirected_output

    # 创建运行按钮
    on_run_button_click(command,text)
    root.mainloop()