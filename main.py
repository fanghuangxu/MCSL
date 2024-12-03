import os
import tkinter as tk
from tkinter import messagebox
from cml.utils import get_version_list as version_list
import utils
import tkinter.ttk
import download_file
import json
from tkinter import font
import cmd_text_for_tkinter
import webbrowser 
import forge
import lang as language
# import kill





label_font=font.Font(size=12)
current_directory = os.path.dirname(os.path.abspath(__file__))
lang_dir=os.listdir(f"{current_directory}/MCSL/.mcsl/lang")
l=[]
for lang_file in lang_dir:
    l.append(f"{current_directory}/MCSL/.mcsl/lang/{lang_file}")
lang=language.load_lang_file(l)
root = tk.Tk()
lang_mode="en_us"
root.title(lang[lang_mode]["__main__.title"])
root.geometry("400x300")
utils.root.withdraw()

def AddServer():
    utils.clear_widgets(root)
    root.title(lang[lang_mode]["AddServer.title"])
    versions=version_list()
    version=[]
    for x in versions:
        if x['type']=="release":
            version.append(x['id'])
    version_combo = tkinter.ttk.Combobox(root, values=version)
    version_combo.set(lang[lang_mode]["AddServer.version_comb.setTitle"])
    version_combo.pack()
    def cheer_download_Server_jar(server_name):
        
        json_url=""
        version=version_combo.get()
        for v in versions:
            if v['id']==version and v['type']=="release":
                json_url=v["url"]
                list=[]
                list.append(json_url)
                print(list)
                
                download_file.main(urls=list,folder=f'{current_directory}/MCSL/temps/{version_combo.get()}',name=f"{server_name}.json")
                break
        

        # download jar

        with open(f'{current_directory}/MCSL/temps/{version_combo.get()}/{server_name}.json','r') as json_file:
            data=json.load(json_file)

        server_url=data['downloads']['server']['url']
        os.makedirs(f"{current_directory}/MCSL/servers/{server_name.replace('/','')}",exist_ok=True)
        open(f"{current_directory}/MCSL/servers/{server_name}/version.server.txt","w").write(version_combo.get())
        utils.root.deiconify()
        utils.clear_widgets(root)
        l=tk.Label(root,text=lang[lang_mode]["__main__.welcome_text"],font=label_font)
        l.pack()
        root.title(lang["zh_cn"]["__main__.title"])
        utils.download_progress(server_url,f"{current_directory}/MCSL/servers/{server_name}/server.jar") 
        
    server_name_entry=tk.Text(root,height=1,width=20)
    server_name_entry.pack()
    cheer=tkinter.ttk.Button(root, text=lang[lang_mode]["AddServer.Button.text"], command=lambda:cheer_download_Server_jar(server_name_entry.get(1.0,"1.end")))
    cheer.pack()





def ServerList():
    utils.clear_widgets(root)
    root.title(lang[lang_mode]["ServerList.title"])
    l=tk.Label(root,text=lang[lang_mode]["ServerList.Label.text"],font=label_font)
    l.pack()
    server_list=os.listdir(f"{current_directory}/MCSL/servers")
    listbox=tk.Listbox(root,width=20,height=10)
    for server in server_list:
        listbox.insert(tk.END,server)
    listbox.pack()
    def start_server():
        server_name=listbox.get(tk.ACTIVE)
        try:
            with open(f"{current_directory}/MCSL/servers/{server_name}/eula.server.txt","r") as f:
                f.close()
        except FileNotFoundError:
            webbrowser.open("https://aka.ms/MinecraftEULA")
            messagebox.showinfo(lang[lang_mode]["ServerList.info.title"],lang[lang_mode]["ServerList.info.text"])
            with open(f"{current_directory}/MCSL/servers/{server_name}/eula.server.txt","w") as f:
                f.write("eula=true")
        eula="""
#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).
#Wed Nov 27 14:47:44 CST 2024
eula=true
"""
        open(f"{current_directory}/MCSL/servers/{server_name}/eula.txt","w").write(eula)

        cmd_text_for_tkinter.window(f"cd {current_directory}/MCSL/servers/{server_name} && java -Xmx1024M -Xms1024M -jar server.jar","mc服务器控制台")
    start_button=tk.Button(root,text=lang[lang_mode]["ServerList.Button.text"],command=start_server)
    start_button.pack()
def AddForgeToServer():
    utils.clear_widgets(root)
    root.title("服务器列表")
    l=tk.Label(root,text="服务器列表",font=label_font)
    l.pack()
    server_list=os.listdir(f"{current_directory}/MCSL/servers")
    listbox=tk.Listbox(root,width=20,height=10)
    for server in server_list:
        listbox.insert(tk.END,server)
    listbox.pack()
    def add_forge():
        server_name=listbox.get(tk.ACTIVE)
        version=open(f"{current_directory}/MCSL/servers/{server_name}/version.server.txt","r").read()
        build=forge.get_forge_builds(version=version)
        url=[f"https://bmclapi2.bangbang93.com/forge/download/{build}"]
        path=f"{current_directory}/MCSL/servers/{server_name}/"
        if not os.path.exists(path):
            os.makedirs(path)
        download_file.main(url,path,"forge_installer.jar")
        forge.install_forge(f"{current_directory}/MCSL/servers/{server_name}")
    tk.Button(root,text="添加",command=add_forge).pack()
        

# 创建菜单栏
menu_bar = tk.Menu(root)

# 创建服务器菜单
servers_menu = tk.Menu(menu_bar, tearoff=0)
servers_menu.add_command(label=lang[lang_mode]["__main__.servers_meun.text1"], command=AddServer)
servers_menu.add_command(label=lang[lang_mode]["__main__.servers_meun.text2"], command=ServerList)
# 将服务器菜单添加到菜单栏
menu_bar.add_cascade(label=lang[lang_mode]["__main__.meun_bar.text1"], menu=servers_menu)
forge_menu = tk.Menu(menu_bar, tearoff=0)
forge_menu.add_command(label="将Forge添加到服务器", command=AddForgeToServer)
# menu_bar.add_cascade(label="Forge", menu=forge_menu)
# 将菜单栏添加到主窗口
root.config(menu=menu_bar)

l=tk.Label(root,text=lang[lang_mode]["__main__.welcome_text"],font=label_font)
l.pack()

# 运行主循环
root.mainloop()


utils.root.destroy()