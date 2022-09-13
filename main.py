import os
import sqlite3
import subprocess


def get_base(backup, pass_code):
    path_tmp = "tmp\\"
    for f in os.listdir(path_tmp):
        os.remove(os.path.join(path_tmp, f))
    cmd = 'signalbackup-tools_win.exe ' + backup + ' ' + pass_code + ' --output ' + path_tmp
    print(cmd)
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True)
    p.wait()

    print("process finished")
    return "tmp\\database.sqlite"


def get_data(base):
    conn = sqlite3.connect(base)
    c = conn.cursor()
    c.execute("SELECT * FROM sms")

    rows = c.fetchall()
    for row in rows:
        print(row)
    # conn.commit()
    conn.close()


def get_result(data):
    pass


def main():
    file_path = "signal-2021-11-19-12-38-24.backup"
    pass_code = "486746075681940264135041361970"
    get_data(get_base(file_path, pass_code))


if __name__ == '__main__':
    main()
