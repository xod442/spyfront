
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

Flask script that processes existing vlan interface flood lists and vni
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
from configlet_assign.assignlet import *
from settings import APP_STATIC
from utilities.build_db import *
from utilities.tunnel import *
from vxlan_builder import *
from init.models import Vxlan, Inventory, Creds


def modify_existing_vxlans(switch_list,vlan):

    vxlans = Vxlan.objects()

    new_vxlan_list = []
    modified_vxlan_list = []
    established_floods = []
    counter = 0
    process_list = []
    # Iterate through all the switches, look for updates
    for vx in vxlans:
        #print 'for vx in vxlans counter is %s' % (counter)
        vxlan = {}
        update_list = []
        new_flood = {}
        local_ip = []
        current_flood = []
        new_vxlan = {}
        mod_vxlan = {}
        # This switch has a vxlan interface check to see if it belongs to the vlan
        # Get the vni to vlan map...it could be a list a list
        vni = vx[u'vni']
        sip = vx[u'sip']

        temp_vni = []
        for vmap in vni:
            #The vxlan is part of the vlan from the end user
            temp = vmap[u'vlan']
            temp_vni.append(temp)

        #print 'this is the temp vni list %s' % (temp_vni)

        if vlan in temp_vni and sip in switch_list:
            #print 'match vni list ....modifying...'
            # Modify the floods, keep vni the same
            mod_vxlan =  modify_existing_vxlan(vx,switch_list,vlan)
            mod_vxlan['sint'] = vx[u'sint']
            mod_vxlan['sip'] = vx[u'sip']
            process_list.append(mod_vxlan['sip'])
            modified_vxlan_list.append(mod_vxlan)

        if vlan in temp_vni and sip not in switch_list:
            #print 'match vni list ....modifying...'
            # Modify the floods, keep vni the same
            mod_vxlan =  modify_existing_vxlan(vx,switch_list,vlan)
            mod_vxlan['sint'] = vx[u'sint']
            mod_vxlan['sip'] = vx[u'sip']
            process_list.append(mod_vxlan['sip'])
            modified_vxlan_list.append(mod_vxlan)

        if vlan not in temp_vni and sip in switch_list:
            #print 'match vni list ....modifying...'
            # Modify the floods, keep vni the same
            mod_vxlan =  modify_existing_vxlan(vx,switch_list,vlan)
            mod_vxlan['sint'] = vx[u'sint']
            mod_vxlan['sip'] = vx[u'sip']
            process_list.append(mod_vxlan['sip'])
            modified_vxlan_list.append(mod_vxlan)

    return modified_vxlan_list, process_list


def process_new_vxlans(new_switch_list,vlan,processed_list):

    new_vxlan_list = []

    for switch in new_switch_list:

        new_flood = {}
        new_vxlan = {}
        new_list = []
        local_ip = []
        new_vni = {}
        new_vni_list = []
        new_flood_list = []

        local_ip.append(switch)
    
        device = Inventory.objects(sip=switch).first()
        new_vxlan['host'] = device['host']

        if device['mlag'] == 'no':
            new_vxlan['sint'] = 'loopback 0'
        else:
            new_vxlan['sint'] = 'loopback 1'

        # Remove local switch IP from switchlist
        new_list = set(new_switch_list) - set(local_ip)
        # Turn the set back into a python list
        new_list = list(new_list)

        new_flood['floods'] = new_list+processed_list
        new_flood['vlan'] = vlan.encode('utf-8')
        new_flood_list.append(new_flood)

        xx_vni = vlan.encode('utf-8')+'00'

        new_vni['vni'] = xx_vni
        new_vni['vlan'] = vlan.encode('utf-8')
        new_vni_list.append(new_vni)

        #print 'this is the vinny %s' % (vxlan['vni'])
        new_vxlan['floods'] = new_flood_list
        new_vxlan['sip'] = switch.encode('utf-8')
        new_vxlan['vni'] = new_vni_list

        new_vxlan_list.append(new_vxlan)

    #fail.append('rick')
    return new_vxlan_list
