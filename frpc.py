def run_frpc(frpcpath, frpcconfpath):
    import cmd_text_for_tkinter
    cmd_text_for_tkinter.window(command=f"{frpcpath} -c {frpcconfpath}", title="frpc内网穿透")