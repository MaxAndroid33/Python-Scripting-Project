import os
import json
import sys
import shutil
from subprocess import PIPE, run


GAME_DIR_PATTERN = "game"


def create_dir(path):
    if not os.path.exists(path):
        if os.name == 'nt':
            os.mkdir(path)
        elif os.name == 'posix':
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


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        (_, dir_name) = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def make_json_meradata_file(path, gaem_dirs):
    data = {
        "gameNames": gaem_dirs,
        "numberofGames": len(gaem_dirs)

    }

    with open(path, "w") as f:
        json.dump(data, f)


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")

    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
    
    json_path =os.path.join(target_path,"metadate.json")
    make_json_meradata_file(json_path,new_game_dirs)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only")

    source, target = args[1:]
    main(source, target)
