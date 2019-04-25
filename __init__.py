# import python modules
import os


APP_DIR = os.path.dirname(__file__, )
# REL_PATH_PICKLE = '../_pickled/'
# ABS_FILE_PICKLE = os.path.abspath(os.path.join(APP_DIR, REL_PATH_PICKLE))


def main():
    print(APP_DIR)
    # print(ABS_FILE_PICKLE)


if __name__ == '__main__':
    main()
