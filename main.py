import subprocess


def get_base(backup, pass_code):
    cmd = 'signalbackup-tools_win.exe signal-2021-11-19-12-38-24.backup 486746075681940264135041361970 --output tmp\\'
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    print("process finished")


def get_data(base):
    pass


def get_result(data):
    pass


def main():
    file_path = "signal-2021-11-19-12-38-24.backup"
    pass_code = "486746075681940264135041361970x"
    get_base(file_path, pass_code)


if __name__ == '__main__':
    main()
