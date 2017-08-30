
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
x[u'floods']= [ { "floods" : [ "10.132.0.189"], "vlan" : "102" }, { "floods" : [ "10.132.0.189" ], "vlan" : "30000" } ]
x[u'sip'] = '10.132.0.184'
x[u'host'] = 'pod2.leaf01'

y['sint'] = "loopback1"
y[u'vni'] = [ { "vlan" : "102", "vni" : 10200 }, { "vlan" : "3000", "vni" : 30000 } ]
y[u'floods'] = [ { "floods" : [ "10.132.0.184" ], "vlan" : "102" }, { "floods" : [ "10.132.0.184"], "vlan" : "30000" } ]
y[u'sip'] = "10.132.0.189"
y[u'host'] = 'pod2.leaf06'

vxlan = [x,y]
vlan = "102"
switch_list = ['10.132.0.188', '10.132.0.185', '10.132.0.182', '10.132.0.184', '10.132.0.189']
c = 0
modified_vxlans = []
established_floods = []

# Iterate through all the switches, look for updates
for vx in vxlan:
    print c
    vxlan= {}
    update_list = []
    new_flood = {}
    local_ip = []
    current_flood = []


    # This switch has a vxlan interface check to see if it belongs to the vlan
    # Get the vni to vlan map...it could be a list a list
    vni = vx[u'vni']
    print 'this is the vni %s' % (vni)
    # There will be only one match from a long list of mappings.
    for vmap in vni:
        #The vxlan is part of the vlan from the end user
        if vmap[u'vlan'] == vlan:
            established_floods.append(vx[u'sip'])
            print "this is the established %s" % (established_floods)
            print "vlan %s is in the vni_map" % (vlan)
            # vni is defined
            vxlan['vni'] = vni
            print vxlan
            # Pull apart floods and insert flodlist
            for flood in vx[u'floods']:
                print "checking floods....."
                # Look at all the floodlists in the vxlan interfacs and match on vlan
                if flood[u'vlan'] == vlan:
                    print '=========VLAN in======FLOODS==================='

                    # If the switches IP is in the switch_list pop it out.
                    print "here is what is in the current floods %s" % (flood[u'floods'])
                    if vx[u'sip'] in switch_list:
                        print "this is the switch_list %s and the is the current sip %s" % (switch_list, vx[u'sip'])
                        # Make a list of just the local IP
                        local_ip.append(vx[u'sip'])
                        print "this is the %s" % (local_ip)
                        # Remove local switch IP from switchlist
                        new_list = set(switch_list) - set(local_ip)

                        # Turn the set back into a python list
                        new_list = list(new_list)

                        x_list = set(new_list) - set(flood[u'floods'])
                        x_list = list(x_list)
                        print 'this is the x list %s' % (x_list)
                        new_flood[u'floods'] = flood[u'floods']+x_list
                        'this is the final flood %s' % (new_flood[u'floods'])

                    else:
                        print '=============ELSE SWITCH NOT IN SWITCH LIST++++++++++++'
                        x_list = set(switch_list) - set(flood[u'floods'])
                        x_list = list(x_list)
                        new_flood[u'floods'] = flood[u'floods']+x_list

                        print '=====NOT IN SWITCH_LIST======================='
                        print 'this is the new flood %s ' % (new_flood[u'floods'])
                    # Now we have two sets of devices to process. New and update
                    # Create ne wfloodlist dictionary


                    new_flood[u'vlan'] = vlan

                    print '=========update list========================'
                    # Add dict to temporary collection of floods
                    update_list.append(new_flood)
                    #print "the update list inside the current loop %s" % (update_list)

                else:
                    # If flood is not the same vlan, collect them for later
                    update_list.append(flood)
                    #print "This is the update list without matching vlan %s" % (update_list)

            print '=========vxlan interface====================='
            vxlan['floods'] = update_list
            #print vxlan
            vxlan['sint'] = vx[u'sint']
            #print vxlan


            vxlan['host'] = vx[u'host']
            print vxlan
            modified_vxlans.append(vxlan)
            print '=========modified list================='
            print modified_vxlans

            print "=======================GET NEXT========================="
    c = c + 1
