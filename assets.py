import pyfiglet
"""
Assets for the solar system program
"""
mercury = """ __  __‽
|  \/  | ___ _ __ ___ _   _ _ __ _   _‽
| |\/| |/ _ \ '__/ __| | | | '__| | | |‽
| |  | |  __/ | | (__| |_| | |  | |_| |‽
|_|  |_|\___|_|  \___|\__,_|_|   \__, |‽
                                 |___/‽
""".replace("\n","")

if __name__ == "__main__":
    f = pyfiglet.figlet_format("Mercury", font="mono9")
    print(f)