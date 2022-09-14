import os
import sqlite3
import subprocess
from tkinter import *
from tkinter import filedialog

# from tkinter.filedialog import askopenfilename
import my_icon


def get_base(backup, pass_code):
    path_tmp = "tmp\\"
    for f in os.listdir(path_tmp):
        os.remove(os.path.join(path_tmp, f))
    cmd = 'signalbackup-tools_win.exe ' + backup + ' ' + pass_code + ' --output ' + path_tmp
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    txt.configure(state='normal')
    txt.insert(2.0, "process finished!\n")
    txt.configure(state='disabled')
    return "tmp\\database.sqlite"


def get_file_path():
    # filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    # widget.insert(0, filename)
    # print(widget.get())
    ftypes = [('Backup файлы', '*.backup'), ('Все файлы', '*')]
    dlg = filedialog.Open(filetypes=ftypes)
    fl = dlg.show()
    entry_filename.insert(0, fl.replace("/", "\\"))


def get_data(base):
    conn = sqlite3.connect(base)
    c = conn.cursor()
    c.execute("SELECT * FROM sms")

    rows = c.fetchall()
    for row in rows:
        print(row)
    # conn.commit()
    conn.close()


def make_result(data):
    pass


def main():
    pass_code = "486746075681940264135041361970"
    # get_data(get_base(file_path, pass_code))
    root = Tk()
    root.title('SignalBackupParser 0.9b')
    root.geometry('600x400')
    icon = my_icon.set_icon()
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(data=icon))
    root.resizable(False, False)
    global entry_filename
    entry_filename = Entry(root, width=45, font='arial 9')
    entry_filename.grid(row=0, column=0, padx=5, pady=5)
    entry_filename.insert(0, "Укажите путь к файлу или нажмите открыть")

    # entry_filename.configure(state=DISABLED)

    def on_click(event):
        # entry_filename.configure(state=NORMAL)
        entry_filename.delete(0, END)

    entry_filename.bind("<Button-1>", on_click)

    button_open = Button(root, text=u'Открыть', width=15, height=1, bg='#19dae0', fg='white',
                         font='arial 9 bold', command=get_file_path)
    button_open.grid(row=0, column=1, padx=5, pady=5)
    global txt
    txt = Text(root, width=55, height=18, font='arial 9', state='disabled')
    txt.grid(row=1, column=0, columnspan=2, padx=5, pady=(20, 20))
    btn_2 = Button(root, text='Анализ', width=8, height=1, bg='#19dae0', fg='white', font='arial 14',
                   command=lambda: get_data(get_base(file_path, pass_code)))
    btn_2.grid(row=3, column=0, columnspan=2, padx=10)
    m_lbl = Label(root, text='© VKukh', font='arial 7', fg='#999999', justify=LEFT)
    m_lbl.grid(row=4, column=0, columnspan=2)

    root.mainloop()


if __name__ == '__main__':
    main()
