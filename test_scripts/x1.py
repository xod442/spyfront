


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
from pyhpeimc.auth import *
from pyhpeimc.plat.icc import *
from jinja2 import Environment, FileSystemLoader, Template
import json


# Track position in doc[] elements
count = 0

auth = IMCAuth("http://","10.132.0.15", "8080", "admin", "admin")

ENV = Environment(loader=FileSystemLoader('./'))

# Open YAML file for processing
f = open(os.path.join(APP_STATIC, 'all.yaml'), 'r')
file = f.read()
f.close()

# Take the contents of the all.yaml file and make it a python dictionary
doc=yaml.load(file)


#define the switch
switch = {}

for switches in doc[3]['fabric']:
    for key in switches:
        switchname = key
        print '______________________________>%s' % (switchname)
        switch['username'] = doc[0]['provider'][0]['username'] # username
        switch['password'] = doc[0]['provider'][1]['password'] # pwssword


        # Gateway
        switch['gateway'] = [doc[1]['gateway'][0]['gateway']] # gateway]

        # Create a temporary file to store the interface configlet
        switch['asn'] = doc[3]['fabric'][count][switchname][0]['asn'] # asn

        peers = []
        nets = []

        for peer in doc[3]['fabric'][count][switchname][1]['fabricpeers']:
             peers.append(peer)

        for net in doc[3]['fabric'][count][switchname][2]['networks']:
            nets.append(net)
        switch['peers'] = peers
        switch['nets'] = nets

        # Create a temporary file to store the interface configlet
        switch['process'] = doc[5]['ospf'][count][switchname][0]['process']

        switch['rid'] = doc[5]['ospf'][count][switchname][1]['router_id']

        ospf_nets = []

        for net in doc[5]['ospf'][count][switchname][2]['networks']:
            ospf_nets.append(net)

        switch['ospf_nets'] = ospf_nets

        key_counter = 0
        # a disct for each interface
        xface = {}
        # a list of interface dictioaries
        interface_list = []

        description = 'Production Interface'
        mask = '255.255.255.0'

        for face in doc[6]['interface'][count][switchname]:
            for key in face:
                xface['ifdesc'] = key
            ip = doc[6]['interface'][count][switchname][key_counter][key][0]['ipv4']
            #print doc[6]['interface'][count][switchname][key_counter]
            xface['description'] = description
            xface['ipaddress'] = ip
            xface['ifdesc'] = key
            xface['mask'] = mask
            key_counter = key_counter + 1
            interface_list.append(xface)
            xface = {}



        # interface_list
        switch['interfaces'] = interface_list

        #hostname
        hostname = doc[2]['mgmt'][count][switchname][0]['hostname']
        switch['hostname'] = hostname

        #get loopback ip and mask
        description = 'Loopback0'
        loopback = doc[2]['mgmt'][count][switchname][1]['loopback0_ip']
        switch['loopback'] = loopback

        # get management ip and mask

        management = doc[2]['mgmt'][count][switchname][2]['management_ip']
        switch['management'] = management

        # process the enablepeers for comware bgp

        enablepeers = doc[4]['bgp-peers'][count][switchname][0]['enablepeers']
        switch['enablepeers'] = enablepeers



    print '////////////////////////////////////////////////'
    #print switch

    template = ENV.get_template("./templates/comware.j2")

    f = open(os.path.join(APP_STATIC, 'comware_configs/'+hostname+'.cfg'), 'w')

    filename = hostname+'.cfg'

    #f.write(template.render(switch=switch))

    config = template.render(switch=switch)

    #print config

    create_new_file = create_cfg_segment(filename,config,'Comware Configuration',auth.creds,auth.url)


    count = count + 1
