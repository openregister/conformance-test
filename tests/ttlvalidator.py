import rdflib
import re

from rdflib.graph import Graph
from rdflib.namespace import Namespace

class TtlValidator:
	def __init__(self):
		self.fields = []
		self.entryRegexMap = {}

	def add_data(self, data):
		self.graph = Graph()
		self.graph.parse(data=data, format="turtle")

	def add_fields(self, namespace, fields):
		ns = Namespace(namespace)
		self.fields.extend(ns[f] for f in fields)

	def add_entry_regex(self, field, pattern):
		self.entryRegexMap[field] = re.compile(pattern)

	def addEntryFieldsToValidation(self, namespace):
		ns = Namespace(namespace)
		self.fields.extend(ns[f] for f in self.entryRegexMap.keys())

	def validateFieldsExist(self):
		problems = []
		problems.extend(p for p in self.graph.predicates() if p not in self.fields)
		
		return problems

	def validateDataMatchesFieldDataTypes(self, namespace):
		problems = []

		ns = Namespace(namespace)

		for p, r in self.entryRegexMap.items():
			objects = list(self.graph.objects(subject=None, predicate=ns[p]))
			problems.extend(v for k, v in enumerate(objects) if r.search(v) is None)

		return problems