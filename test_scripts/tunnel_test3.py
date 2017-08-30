
'''
 2017 wookieware.

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

Flask script that builds a configlet of interface vxlan 1 as saves file
'''

from jsonrpclib import Server
from cvprac.cvp_client import CvpClient
from flask import Blueprint, render_template, send_file, request, redirect, session, url_for, abort, flash
import bcrypt
import uuid
import os
from werkzeug import secure_filename
from mongoengine import Q
from configlets import arista_config_build
from configlet_assign import assignlet
from settings import APP_STATIC
from utilities.build_db import *
from init.models import Vxlan, Inventory, Creds

x = {}
y = {}
x[u'sint'] = "loopback0"
x[u'vni'] = [ { "vlan" : "102", "vni" : 10200 }, { "vlan" : "3000", "vni" : 30000 } ]
x[u'floods']= [ { "floods" : [ "10.132.0.189","10.10.10.10","12.12.12.12"], "vlan" : "102" }, { "floods" : [ "10.132.0.189" ], "vlan" : "30000" } ]
x[u'sip'] = '10.132.0.184'
x[u'host'] = 'pod2.leaf01'

y['sint'] = "loopback1"
y[u'vni'] = [ { "vlan" : "102", "vni" : 10200 }]
y[u'floods'] = [ { "floods" : [ "10.132.0.184","10.132.0.111","10.132.0.12" ], "vlan" : "102" } ]
y[u'sip'] = "10.132.0.189"
y[u'host'] = 'pod2.leaf06'

vxlan = [x,y]
vlan = "102"
switch_list = ['10.132.0.188', '10.132.0.185', '10.132.0.182', '10.132.0.184', '10.132.0.189']
c = 0
modified_vxlans = []
established_floods = []
new_flood = {}
new_flood_list = []
vx = {}
print x
print "============================================================================"
for fl in x[u'floods']:
    new_flood = {}
    temp_flood = ','.join(fl['floods'])
    temp_flood = temp_flood.replace(',',' ')
    print 'this is the temp flood ==>  %s ' % (temp_flood)
    new_flood['floods'] = temp_flood
    new_flood['vlan'] = vlan
    new_flood_list.append(new_flood)

vx['mod_floods'] = new_flood_list
print 'this is the new_flood list %s' % (vx['mod_floods'])
