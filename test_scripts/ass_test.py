#!/usr/bin/env python
'''
2016 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman" ]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

A script that uses cvprac to communicate with a CVP server
It applies a switches vxlan configlet to the device and clears up any outstanding tasks

Processes any pending tasks
'''
from flask import Blueprint, render_template, send_file, request, redirect, session, url_for, abort, flash
import bcrypt
import uuid
import os
from werkzeug import secure_filename
from mongoengine import Q

from settings import APP_STATIC
from utilities.build_db import *
from utilities.tunnel import *
from init.models import Vxlan, Inventory, Creds
from cvprac.cvp_client import CvpClient


cvp = '10.132.0.77'
cvp_user = 'cvpadmin'
cvp_word = 'Grape123'
print cvp
print cvp_user
print cvp_word

c = CvpClient()
# Connect to the CVP server
c.connect([cvp],cvp_user,cvp_word)

# get devices from inventory assign to result, a python dictionary
result = c.api.get_inventory()

print result

host = 'pod2.leaf02'

# Iterate through the result dictionary
for dev in result:
    switch_name = dev['fqdn']
    print switch_name
    if switch_name == host:
        print 'in the loop ---------------------------------------'
        switch_name = switch_name.encode('utf-8')
        print switch_name
        # Configlet name
        configlet_name = switch_name+'.vxlan'
        print " ====================Name of configlet++++++++++++++++="
        print configlet_name
        print " ====================Name of URL++++++++++++++++="
        url = '/configlet/getConfigletByName.do?name=%s' % (configlet_name)
        print url
        # Get all configlets from CVP result2 is a python dictionary
        new_configlet = c.get(url)
        print " ====================The configlet++++++++++++++++="
        print new_configlet
        # Get the device dictionary
        dev_dict = c.api.get_device_by_name(switch_name)
        print " ====================The Device dict++++++++++++++++="
        print dev_dict
        # Apply the configlet
        #results = c.api.apply_configlets_to_device("Script: Add configlet to device",dev_dict,new_configlet)

    '''

    # Clear up outstanding tasks
    tasks = c.api.get_tasks_by_status('Pending')
    for tasks in tasks:
        task_id = tasks['workOrderId']
        c.api.execute_task(task_id)
        # poll c.api.get_task_by_id(task_id) until status['taskStatus'] == 'COMPLETED'
    '''
