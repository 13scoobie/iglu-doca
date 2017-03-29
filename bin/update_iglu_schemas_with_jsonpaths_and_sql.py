#!/bin/python

from collections import defaultdict
import json 
import os

try: 
	import requests
except ImportError: 
	exit("you need to install requests: 'pip install requests'")


url = 'http://example.com/api/schemas/%(vendor)s/%(name)s/%(schemaFormat)s/%(version)s?isPublic=true'
repo = '/tmp/iglu-repository'

# schemas/<vendor>/<name>/jsonschema/<version>
# jsonpaths/<vendor>/<name>_<version>.json
# sql/<vendor>/<name>_<version>.sql

for root, dirs, files in os.walk(repo + '/schemas'):
	for name in files: 
		with open('%s/%s' %(root, name), 'r') as f: 
			schema = json.load(f)
		vendor = schema['self']['vendor']
		name = schema['self']['name']
		version = schema['self']['version']
		print(vendor, name, version)

		major, minor, patch = version.split('-')

		with open('%s/jsonpaths/%s/%s_%s.json' % (repo, vendor, name, major), 'r') as f: 
			jsonpaths = json.load(f)

		schema['jsonpaths'] = jsonpaths['jsonpaths']

		with open('%s/sql/%s/%s_%s.sql' % (repo, vendor, name, major)) as f: 
			sql = f.read()

		schema['sql'] = sql 

		data = json.dumps(schema)
		headers = {'apikey': 'superuser-api-key'}
		thisurl = url % dict(vendor=vendor, name=name, schemaFormat='jsonschema', version=version)
		print(thisurl)
		try: 
			response = requests.post(thisurl, data=data, headers=headers)
		except: 
			# if this schema exists already it will respond with 'unauthorized' 
			response = requests.put(thisurl, data=data, headers=headers)
		print(response.text)
