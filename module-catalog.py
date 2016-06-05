#!/usr/bin/env python
"""YANG module catalog data generator

from __future__ import print_function

import optparse
import sys
import re
import string
import logging

import types
import StringIO

import json

from pyang import plugin
from pyang import statements
from pyang import util
from xml2json import json2xml

__author__ = 'camoberg@tail-f.com,sunseawq@huawei.com'
__copyright__ = "Copyright (c) 2015, Carl Moberg, Qin Wu"
__license__ = "New-style BSD"
__email__ = "camoberg@cisco.com,sunseawq@huawei.com"
__version__ = "0.2.1"

def pyang_plugin_init():
    plugin.register_plugin(ModuleCatalogPlugin())

class ModuleCatalogPlugin(plugin.PyangPlugin):

    def add_output_format(self, fmts):
    	fmts['module-catalog'] = self

    def add_opts(self, optparser):
        optlist = [
            optparse.make_option('--module-catalog-format',
            	type = 'choice',
            	dest = 'outputFormat',
            	choices=['xml', 'json'],
            	default='xml',
            	help = 'Swagger debug'),
            ]

        g = optparser.add_option_group("YANG Module Schema-specific options")
        g.add_options(optlist)

    def setup_ctx(self, ctx):
        ctx.opts.stmts = None

    def setup_fmt(self, ctx):
        ctx.implicit_errors = False

    def print_json(self, data):
        print(json.dumps(data))

    def print_xml(self, data):
        jsonstring = json.dumps(data)
        decodedstring=json.loads(jsonstring)
        #print(decodedstring)
        jsondata = {data['name']:decodedstring}
        print(json2xml(jsondata))

    def emit(self, ctx, modules, fd):
		me = ModuleCatalogEmitter()
		result = me.emit(ctx, modules)
		# print(result)
		if fd:
			fqfd = os.getcwd() + '/' + fd.name
                        if os.path.isfile(fqfd):
                		print("File '%s' exists" % fqfd)
                		return
		fd.write("%s" % result)
		if ctx.opts.outputFormat == 'json':
			self.print_json(result)
		else:
			self.print_xml(result)
		fd.close()

class ModuleCatalogEmitter(object):
	def emit(self, ctx, modules):
		res = {}
		for module in modules:

		# Here are the top-level leafs from the draft:
		# +--rw name                string -> is the 'module' statement
		# +--rw namespace?          string DONE
		# +--rw prefix?             string DONE
		# +--rw revision?           string DONE
		# +--rw summary?            string -> Can't be inferred from module
		# +--rw module-version?     string -> Can't be inferred from module

			res['name'] = module.arg
			for statement in ['namespace','description', 'prefix', 'revision', 'module-version']:
				stmt = module.search_one(statement)
				if stmt:
					if statement == 'description':
						res['summary'] = stmt.arg
					else:
						res[stmt.keyword] = stmt.arg
			return res


