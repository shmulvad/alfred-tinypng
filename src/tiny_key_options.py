import sys
import json


def send_items_to_alfred(items):
    print(json.dumps({'items': items}))


def api_key_provided_item(api_key):
    send_items_to_alfred([{
        'title': f'Set API key to "{api_key}"',
        'subtitle': f'Set API key to "{api_key}"',
        'arg': api_key,
        'valid': True
    }])


def no_api_key_provided_items():
    send_items_to_alfred([
        {
            'title': 'Set API key to ...',
            'subtitle': 'Set API key to ...',
            'valid': False
        },
        {
            'title': 'Get a new API key',
            'subtitle': 'Open https://tinypng.com/developers to get a new API key',
            'arg': 'WEBSITE',
            'valid': True
        }
    ])


def main():
    if len(sys.argv) > 1:
        api_key_provided_item(sys.argv[1])
    else:
        no_api_key_provided_items()


if __name__ == "__main__":
    main()
