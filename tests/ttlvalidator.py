import re

from rdflib.graph import Graph
from rdflib.namespace import Namespace


class TtlValidator:
    def __init__(self):
        self.graph = Graph()
        self.fields = []
        self.entryRegexMap = {}
        self.specification_namespace = Namespace('https://openregister.github.io/specification/#')

    def add_data(self, data):
        self.graph.parse(data=data, format='turtle')

    def add_fields(self, namespace, fields):
        ns = Namespace(namespace)
        self.fields.extend(ns[f] for f in fields)

    def add_entry_regex(self, field, pattern):
        self.entryRegexMap[field] = re.compile(pattern)

    def add_entry_fields_to_validation(self):
        self.fields.extend(self.specification_namespace[f] for f in self.entryRegexMap.keys())

    def validate_fields_exist(self):
        return [p for p in self.graph.predicates() if p not in self.fields]

    def validate_data_matches_field_data_types(self):
        problems = []

        for p, r in self.entryRegexMap.items():
            objects = list(self.graph.objects(subject=None, predicate=self.specification_namespace[p]))
            problems.extend(v for _, v in enumerate(objects) if r.search(v) is None)

        return problems
