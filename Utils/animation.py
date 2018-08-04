from threading import Thread  # threading module for cursor animation
from time import sleep  # necessary for cursor animation
from colorama import init, Fore  # colors to Windows Command Prompt

init(autoreset=True)  # inicialize Windows Command Prompt


# Cursor animation taken from:
# stackoverflow.com/questions/7039114/waiting-animation-in-command-prompt-python
class CursorAnimation(Thread):
    """Cursor animation taken from stackoverflow"""
    def __init__(self):
        self.flag = True
        self.animation_char = "|/-\\"
        self.idx = 0
        Thread.__init__(self)

    def run(self):
        """Start cursor animation"""
        while self.flag:
            print(Fore.RED + 'Processing request...', end='')
            print(self.animation_char[self.idx % len(self.animation_char)] +
                  "\r", end='')
            self.idx += 1
            sleep(0.1)

    def stop(self):
        """Stop cursor animation"""
        self.flag = False
        print(Fore.GREEN + 'Processing request... Done!')
