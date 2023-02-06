import os
import json
import sys
import shutil
from subprocess import PIPE, run


GAME_DIR_PATTERN = "game"


def create_dir(path):
    if not os.path.exists(path):
        if os.name is 'nt':
            os.mkdir(path)
        elif os.name is 'posix':
            os.makedirs(path)


def find_all_game_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break
    return game_paths


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    source_target = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    print(game_paths)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only")

    source, target = args[1:]
    main(source, target)
