import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re
import tkinter as tk
from tr import tr
from en import en

lang = tr  # Default language

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()
        self.master.geometry(self.center_window(600, 250))  # Başlangıç penceresi boyutları

    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        return f'{width}x{height}+{x}+{y}'

    def create_widgets(self):
        self.left_frame = tk.Frame(self, width=200)
        self.left_frame.grid(row=0, column=0, sticky="ns")
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.buttons = [
            (lang["system_info"], "sys_info"),
            (lang["cpu_info"], "cpu_info"),
            (lang["mem_info"], "mem_info"),
            (lang["swap_info"], "swap_info"),
        ]

        self.create_buttons()

        # Language change button
        self.lang_button = tk.Button(self.left_frame, text="English" if lang == tr else "Türkçe", command=self.toggle_language)
        self.lang_button.pack(fill='x', pady=5)

        self.system_information("sys_info")

    def create_buttons(self):
        for text, info_type in self.buttons:
            button = tk.Button(self.left_frame, text=text, command=lambda t=info_type: self.display_info(t))
            button.pack(fill='x', pady=5)

    def toggle_language(self):
        global lang
        lang = en if lang == tr else tr
        self.update_ui()

    def update_ui(self):
        # Update button texts
        for widget in self.left_frame.winfo_children():
            widget.destroy()  # Remove old buttons

        self.create_buttons()
        self.lang_button = tk.Button(self.left_frame, text="English" if lang == tr else "Türkçe", command=self.toggle_language)
        self.lang_button.pack(fill='x', pady=5)

        # Update the right frame with the current info type
        self.display_info("sys_info")

    def display_info(self, info_type):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.system_information(info_type)

    def system_information(self, info_type):
        row = 0
        def add_label(text, column=0, span=1):
            nonlocal row
            label = tk.Label(self.right_frame, text=text, font=('Arial', 12), fg='Black')
            label.grid(row=row, column=column, columnspan=span, sticky='w')
            row += 1

        if info_type == "sys_info":
            add_label(lang["sys_information"], span=2)
            uname = platform.uname()
            add_label(f"{lang['system']}: {uname.system}")
            add_label(f"{lang['node_name']}: {uname.node}")
            add_label(f"{lang['release']}: {uname.release}")
            add_label(f"{lang['version']}: {uname.version}")
            add_label(f"{lang['machine']}: {uname.machine}")
            add_label(f"{lang['processor']}: {cpuinfo.get_cpu_info()['brand_raw']}")
            add_label(f"{lang['ip_address']}: {socket.gethostbyname(socket.gethostname())}")
            add_label(f"{lang['mac_address']}: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")

        elif info_type == "cpu_info":
            add_label(lang["cpu_info"], span=2)
            add_label(f"{lang['physical_cores']}: {psutil.cpu_count(logical=False)}")
            add_label(f"{lang['total_cores']}: {psutil.cpu_count(logical=True)}")
            cpufreq = psutil.cpu_freq()
            add_label(f"{lang['max_freq']}: {cpufreq.max:.2f}Mhz")
            add_label(f"{lang['min_freq']}: {cpufreq.min:.2f}Mhz")
            add_label(f"{lang['current_freq']}: {cpufreq.current:.2f}Mhz")

        elif info_type == "mem_info":
            add_label(lang["mem_info"], span=2)
            svmem = psutil.virtual_memory()
            add_label(f"{lang['total']}: {get_size(svmem.total)}")
            add_label(f"{lang['available']}: {get_size(svmem.available)}")
            add_label(f"{lang['used']}: {get_size(svmem.used)}")
            add_label(f"{lang['percentage']}: {svmem.percent}%")

        elif info_type == "swap_info":
            add_label(lang["swap_info"], span=2)
            swap = psutil.swap_memory()
            add_label(f"{lang['total']}: {get_size(swap.total)}")
            add_label(f"{lang['free']}: {get_size(swap.free)}")
            add_label(f"{lang['used']}: {get_size(swap.used)}")
            add_label(f"{lang['percentage']}: {swap.percent}%")

if __name__ == "__main__":
    root = tk.Tk()
    root.title(lang["title"])
    root.iconbitmap("sys_info.ico")
    app = Application(master=root)
    app.mainloop()
