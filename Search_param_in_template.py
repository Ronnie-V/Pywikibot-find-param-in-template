#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pywikibot
import re
import csv
from pywikibot import pagegenerators as pg
import sys

template = ''
param = ''
showvalues = ''

if len(sys.argv) <3:
  print (f"Dit script moet aangeroepen worden met twee parameters: py {sys.argv[0]} sjabloonnaam parameter")
  print (f"De derde parameter is optioneel en zorgt ervoor dat naast de paginatitel ook de waarde wordt opgeslagen: py {sys.argv[0]} sjabloonnaam parameter True")
  quit()
else:
  template = sys.argv[1]
  param = sys.argv[2]
  if len(sys.argv) > 3:
    showvalues = sys.argv[3]

print (template, param, showvalues) 

def list_template_usage(site_obj, tmpl_name):
    name = "{}:{}".format(site_obj.namespace(10), tmpl_name)
    tmpl_page = pywikibot.Page(site_obj, name)
    page = pywikibot.Page(pywikibot.Link(template,
                                         default_namespace=10,
                                         source=site))
    return page.getReferences(only_template_inclusion=True)

def FindParamExists(page, param):
    regex = f'\|(\s)*{param}(\s)*=(\s)*(.+)'
    res = re.compile(regex).search(page.text)
    if res:
      value = True
    else:
      value = False
    return value

def GetParamValue(page, param):
    regex = f'\|(\s)*{param}(\s)*=(\s)*(.+)'
    res = re.compile(regex).search(page.text)
    if res:
      value = res.group(4)
    else:
      value = ""
    return value

site = pywikibot.Site('nl', 'wikipedia')
gen = list_template_usage(site, template)
print ( gen.length() )
t = 0
if showvalues != "":
  with open(f"output_{param}_in_{template}.csv", "w", newline="", encoding='utf-8') as csvf:
    fields = ["pagetitle", "value"]
    writer = csv.DictWriter(csvf, fieldnames=fields)
    writer.writeheader()
    for page in gen:
      t += 1
      if t % 100 == 0:
        print (t)
      value = GetParamValue(page, param)
      if value != "":
        writer.writerow({"pagetitle": page.title(), "value": value})
else: 
  with open(f"output_{param}_in_{template}.csv", "w", newline="", encoding='utf-8') as csvf:
    fields = ["pagetitle"]
    writer = csv.DictWriter(csvf, fieldnames=fields)
    writer.writeheader()
    for page in gen:
      t += 1
      if t % 100 == 0:
        print (t)
      if FindParamExists(page, param):
        writer.writerow({"pagetitle": page.title()})
        
print (t)        