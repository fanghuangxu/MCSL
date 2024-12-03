import subprocess
import os
import signal

def get_java_process_using_port(port):
    try:
        # 运行 lsof 命令获取占用指定端口的进程信息
        result = subprocess.check_output(['lsof', '-i', f':{port}']).decode('utf-8')
        
        # 解析输出，找到 PID
        lines = result.splitlines()
        if len(lines) > 1:
            # 如果有结果，第二行包含进程信息
            process_info = lines[1].split()
            pid = int(process_info[1])  # 提取 PID
            return pid
        else:
            print("没有找到占用该端口的进程。")
            return None
    except subprocess.CalledProcessError:
        print("调用 lsof 时出错，可能没有找到任何进程。")
        return None

def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)  # 优雅地终止进程
        print(f"进程 {pid} 已被终止。")
    except ProcessLookupError:
        print(f"进程 {pid} 不存在。")
    except Exception as e:
        print(f"终止进程时出错: {e}")

def kill_java_process_using_port(port):
    pid = get_java_process_using_port(port)
    if pid:
        kill_process(pid)


def kill_processes(file):
    try:
        # 运行 lsof 命令获取占用指定端口的进程信息
        result = subprocess.check_output(['lsof',  f'{file}']).decode('utf-8')
        
        # 解析输出，找到 PID
        lines = result.splitlines()
        if len(lines) > 1:
            # 如果有结果，第二行包含进程信息
            process_info = lines[1].split()
            pid = int(process_info[1])  # 提取 PID
            os.kill(pid, signal.SIGTERM)  # 优雅地终止进程
        else:
            print("没有找到占用该端口的进程。")
            return None
    except subprocess.CalledProcessError:
        print("调用 lsof 时出错，可能没有找到任何进程。")
        return None
    
kill_java_process_using_port(25565)