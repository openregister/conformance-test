TIMESTAMP_PATTERN = '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
ENTRY_NUMBER_PATTERN = '^\d+$'
KEY_PATTERN = '.+'
HASH_PATTERN = '^sha-256:[a-f\d]{64}$'
MULTIHASH_PATTERN = '^[a-f\d]+$'
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
        'pattern': MULTIHASH_PATTERN
    }
}

BLOB_ID = {
    '_id': {
        'type': 'string',
        'pattern': MULTIHASH_PATTERN
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

HASHING_ALGORITHM = {
    'type': 'object',
    'properties': {
        'digest-length': {'type': 'integer'},
        'function-type': {'type': 'integer'},
        'codec': {'type': 'string'}
    },
    'required': ['digest-length', 'function-type', 'codec']
}

STATISTICS = {
    'type': 'object',
    'properties': {
        'total-records': {'type': 'integer'},
        'total-entries': {'type': 'integer'},
        'total-blobs': {'type': 'integer'}
    },
    'required': ['total-records', 'total-entries', 'total-blobs']
}

STATUS = {
    'type': 'object',
    'properties': {
        'start-date': {'type': 'string', 'format': 'date-time'},
        'end-date': {'type': 'string', 'format': 'date-time'},
        'replacement': {'type': 'string', 'format': 'uri'},
        'reason': {'type': 'string'}
    },
    'required': ['start-date']
}

SCHEMA = {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "pattern": KEY_PATTERN,
      },
      "datatype": {
        "type": "string",
        "enum": [
          "curie",
          "datetime",
          "name",
          "hash",
          "integer",
          "period",
          "string",
          "text",
          "url"
        ]
      },
      "cardinality": {
        "type": "string"
      },
      "title": {
        "type": "string"
      },
      "description": {
        "type": "string"
      }
    },
    "required": [
      "id",
      "datatype",
      "cardinality"
    ]
  }
}