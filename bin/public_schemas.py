#!/bin/python

class SchemasJS:
        def __init__(self, schemas):
		self.schemas = schemas
	def __format__(self,format):
		return "/* eslint global-require: 0 */\n\nimport { fromJS } from 'immutable';\n\nexport default fromJS([\n" +\
                 ",\n".join( "   require('{}')".format(schema) for schema in self.schemas ) +\
                 "\n]);\n"

from urllib import urlopen
import json 
import os
import sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
url = 'http://example.com/api/schemas/public'
home = os.path.dirname(bindir)
f = urlopen(url)
j = json.loads(f.read())

# schema/co.ga/email_submission/jsonschema/1-0-0

updated = []
relative = []
for schema in j: 
	if schema['self']['name'] == 'schema' and schema['self']['vendor'] == 'com.snowplowanalytics.self-desc': 
		continue
	filename = os.path.join(home, 'schema', schema['self']['vendor'] ,  schema['self']['name'], 'jsonschema' , schema['self']['version'])
        relative.append( '/'.join(['.','schema', schema['self']['vendor'] ,  schema['self']['name'], 'jsonschema' , schema['self']['version'] ]) )
        if not os.path.exists(os.path.dirname(filename)):
        	os.makedirs(os.path.dirname(filename))
	with open(filename, 'w') as f: 
		json.dump(schema, f)
	updated.append(filename)


# if schemas ever disappear 
jsons = [f for f in os.listdir(os.path.join(home, 'schema')) if f.endswith('.json')]
# this is the set of schemas that no longer exist on schema registry. 
deleted = set(jsons).difference(updated)
for d in deleted: 
	os.remove(d)
file = open(os.path.join(home,'schemas.js'),'w')
js =  '{}'.format(SchemasJS(relative))
file.write(js)
