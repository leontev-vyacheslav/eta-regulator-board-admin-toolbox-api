from multiprocessing import cpu_count, freeze_support
import sys
import uvicorn
import psutil
from pystray import Icon, Menu, MenuItem
from PIL import Image

import src.main

class ConsoleProxy:
    def __init__(self):
        sys.stdout = open(f'{src.main.app.title}.log', 'a', encoding='utf-8')
        sys.stderr = sys.stdout

    def write(self, message):
        sys.stdout.write(message)
        sys.stdout.flush()

    def isatty(self):
        return False

def on_exit_menu_item_click_handler():

    for p in psutil.process_iter():
        try:
            if  'eta_regulator_board_admin_toolbox'.lower() in p.name().lower():
                p.kill()
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


icon = Icon(
    src.main.app.description,
    icon=Image.open('_internal/src/assets/icon.png'),
    menu=Menu(
    MenuItem(
        'Exit ETA Regulator Board Admin API server',
        on_exit_menu_item_click_handler,
    )
    )
)

def start_server(host="0.0.0.0", port=5012, num_workers=1, reload=False):
    uvicorn.run("src.main:app",
                host=host,
                port=port,
                reload=reload
            )

if __name__ == "__main__":
    icon.run_detached()
    console_proxy = ConsoleProxy()
    num_workers = int(cpu_count() / 2)
    print(f'{src.main.app.description}: (it will be used workers in amount of {num_workers})')

    freeze_support()

    start_server(num_workers=num_workers)
