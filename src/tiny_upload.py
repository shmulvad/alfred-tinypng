import sys
import re
import os
from typing import Tuple, List
from os.path import isfile, join
import tinify
from tinify import Source

EXTS = ['png', 'jpg', 'jpeg']
KEEP_BACKUPS = sys.argv[2].lower() == 'true'


def get_new_and_bak_file(file: str) -> Tuple[str, str]:
    splitted = file.split('.')
    base_dir, ext = '.'.join(splitted[:-1]), splitted[-1]
    new_file = f'{base_dir}.new.{ext}'
    old_file = f'{base_dir}.bak.{ext}'
    return new_file, old_file


def write_img_to_disk(img: Source, file: str) -> None:
    if not KEEP_BACKUPS:
        img.to_file(file)
        return

    new_file, old_file = get_new_and_bak_file(file)
    img.to_file(new_file)
    os.rename(file, old_file)
    os.rename(new_file, file)


def compress(file: str) -> None:
    source = tinify.from_file(file)
    write_img_to_disk(source, file)


def scale(file: str, axis: str, length: int) -> None:
    source = tinify.from_file(file)
    resized = (source.resize(method='scale', width=length)
               if axis == 'w'
               else source.resize(method='scale', height=length))
    write_img_to_disk(resized, file)


def resize_general(file: str, width: int, height: int, method: str) -> None:
    resized_img = tinify.from_file(file).resize(
        method=method.lower(),
        width=width,
        height=height
    )
    write_img_to_disk(resized_img, file)


def get_file_lst(files_or_folder: str) -> List[str]:
    is_files = bool(re.search(r':', files_or_folder))
    if is_files:
        # Remove last : and then split
        return files_or_folder[:-1].split(':')
    else:  # is folder
        return [f for f in os.listdir(files_or_folder)
                if isfile(join(files_or_folder, f))]


def send_notification_msg(command: str, files: List[str], succeses: int) -> None:
    text_prefix = {
        'COMPRESS': 'Compress',
        'SCALE': 'Scal',
        'FIT': 'Fitt',
        'COVER': 'Cover',
        'THUMB': 'Thumb'
    }
    cmd_text = text_prefix[command] if command in text_prefix else '...'
    num_files = len(files)
    if succeses == 0 and num_files == 1:
        print(f'Error {cmd_text.lower()}ing file')
    elif succeses == 1 and num_files == 1:
        print(f'{cmd_text}ed {files[0]}')
    else:
        print(f'{cmd_text}ed {succeses}/{num_files} files')


def main():
    tinify.key = sys.argv[1]
    files_or_folder = sys.argv[3]
    command = sys.argv[4]
    width = int(sys.argv[5])
    height = int(sys.argv[6])
    axis = sys.argv[7]
    length = int(sys.argv[8])

    succeses = 0
    files = get_file_lst(files_or_folder)
    for file in files:
        try:
            ext = file.split('.')[-1]
            if ext not in EXTS:
                error_msg = f'Error with {file}: Extension {ext} not supported\n'
                sys.stderr.write(error_msg)
                continue
            elif command == 'COMPRESS':
                compress(file)
            elif command == 'SCALE':
                scale(file, axis, length)
            else:
                resize_general(file, width, height, command)
            succeses += 1
        except Exception as e:
            sys.stderr.write(f'Error with {file}: {e}\n')

    send_notification_msg(command, files, succeses)


if __name__ == '__main__':
    main()
