
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
import bcrypt
import uuid
import os
from werkzeug import secure_filename
from mongoengine import Q
from configlets.arista_config_build import *
from configlet_assign.assignlet import *
from settings import APP_STATIC
from utilities.build_db import *
from utilities.process_vxlans import *
from init.models import Vxlan, Inventory, Creds
x = {}
y = {}
x[u'sint'] = "loopback0"
x[u'vni'] = [ { "vlan" : u"102", "vni" : u'10200' }, { "vlan" : u"3000", "vni" : u'30000' } ]
x[u'floods']= [ { "floods" : [ u"10.132.0.189",u"10.10.10.10",u"12.12.12.12"], "vlan" : u"102" }, { "floods" : [ u"10.132.0.189" ], "vlan" : u"30000" } ]
x[u'sip'] = '10.132.0.184'
x[u'host'] = 'pod2.leaf01'

y['sint'] = "loopback1"
y[u'vni'] = [ { "vlan" : u"102", "vni" : u'10200' }]
y[u'floods'] = [ { "floods" : [ u"10.132.0.184",u"10.132.0.111",u"10.132.0.12" ], "vlan" : u"102" } ]
y[u'sip'] = "10.132.0.189"
y[u'host'] = 'pod2.leaf06'

vxlans = [x,y]
vlan = "102"
switch_list = ['10.132.0.188', '10.132.0.185', '10.132.0.182','10.132.0.184','10.132.0.189']
vxlan = {}
for v in vxlans:

    temp_flood =[]
    # Build record to write to mongo database
    sint = v['sint'].encode('utf-8')
    sip = v['sip'].encode('utf-8')
    vni = v['vni']
    floods = v['floods']

    temp_vni = []
    for v in vni:
        new_vni = {}
        #print 'there are %d in vni' % (len(vni)
        x_vlan = v['vlan']
        x_vni = v['vni']
        x_vlan = x_vlan.encode('utf-8')
        x_vni = x_vni.encode('utf-8')
        new_vni['vni'] = x_vni
        new_vni['vlan'] = x_vlan
        temp_vni.append(new_vni)
    vni = temp_vni


    for f in floods:
        new_flood = {}
        temp_flood_list = []
        x_flood = f['floods']
        x_fvlan = f['vlan']
        new_flood['vlan'] = x_fvlan.encode('utf-8')
        for i in x_flood:
            i = i.encode('utf-8')
            temp_flood_list.append(i)
        new_flood['floods'] = temp_flood_list
        new_flood['vlan']
        temp_flood.append(new_flood)
    flood = temp_flood

    vxlan['sip'] = sip
    vxlan['sint'] = sint
    vxlan['vni'] = vni
    vxlan['floods'] = flood
    print '----------------------------------------------------'
    print vxlan
    print '----------------------------------------------------'
