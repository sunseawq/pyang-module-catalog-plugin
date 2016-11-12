"""YANG module catalog data generator
"""
from __future__ import print_function

import optparse
import sys
import re
import string
import logging
import os
import cgi
import types
import StringIO

import json

from pyang import plugin
from pyang import statements
from pyang import util
from xml2json import json2xml
import xml.etree.ElementTree as ET
import bottle

pyangout = '/pyang-master'

def xml_indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            xml_indent(e, level + 1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem

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
        jsondata = {data['name']:jsonstring}
        #print(jsondata)
        #d ={'r':{'@p': 'p1','#text': 't1', 'c': 't2'}}
        print(json2xml(jsondata))
        #print("%s" %json2xml(jsondata))
        #e = {'prefix': 'if', 'namespace': 'urn:ietf:params:xml:ns:yang:ietf-interfaces', 'name': 'ietf-interfaces', 'revision': '2014-05-08'}
        #f = {'r':'r1','#text1':'t2'}
        #g = {'module':f}
        #print(g)
        #pyOutput = cgi.escape(json2xml(jsondata))
        #splitStr = ""
        #if ("\n" in pyOutput):
        #    splitStr = "}\n&lt;"
        #else:
        #    splitStr = "}&lt;"
        #outputList = pyOutput.split(splitStr)

       # jsonOutputTmp = outputList[0] + "}"
       # outputJson = json.loads(jsonOutputTmp)
       # jsonOutputTmp = json.dumps(outputJson, indent=2)

        #xmlOutputTmp = "&lt;" + outputList[1]
        #xmlOutputTmp = xmlOutputTmp.replace("&lt;", "<")
        #xmlOutputTmp = xmlOutputTmp.replace("&gt;", ">")
        #outputXmlET_tmp = ET.fromstring(xmlOutputTmp)
        #outputXmlET = xml_indent(outputXmlET_tmp, 0)
        #xmlOutputTmp = ET.tostring(outputXmlET)

        #xmlOutputTmp = xmlOutputTmp.replace("<", "&lt;")
        #xmlOutputTmp = xmlOutputTmp.replace(">", "&gt;")
        #print(xmlOutputTmp)

    def emit(self, ctx, modules, fd):
        me = ModuleCatalogEmitter()
        result = me.emit(ctx, modules)
        if ctx.opts.outputFormat == 'json':
            self.print_json(result)
        else:
            #self.print_xml(result)
            jsonstring = json.dumps(result)
            decodedstring=json.loads(jsonstring)
            jsondata = {result['name']:decodedstring}
            print(json2xml(jsondata))
            #pyOutput = json2xml(jsondata)
            #splitStr = ""
            #if ("\n" in pyOutput):
            #    splitStr = "}\n&lt;"
            #else:
            #    splitStr = "}&lt;"
            #outputList = pyOutput.split(splitStr)
            # jsonOutputTmp = outputList[0] + "}"
            # outputJson = json.loads(jsonOutputTmp)
            # jsonOutputTmp = json.dumps(outputJson, indent=2)
            #xmlOutputTmp = "&lt;" + outputList[0]
            #xmlOutputTmp = xmlOutputTmp.replace("&lt;", "<")
            #xmlOutputTmp = xmlOutputTmp.replace("&gt;", ">")
            #outputXmlET_tmp = ET.fromstring(xmlOutputTmp)
            #outputXmlET = xml_indent(outputXmlET_tmp, 0)
            #xmlOutputTmp = ET.tostring(outputXmlET)
            #xmlOutputTmp = xmlOutputTmp.replace("<", "&lt;")
            #xmlOutputTmp = xmlOutputTmp.replace(">", "&gt;")
            #print(xmlOutputTmp)
        #if fd.name == '<stdout>':
        #    fn= ""
        #    print(fn)
        #else:
        #    fn=fd.name
        #    print(fn)
        #print(fd.name[1:])

        #if fn != "":
                #fqfd = os.getcwd() + '/' + fn
                #print(fqfd)
                #if os.path.isfile(fqfd):
                #    print("File '%s' exists" % fqfd)
                #    return
                #else:
                #    fd.write("%s" % result)
                #    fd.close()
        #else:
        #    print("output file name can not be determined")
        #    #else:
        #       #     fd.write("%s" % result)
        if fd:
#            fd.write("%s" % result)
###         print json
            fd.write("%s" % json.dumps(result))
            fd.write("\r\n")

###         print xml
            jsonstring = json.dumps(result)
            decodedstring=json.loads(jsonstring)
            jsondata = {result['name']:decodedstring}
            print(json2xml(jsondata))
            fd.write("%s" % json2xml(jsondata))
            fd.close()
        #fd.close()
        
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
			for statement in ['namespace','prefix', 'revision', 'module-version']:
				stmt = module.search_one(statement)
				if stmt:
					if statement == 'description':
						res['summary'] = stmt.arg
					else:
						res[stmt.keyword] = stmt.arg
			return res


