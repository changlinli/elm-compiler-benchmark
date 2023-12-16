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


def filename_to_module_name(filename: str) -> str:
    return filename.split(".")[0]

def file_path_to_module_name(file_path: str) -> str:
    print(f"{file_path=}")
    path_components = [ component for component in file_path.split("/") if len(component) > 0 ]
    path_components_normalized = [ component.split("_")[0] for component in path_components ]
    return ".".join(path_components_normalized)

def add_idx_to_module_name(module_name: str, idx: int) -> str:
    split_by_periods = module_name.split(".")
    if len(split_by_periods) > 1:
        return ".".join([f"{split_by_periods[0]}_{idx}"] + split_by_periods[1:])
    else:
        return f"{module_name}_{idx}"

def modify_import_line(import_line: str, module_names: set[str], idx: int) -> str:
    if import_line.startswith("import"):
        import_and_rest = import_line.split(" ")
        import_and_rest[1] = \
            add_idx_to_module_name(import_and_rest[1], idx) if import_and_rest[1] in module_names else import_and_rest[1]
        return " ".join(import_and_rest)
    else:
        return import_line

def strip_elm_suffix_of_filename(filename: str) -> str:
    return filename.split(".")[0]

def add_idx_to_elm_filename(filename: str, idx: int) -> str:
    file_components = filename.split(".")
    if len(file_components) > 1:
        return "".join([file_components[0], "_", str(idx), "."] + file_components[1:])
    else:
        return f"{filename}_{idx}"

def modify_module_line(module_line: str, module_names: set[str], idx: int) -> str:
    if module_line.startswith("module"):
        module_name_and_rest = module_line.split(" ")
        module_name_and_rest[1] = add_idx_to_module_name(module_name_and_rest[1], idx) if module_name_and_rest[1] in module_names else module_name_and_rest[1]
        return " ".join(module_name_and_rest)
    else:
        return module_line

def should_modify_line(line: str, module_names: set[str]) -> bool:
    words = line.split(" ")
    for word in words:
        if word in module_names:
            return True
    return False

def modify_line(file_line: str, module_names: set[str], idx: int) -> str:
    if file_line.startswith("module"):
        return modify_module_line(file_line, module_names, idx)
    elif file_line.startswith("import"):
        return modify_import_line(file_line, module_names, idx)
    else:
        words = [ word for word in file_line.split(" ") ]
        modified_words = []
        for word in words:
            fragments = [ fragment for fragment in word.split(".") ]
            modified_fragments = [ f"{fragment}_{idx}" if fragment in module_names else fragment for fragment in fragments ]
            modified_words.append(".".join(modified_fragments))
        return " ".join(modified_words)

for root, subdirs, files in os.walk(SRC_DIRECTORY):
    for file in files:
        # root otherwise will have SRC_DIRECTORY in it
        original_module_name = file_path_to_module_name(os.path.join(root[len(SRC_DIRECTORY):], strip_elm_suffix_of_filename(file)))
        module_names.add(original_module_name)

print(f"{module_names=}")
example_line = "            Asset.src Asset.defaultAvatar "
print(f"{modify_line(example_line, module_names, 1)}")

for dir_entry in original_files:
    filename = dir_entry.name
    print(filename)
    for i in range(NUM_OF_DUPLICATES):
        new_filename = f"{GENERATED_DESTINATION}/{add_idx_to_elm_filename(filename, i)}"
        if os.path.isdir(dir_entry):
            shutil.copytree(f"{SRC_DIRECTORY}/{filename}", new_filename)
            parent_module_name = filename_to_module_name(filename)
            for root, subdirs, files in os.walk(filename):
                for sub_filename in files:
                    full_filename = os.path.join(root, sub_filename)
                    with open(full_filename, "r+") as f:
                        file_contents = f.read()
                        file_contents_by_line = file_contents.splitlines()
                        new_lines = \
                            [ modify_line(line, module_names, i)
                             for line in file_contents.splitlines() ]
                        f.seek(0)
                        f.write('\n'.join(new_lines))
                        f.truncate()
        elif os.path.isfile(dir_entry):
            shutil.copy(f"{SRC_DIRECTORY}/{filename}", new_filename)
            with open(new_filename, "r+") as f:
                file_contents = f.read()
                file_contents_by_line = file_contents.splitlines()
                new_lines = \
                    [ modify_line(line, module_names, i)
                     for line in file_contents.splitlines() ]
                f.seek(0)
                f.write('\n'.join(new_lines))
                f.truncate()

new_main_file = "module Main "
new_main_imports = [ f"import Main_{i}" for i in range(NUM_OF_DUPLICATES) ]
