


'''
2016 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Flask script that manages ansible variables for Arista Switches
'''
from flask import Blueprint, render_template, send_file, request, redirect, session, url_for, abort, flash

from settings import APP_STATIC, APP_TEMPLATE
import yaml
import os
from jinja2 import Environment, FileSystemLoader, Template
import json
from cvprac.cvp_client import CvpClient
from cvprac.writer import writer
from cvprac.writer import writer2
from init.models import Vxlan, Inventory, Creds
vx = {}
y = {}

vx[u'sint'] = "loopback0"
vx[u'vni'] = [ { "vlan" : "102", "vni" : 10200 }, { "vlan" : "3000", "vni" : 30000 } ]
vx[u'floods']= [ { "floods" : [ "10.132.0.189"], "vlan" : "102" }, { "floods" : [ "10.132.0.189" ], "vlan" : "30000" } ]
vx[u'sip'] = '10.132.0.184'
vx[u'host'] = 'pod2.leaf01'

y['sint'] = "loopback1"
y[u'vni'] = [ { "vlan" : "102", "vni" : 10200 }, { "vlan" : "3000", "vni" : 30000 } ]
y[u'floods'] = [ { "floods" : [ "10.132.0.184" ], "vlan" : "102" }, { "floods" : [ "10.132.0.184"], "vlan" : "30000" } ]
y[u'sip'] = "10.132.0.189"
y[u'host'] = 'pod2.leaf06'


cvp = '10.132.0.77'
cvp_user = 'cvpadmin'
cvp_word = 'Grape123'

c = CvpClient()
# Connect to the CVP server
c.connect([cvp], cvp_user, cvp_word)

# Track position in doc[] elements
count = 0

ENV = Environment(loader=FileSystemLoader('./'))

# Update existing vxlan configlets

template = ENV.get_template("./templates/vxlan.arista2.j2")

# Render the python dictionary to the jina2 template
config = template.render(vx=vx)
# Create a python dictionary to pass to the API

hostname = vx[u'host']+".vxlan"

url = '/configlet/getConfigletByName.do?name=%s' % (hostname)
print hostname
get_configlet = c.get(url)
key = get_configlet['key']
print 'this is the key %s' % (key)

add_config = {'config': config, 'key':key, 'name':hostname}
# Call the CVP API to add the configlet
config_result = c.post('/configlet/updateConfiglet.do', add_config)
