TIMESTAMP_PATTERN = '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
ENTRY_NUMBER_PATTERN = '^\d+$'
KEY_PATTERN = '.+'
ITEM_HASH_PATTERN = '^sha-256:[a-f\d]{64}$'

ENTRY_NUMBER = {
    'entry-number': {
        'type': 'string',
        'pattern': ENTRY_NUMBER_PATTERN
    }
}

ITEM_HASH = {
    'item-hash': {
        'type': 'string',
        'pattern': ITEM_HASH_PATTERN
    }
}

ENTRY_TIMESTAMP = {
    'entry-timestamp': {
        'type': 'string',
        'pattern': TIMESTAMP_PATTERN
    }
}

ENTRY_KEY = {
    'key': {
        'type': 'string',
        'pattern': '.+'
    }
}
