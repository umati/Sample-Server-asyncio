import os, datetime

with open("log/buildlog.txt", "a+") as f:
    f.write(f"Build: {datetime.datetime.now()} from {os.getlogin()}\n")
    try:
        p = os.system("python src/generate_export_namespace.py")
        if str(p) == "1":
            f.write("Namespace build failed!\n")
        else:
            f.write("Namespace build passed!\n")
            p = os.system("pyinstaller --onefile src/server.py")
            if str(p) == "1":
                f.write("Executable build failed!\n")
            else:
                f.write("Executable build passed!\n")
    except Exception as e:
        f.write(f"{e}\n")
    f.write("-------------")