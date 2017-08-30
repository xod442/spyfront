
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
from utilities.save_vxlan_db import *
from init.models import Vxlan, Inventory, Creds




vxlan_app = Blueprint('vxlan_app', __name__)

@vxlan_app.route('/new_tunnel', methods=('GET', 'POST'))
def new_tunnel():
    '''
    Query user for point to point switches to build vxlans
    '''
    switch_list = []
    device = Inventory.objects()
    for dev in device:
        switch_list.append(dev['sip'])

    if request.method == 'POST':
        mod_hosts = []
        new_hosts = []
        # Get selections from user
        vlan = request.form['vlan']
        from_ip = request.form['from_ip']
        to_ip = request.form['to_ip']

        if to_ip == from_ip:
            return render_template('vxlan/match_switches.html', from_ip=from_ip, to_ip=to_ip)
        switch_list = [from_ip, to_ip]

        #if 'none selected'in switch_list:
            #return render_template('vxlan/none_selected.html', switch_list=switch_list)

        # Get two lists of vxlan dicts. One for update and another new build
        modified_vxlans, processed_list = modify_existing_vxlans(switch_list,vlan)

        # remove any switches that were processed for existing vxlans
        new_list = set(switch_list) - set(processed_list)
        # Turn the set back into a python list
        new_list = list(new_list)

        #'Now build new vxlans
        #new_vxlans = process_new_vxlans(new_list,vlan)
        new_vxlans = process_new_vxlans(new_list,vlan, processed_list)

        # Send vxlan dict list to configlet builder
        response = arista(modified_vxlans,new_vxlans)


        # Save the modified vxlan information to the Subway mongodb
        if modified_vxlans:
            mod_response = modified_writer(modified_vxlans)


        # Save the modified vxlan information to the Subway mongodb
        if new_vxlans:
            new_response = new_writer(new_vxlans)



        for i in modified_vxlans:
            host = i['host']
            result = cvp(host)
            mod_hosts.append(host)
        for i in new_vxlans:
            host = i['host']
            result = cvp(host)
            new_hosts.append(host)

        return render_template('vxlan/tunnel_up.html',modified=mod_hosts, new=new_hosts)

    return render_template('vxlan/point2point.html', switch_list=switch_list)



@vxlan_app.route('/new_multi', methods=('GET', 'POST'))
def new_multi():
    '''
    Query user for list of switches to build vxlans
    '''
    switch_list = []
    device = Inventory.objects()
    for dev in device:
        switch_list.append(dev['sip'])

    if request.method == 'POST':
        mod_hosts = []
        new_hosts = []

        # Get selections from user
        switch_1 = request.form['ip_one']
        switch_2 = request.form['ip_two']
        switch_3 = request.form['ip_three']
        switch_4 = request.form['ip_four']
        switch_5 = request.form['ip_five']
        vlan = request.form['vlan']
        switch_list = [switch_1,switch_2,switch_3,switch_4,switch_5]
        if 'none selected'in switch_list:
            return render_template('vxlan/none_selected.html', switch_list=switch_list)

        if len(switch_list) != len(set(switch_list)):
            return render_template('vxlan/dupe_switches.html', switch_list=switch_list)

        # Get two lists of vxlan dicts. One for update and another new build
        modified_vxlans, processed_list = modify_existing_vxlans(switch_list,vlan)
        new_vxlans = process_new_vxlans(processed_list,vlan)

        # Send vxlan dict list to configlet builder
        response = arista(modified_vxlans,new_vxlans)

        for i in modified_vxlans:
            host = i['host']
            result = cvp(host)
            mod_hosts.append(host)
        for i in new_vxlans:
            host = i['host']
            result = cvp(host)
            new_hosts.append(host)


        return render_template('vxlan/tunnel_up.html',modified=mod_hosts, new=new_hosts)


    return render_template('vxlan/multi_point.html', switch_list=switch_list)
