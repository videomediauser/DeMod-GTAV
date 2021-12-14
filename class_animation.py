import sys
from time import sleep


def animated_loading():
    chars = "/—\\|"
    for char in chars:
        sys.stdout.write('\r'+'Checking for Updates...'+char)
        sleep(.1)
        sys.stdout.flush()


def animated_download():
    animation = [
        "[        ]",
        "[=       ]",
        "[===     ]",
        "[====    ]",
        "[=====   ]",
        "[======  ]",
        "[======= ]",
        "[========]",
        "[ =======]",
        "[  ======]",
        "[   =====]",
        "[    ====]",
        "[     ===]",
        "[      ==]",
        "[       =]",
        "[        ]",
        "[        ]"
    ]
    i = 0
    while True:
        print(animation[i % len(animation)], end='\rInstall')
        sleep(.1)
        i += 1
        if i == 17:
            break
