import Program
import tkinter as tk
from tkinter import messagebox



def gui():
    root_window = tk.Tk()
    root_window.title("McPing")
    root_window.geometry("200x350")
    root_window.resizable(True, True)

    # 检查文件的状态
    def check_ip():
        flag = True
        if Program.CheckIP() == False:
            inp = messagebox.askyesno(title="缺失ip.yaml文件", message="是否下载")
            if inp:
                try:
                    Program.Download()
                except:
                    messagebox.showinfo(title="失败", message="请尝试手动下载")
                    flag = False
                    root_window.destroy()
                if flag:
                    messagebox.showinfo(title="成功！", message="成功！")
            else:
                messagebox.showinfo(title="", message="请尝试手动下载")
                root_window.destroy()

    def ping():
        flag = True
        try:
            Program.ping_write()
        except:
            messagebox.showinfo(title="失败", message="失败")
            flag = False
        if flag:
            messagebox.showinfo(title="成功！", message="成功！")

    def update():
        flag = True
        try:
            Program.Download()

        except:
            messagebox.showinfo(title="失败",message="请尝试手动下载ip.yaml文件")
            flag = False
        if flag:
            messagebox.showinfo(title="成功",message="成功")

    def print_result():
        top_window = tk.Toplevel()
        top_window.title("结果")

        top_window.resizable(True,True)
        text = tk.Text(top_window,width=50)

        text.grid(padx=0)
        text.insert("insert",chars=Program.read_return())
        top_window.mainloop()

    def write():
        messagebox.showinfo(title="施工中",message="悲")


    check_ip()
    Program.mk_output()

    button_update = tk.Button(text="更新", pady=20, padx=50, command=update).pack()
    button_ping = tk.Button(text="检测", pady=20, padx=50, command=ping).pack()
    button_print = tk.Button(text="展示", pady=20, padx=50,command=print_result).pack()
    button_write = tk.Button(text="写入", pady=20, padx=50,command=write).pack()
    button_exit = tk.Button(text="退出", pady=20, padx=50, command=root_window.destroy).pack()

    root_window.mainloop()
