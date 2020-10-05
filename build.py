import os, datetime

with open("buildlog.txt", "a+") as f:
    f.write(f"Build: {datetime.datetime.now()} from {os.getlogin()}\n")
    try:
       os.system("python src/generate_export_namespace.py")
       f.write("Namespace build passed!\n")
    except Exception as e:
        f.write(f"{e}\n")
    try:
       os.system("pyinstaller --onefile src/server.py")
       f.write("Executable build passed!\n")
    except Exception as e:
        f.write(f"{e}\n")
    f.write("-------------")