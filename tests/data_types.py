TIMESTAMP_PATTERN = '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
ENTRY_NUMBER_PATTERN = '^\d+$'
KEY_PATTERN = '.+'
HASH_PATTERN = '^sha-256:[a-f\d]{64}$'
ITEM_RESOURCE_PATTERN = '/items/sha-256:[a-f\d]{64}$'
NAME_PATTERN = '^[A-Za-z]{1}[A-Za-z0-9][A-Za-z0-9-_/]*$'

INDEX_ENTRY_NUMBER = {
    'index-entry-number': {
        'type': 'string',
        'pattern': ENTRY_NUMBER_PATTERN
    }
}

ENTRY_NUMBER = {
    'entry-number': {
        'type': 'string',
        'pattern': ENTRY_NUMBER_PATTERN
    }
}

ENTRY_NUMBER_V2 = {
    'entry-number': {
        'type': 'integer'
    }
}

ITEM_HASH = {
    'item-hash': {
        'type': 'string',
        'pattern': HASH_PATTERN
    }
}

ITEM_HASH_ARRAY = {
    'item-hash': {
        'type': 'array',
        'items': {
            'type': 'string',
            'pattern': HASH_PATTERN
        }
    }
}

BLOB_HASH = {
    'blob-hash': {
        'type': 'string',
        'pattern': HASH_PATTERN
    }
}

ITEM = {
    'item': {
        'type': 'array',
        'items': {
            'type': 'object'
        }
    }
}

BLOB = {
    'blob': {
        'type': 'object'
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
        'pattern': KEY_PATTERN
    }
}

RECORD_ID = {
    '_id': {
        'type': 'string',
        'pattern': KEY_PATTERN
    }
}
