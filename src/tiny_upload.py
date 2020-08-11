import sys
import re
import os
from os.path import isfile, join
import tinify


EXTS = ['png', 'jpg', 'jpeg']


def get_new_and_bak_file(file):
    splitted = file.split('.')
    base_dir, ext = '.'.join(splitted[:-1]), splitted[-1]
    new_file = f'{base_dir}.new.{ext}'
    old_file = f'{base_dir}.bak.{ext}'
    return new_file, old_file, ext


def compress(file, new_file, old_file):
    source = tinify.from_file(file)
    source.to_file(new_file)
    os.rename(file, old_file)
    os.rename(new_file, file)


def scale(file, new_file, old_file, axis, length):
    source = tinify.from_file(file)
    resized = (source.resize(method='scale', width=length)
               if axis == 'w'
               else source.resize(method='scale', height=length))
    resized.to_file(new_file)
    os.rename(file, old_file)
    os.rename(new_file, file)


def resize_general(file, new_file, old_file, width, height, method):
    source = tinify.from_file(file).resize(
        method=method.lower(),
        width=width,
        height=height
    )
    source.to_file(new_file)
    os.rename(file, old_file)
    os.rename(new_file, file)


def get_file_lst(files_or_folder):
    is_files = bool(re.search(r':', files_or_folder))
    if is_files:
        # Remove " at each end and last :
        files_or_folder = files_or_folder[1:-2]
        return files_or_folder.split(':')
    else:  # is folder
        return [f for f in os.listdir(files_or_folder)
                if isfile(join(files_or_folder, f))]


def send_notification_msg(command, file_lst, succeses):
    text_prefix = {
        'COMPRESS': 'Compress',
        'SCALE': 'Scal',
        'FIT': 'Fitt',
        'COVER': 'Cover',
        'THUMB': 'Thumb'
    }
    cmd_text = text_prefix[command] if command in text_prefix else '...'
    num_files = len(file_lst)
    if succeses == 0 and num_files == 1:
        print(f'Error {cmd_text.lower()}ing file')
    elif succeses == 1 and num_files == 1:
        print(f'{cmd_text}ed {file_lst[0]}')
    else:
        print(f'{cmd_text}ed {succeses}/{num_files} files')


def main():
    files_or_folder = sys.argv[1]
    command = sys.argv[2]
    tinify.key = sys.argv[3]
    width = int(sys.argv[4])
    height = int(sys.argv[5])
    axis = sys.argv[6]
    length = int(sys.argv[7])

    if command == 'COMPRESS':
        def compress_resize_func(file):
            return compress(file)
    elif command == 'SCALE':
        def compress_resize_func(file):
            return scale(file, axis, length)
    else:
        def compress_resize_func(file):
            return resize_general(file, width, height, command)

    succeses = 0
    file_lst = get_file_lst(files_or_folder)
    for file in file_lst:
        try:
            new_file, old_file, ext = get_new_and_bak_file(file)
            if ext not in EXTS:
                continue
            elif command == 'COMPRESS':
                compress(file, new_file, old_file)
            elif command == 'SCALE':
                scale(file, new_file, old_file, axis, length)
            else:
                resize_general(file, new_file, old_file, width, height, command)
            succeses += 1
        except Exception:
            continue
    send_notification_msg(command, file_lst, succeses)


if __name__ == '__main__':
    main()
