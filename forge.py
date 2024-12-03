import os
import requests
import json
import cmd_text_for_tkinter






def get_forge_version(version):
    return requests.get(f"https://bmclapi2.bangbang93.com/forge/minecraft/{version}")
def get_forge_builds(version):
    return get_forge_version("1.21.3").json()[0]["build"]



def install_forge(forge_jar_path):
    
    cmd_text_for_tkinter.window(command=f'cd {forge_jar_path} && java -jar {forge_jar_path}/forge_installer.jar --installServer . --mirror "https://bmclapi2.bangbang93.com/maven/"',title="正在安装Forge",text="正在安装Forge，请耐心等待...")


def run_forge_server(server_path,os_type):
    if os_type == "mac":
        path=f"{server_path}/libraries/net/minecraftforge/forge"
        forge_version=os.listdir(path)[0]
        path=f"{path}/{forge_version}/unix_args.txt"
        with open(server_path+"/run.command","w") as f:
            code=f"""
#!/bin/bash
# 添加自定义 JVM 参数（例如 RAM 分配）到 user_jvm_args.txt
# from the fanghuangxu@163.com

java -jar forge-{forge_version}-shim.jar --onlyCheckJava
if [ $? -ne 0 ]; then
    echo
    echo 如果你在修复上面的错误时遇到困难，请在自述文件中提到的论坛或 Discord 寻求帮助。
    exit 1
fi
cd {server_path}/libraries/net/minecraftforge/forge/{forge_version}
# 在下一行添加自定义程序参数（例如 nogui），在 %* 之前 或直接将它们传递给这个脚本
java @user_jvm_args.txt @libraries/net/minecraftforge/forge/{forge_version}/unix_args.txt "$@"

exit 0
"""
            f.write(code)
        os.system(f"chmod +x {server_path}/run.command")
        os.system(f"cd {server_path} && ./run.command")
    elif os_type == "windows":
        os.system(f"cd {server_path} ; {server_path}/run.bat")

    elif os_type == "linux":
        os.system(f"cd {server_path}")
        os.system(f"{server_path}/run.sh")



# run_forge_server(r"/Volumes/扩展卡/py/python/mcsl/MCSL/servers/我和弟弟电创造服务器",os_type="mac")

        
    