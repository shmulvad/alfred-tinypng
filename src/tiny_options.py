import os
import sys
import json
import re

NUMBER_PATTERN = r'^\d+$'
variables_to_send = {}


def send_items_to_alfred(items):
    print(json.dumps({'items': items, 'variables': variables_to_send}))


def api_key_not_set_item():
    send_items_to_alfred([{
        'title': 'No API key set. Click here to set API key',
        'subtitle': 'Action item to get a new API key and set it',
        'arg': 'API_KEY',
    }])


def compress(args):
    return {
        'title': 'COMPRESS: Compress image(s)',
        'subtitle': 'Compresses image(s)',
        'arg': 'COMPRESS',
        'uid': 'COMPRESS'
    }


def scale(args):
    options = {
        'title': 'SCALE: Scale prop. down by *either* height or width',
        'subtitle': 'Usage: I.e. "w800" or "h500"',
        'valid': False,
        'arg': 'SCALE',
        'uid': 'SCALE',
        'icon': {
            'path': 'scale.png'
        }
    }
    arg = args[0].strip()
    match = re.match(r'^(w|h)(\d+)$', arg)
    if not arg or (len(arg) == 1 and arg[0] in ['w', 'h']):
        return options
    elif len(args) == 1 and match:
        axis, length = match.groups()
        axis_txt = 'width' if axis == 'w' else 'height'
        options['title'] = f'SCALE: Scale prop. down to a {axis_txt} of {length}'
        options['subtitle'] = f'Scale prop. down to a {axis_txt} of {length}'
        options['valid'] = True
        variables_to_send['axis'] = axis
        variables_to_send['len'] = length
        return options


def width_height_resize(type, description, args):
    options = {
        'title': f'{type}: {description} width and height',
        'subtitle': 'Usage: "width height", i.e. "800 500"',
        'valid': False,
        'arg': type,
        'uid': type,
        'icon': {
            'path': f'{type.lower()}.png'
        }
    }

    width = args[0].strip()
    if not width:
        return options

    match_fst = re.match(NUMBER_PATTERN, width)
    if len(args) == 1 and match_fst:
        options['title'] = f'{type}: {description} {width}×...'
        options['subtitle'] = f'{description} {width}×...'
        options['autocomplete'] = f'{width} '
        return options
    elif len(args) == 2:
        height = args[1].strip()
        if match_fst and re.match(NUMBER_PATTERN, height):
            options['title'] = f'{type}: {description} {width}×{height}'
            options['subtitle'] = f'{description} {width}×{height}'
            options['valid'] = True
            variables_to_send['width'] = width
            variables_to_send['height'] = height
            return options
    return None


def fit(args):
    return width_height_resize('FIT', 'Scale prop. down within', args)


def cover(args):
    return width_height_resize('COVER', 'Scale and crop down to exactly', args)


def thumb(args):
    return width_height_resize('THUMB', 'Advanced scale and crop to exactly', args)


def compress_resize_items(query):
    funcs = [scale, fit, cover, thumb]
    if query is None:
        args = [""]
        funcs = [compress] + funcs
    else:
        args = query.strip().split(' ')
    items_raw = [func(args) for func in funcs]
    items = [item for item in items_raw if item]
    send_items_to_alfred(items)


def main():
    for var in ['axis', 'len', 'width', 'height']:
        variables_to_send[var] = 0

    if not os.environ['API_KEY']:
        api_key_not_set_item()
    elif len(sys.argv) < 2:
        compress_resize_items(None)
    else:
        compress_resize_items(sys.argv[1])


if __name__ == '__main__':
    main()
