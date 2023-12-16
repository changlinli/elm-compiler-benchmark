import os
import shutil
from collections import deque
from typing import Deque

NUM_OF_DUPLICATES = 300

SRC_DIRECTORY = "src"

GENERATED_DESTINATION = "generated"

original_files: Deque[os.DirEntry] = deque()

module_names = set()

for dir_entry in os.scandir(SRC_DIRECTORY):
    original_files.append(dir_entry)

for dir_entry in original_files:
    filename = dir_entry.name
    print(filename)
    for i in range(NUM_OF_DUPLICATES):
        new_filename = f"{GENERATED_DESTINATION}/{filename.replace('REPLACETHIS', str(i))}"
        print(f"{new_filename=}")
        if os.path.isdir(dir_entry):
            shutil.copytree(f"{SRC_DIRECTORY}/{filename}", new_filename)
            for root, dirs, files in os.walk(new_filename):
                for file in files:
                    with open(os.path.join(root, file), "r+") as f:
                        file_contents = f.read()
                        file_contents_by_line = file_contents.splitlines()
                        new_lines = \
                            [ line.replace("REPLACETHIS", str(i)) 
                             for line in file_contents.splitlines() ]
                        f.seek(0)
                        f.write('\n'.join(new_lines))
                        f.truncate()
        elif os.path.isfile(dir_entry):
            os.makedirs(os.path.dirname(new_filename), exist_ok=True)
            shutil.copy(f"{SRC_DIRECTORY}/{filename}", new_filename)
            with open(new_filename, "r+") as f:
                file_contents = f.read()
                file_contents_by_line = file_contents.splitlines()
                new_lines = \
                    [ line.replace("REPLACETHIS", str(i)) 
                     for line in file_contents.splitlines() ]
                f.seek(0)
                f.write('\n'.join(new_lines))
                f.truncate()

new_main_file = "module Main "
new_main_imports = [ f"import Main_{i}" for i in range(NUM_OF_DUPLICATES) ]
