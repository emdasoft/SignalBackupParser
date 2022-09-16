import os
import sqlite3
import subprocess
from tkinter import *
from tkinter import filedialog, ttk
import xlsxwriter as xlsxwriter
import my_icon
import tkinter.messagebox as mb


def get_data(row):
    types = {'10485780': 'Входящее сообщение',
             '10485783': 'Исходящее сообщение',
             '2': 'Исходящий звонок',
             '1': 'Входящий звонок',
             '2097684': 'Сервисное сообщение',
             '3': 'Пропущенный аудиозвонок',
             '2097156': 'Сервисное сообщение',
             '10': 'Входящий видеозвонок',
             '11075604': 'Сервисное сообщение',
             '14680084': 'Сервисное сообщение',
             '14680087': 'Сервисное сообщение',
             '7': 'Сервисное сообщение',
             '8': 'Пропущенный видеозвонок',
             }
    sms_id = row[0]
    address = row[1]
    date = row[2]
    date_sent = row[3]
    if row[4] == 1:
        read_state = 'Прочитанное'
    else:
        read_state = 'Непрочитанное'
    direction = types[str(row[5])]
    body = row[6]
    server_guid = row[7]
    recipient_phone = row[8]
    recipient_system_display_name = row[9]
    recipient_signal_profile_name = row[10]
    data = (
        sms_id, address, recipient_system_display_name, recipient_signal_profile_name, recipient_phone, date,
        date_sent, read_state, direction, body, server_guid
    )
    return data


def make_result(base):
    workbook = xlsxwriter.Workbook('out/Signal.xlsx')
    worksheet_contacts = workbook.add_worksheet('Контакты')

    worksheet_messages = workbook.add_worksheet('Сообщения')
    worksheet_messages.set_column('A:A', 18)
    worksheet_messages.set_column('B:B', 16)
    worksheet_messages.set_column('C:G', 30)
    worksheet_messages.set_column('H:H', 17)
    worksheet_messages.set_column('I:I', 30)
    worksheet_messages.set_column('J:J', 50)
    worksheet_messages.set_column('K:K', 34)
    bold = workbook.add_format({'bold': True, 'bg_color': '#c0c0c0', 'align': 'center',
                                'font_name': 'Arial', 'font_size': '10'})
    regular = workbook.add_format({'bold': False, 'font_name': 'Arial', 'font_size': '10', 'text_wrap': 1,
                                   'valign': 'top'})
    worksheet_messages.write('A1', 'ID сообщения', bold)
    worksheet_messages.write('B1', 'ID абнента', bold)
    worksheet_messages.write('C1', 'Имя абонента', bold)
    worksheet_messages.write('D1', 'Имя абонента (Signal)', bold)
    worksheet_messages.write('E1', 'Номер абонента', bold)
    worksheet_messages.write('F1', 'Время', bold)
    worksheet_messages.write('G1', 'Время отправки', bold)
    worksheet_messages.write('H1', 'Статус', bold)
    worksheet_messages.write('I1', 'Тип сообщения', bold)
    worksheet_messages.write('J1', 'Текст', bold)
    worksheet_messages.write('K1', 'GUID', bold)
    worksheet_messages.autofilter('A1:K1')
    worksheet_messages.freeze_panes(1, 0)

    try:
        conn = sqlite3.connect(base)
        c = conn.cursor()
        c.execute("SELECT sms._id, sms.address, sms.date, sms.date_sent, sms.read, sms.type, sms.body, "
                  "sms.server_guid, recipient.phone, recipient.system_display_name, recipient.signal_profile_name "
                  "FROM sms INNER JOIN recipient ON recipient._id = sms.address")
        rows = c.fetchall()
        row_xlsx = 1
        for row in rows:
            col = 0
            for item in (get_data(row)):
                worksheet_messages.write(row_xlsx, col, item, regular)
                col += 1
            row_xlsx += 1
        # conn.commit()
        conn.close()
        msg = "Анализ резервной копии произведен успешно! Отчет сохранен в каталог 'out'"
        mb.showinfo("Готово!", msg)
    except Exception as e:
        msg = "Возникла ошибка по причине: " + str(e) + "\nУбедитесь в корректности введенных данных"
        mb.showerror("Ошибка", msg)

    workbook.close()


def main():
    def get_file_path():
        ftypes = [('Backup файлы', '*.backup'), ('Все файлы', '*')]
        dlg = filedialog.Open(filetypes=ftypes)
        fl = dlg.show()
        entry_filename.delete(0, END)
        entry_filename.insert(0, fl.replace("/", "\\"))

    def get_base():
        backup = entry_filename.get()
        print(backup)
        pass_code = entry_pass.get()
        print(pass_code)
        path_tmp = "tmp\\"
        for f in os.listdir(path_tmp):
            os.remove(os.path.join(path_tmp, f))
        try:
            cmd = 'signalbackup-tools_win.exe ' + backup + ' ' + pass_code + ' --output ' + path_tmp
            PIPE = subprocess.PIPE
            proc = subprocess.Popen(cmd, shell=True)
            proc.wait()
        except Exception as e:
            msg = "Ошибка вызвана по причине: " + str(e) + "\nУбедитесь в корректности введенных данных"
            mb.showerror("Ошибка", msg)
        return "tmp\\database.sqlite"

    try:
        path_out = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'out/Signal.xlsx')
        os.remove(path_out)
    except:
        pass
    root = Tk()
    root.title('SignalBackupParser 0.9b')
    root.geometry('540x480')
    icon = my_icon.set_icon()
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(data=icon))
    bg = PhotoImage(file="logo.png")
    root.resizable(False, False)
    logo_label = Label(root, image=bg)
    logo_label.grid(row=0, column=0, columnspan=3)

    file_label = ttk.Label(root, font='arial 9', foreground='#999999',
                           text="Укажите путь к файлу резервной копии Signal "
                                "или нажмите 'Открыть'")
    file_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    entry_filename = ttk.Entry(root, width=55, font='arial 9')
    entry_filename.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    button_open = Button(root, text=u'Открыть', width=15, height=1, bg='#138eec', fg='white',
                         font='arial 9 bold', command=get_file_path)
    button_open.grid(row=2, column=2, padx=5, pady=5)

    pass_label = ttk.Label(root, font='arial 9', foreground='#999999',
                           text="Укажите парольною фразу (30 символов) к резервной копии Signal")
    pass_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    entry_pass = ttk.Entry(root, width=75, font='arial 9')
    entry_pass.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    btn_2 = Button(root, text='Анализ', width=15, height=1, bg='#138eec', fg='white', font='arial 14',
                   command=lambda: make_result(get_base()))
    btn_2.grid(row=5, column=0, columnspan=3, padx=10, pady=(40, 0))
    m_lbl = ttk.Label(root, text='© VKukh', font='arial 7', foreground='#999999', justify=LEFT)
    m_lbl.grid(row=6, column=0, columnspan=3)

    root.mainloop()


if __name__ == '__main__':
    main()
