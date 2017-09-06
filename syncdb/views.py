
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

Flask script that manages ansible variables for Arista Switches

# Read single example
# x = db.vlan.find_one({"vlanId" : 399})

# Read all
# x = db.vlan.find_one()

# write one document
# app_keys.insert({dict})

'''
from flask import Blueprint, render_template, request, redirect, session, url_for, abort, flash
import os
from werkzeug import secure_filename
import pymongo
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader, Template
from hpOneView.oneview_client import OneViewClient


sync_app = Blueprint('sync_app', __name__)

@sync_app.route('/sync', methods=('GET', 'POST'))
def sync():
    '''
    Get the OneView creds from db
    '''

    client = MongoClient('mongo', 27017)
    db = client.creds

    try:
        # define the collections
        auth_info = db.keyz.find()
    except:
        error = "Failed to get credentials from database"
        return render_template('sync/autherror.html', error=error)

    # Assign the local variable
    ovip = auth_info[0]['ovip']
    ov_user = auth_info[0]['ov_user']
    ov_word = auth_info[0]['ov_word']

    config = {
        "ip": ovip,
        "credentials": {
            "userName": ov_user,
            "password": ov_word
        }
    }

    # Switch to the main database
    db = client.pov2

    # define the collections
    vlans = db.vlan
    netsets = db.netset
    ligs = db.lig

    # Create OneView Client connection
    oneview_client = OneViewClient(config)
    # vlans
    try:
        # Get all, etheret-networks and write to the vlan collection
        ethernet_nets = oneview_client.ethernet_networks.get_all()
        for net in ethernet_nets:
            vlans.insert(net)
    except:
        error = "Application did not return list of ethernet-networks"
        return render_template('sync/dberror.html', error=error)

    # netsets
    try:
        # Get all, etheret-networks and write to the vlan collection
        sets = oneview_client.network_sets.get_all()
        for setz in sets:
            netsets.insert(setz)
    except:
        error = "Application did not return list of network-sets"
        return render_template('sync/netseterror.html', error=error)

    # logical interconnect group
    try:
        # Get all, etheret-networks and write to the vlan collection
        ligz = oneview_client.logical_interconnect_groups.get_all()
        for lig in ligz:
            ligs.insert(lig)
    except:
        error = "Application did not return list of Logical interconnect Groups"
        return render_template('sync/ligerror.html', error=error)

    return render_template('main/mainx.html')
