
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

Flask script that manages mongo database tables

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

init_app = Blueprint('init_app', __name__)

@init_app.route('/init', methods=('GET', 'POST'))
def init():
    '''
    Create a Mongo database to store the user credentials
    '''

    # Create client connector (db is running in a container)
    client = MongoClient('mongo', 27017)

    # Define credentials database
    db = client.creds

    # define the collections
    app_keys = db.keyz

    # Get the credentials from the log in screen
    ovip = request.form['ovip']
    ov_user = request.form['ov_user']
    ov_word = request.form['ov_word']

    creds = {"ovip" : ovip, "ov_user" : ov_user, "ov_word" : ov_word}

    # Test the creds against the ip address
    try:
        config = {
            "ip": ovip,
            "credentials": {
                "userName": ov_user,
                "password": ov_word
            }
        }
        # Create a client
        oneview_client = OneViewClient(config)

        # Get all, with defaults
        ethernet_nets = oneview_client.ethernet_networks.get_all()

    except:
        error = "Invlaid Username or Password"
        return render_template('init/autherror.html', error=error, e=ov_user)

    # Save the record
    try:
        app_keys.insert(creds)

    except:
        error = "Failed in the Creds database write"
        return render_template('init/dberror.html', error=error)


    return render_template('main/mainx.html')

@init_app.route('/show_networks', methods=('GET', 'POST'))
def show_networks():
    '''
    # Reports on vlans learned from OneView
    '''
    client = MongoClient('mongo', 27017)

    # Define credentials database
    db = client.pov2

    try:
        # Read all vlan records
        networks = db.vlan.find()

    except:
        error = "Failed to read the vlan database"
        return render_template('init/dberror.html', error=error)


    return render_template('init/show_networks.html', networks=networks)

@init_app.route('/show_network_sets', methods=('GET', 'POST'))
def show_network_sets():
    '''
    # Reports on vlans learned from OneView
    '''
    client = MongoClient('mongo', 27017)

    # Define credentials database
    db = client.pov2

    try:
        # Read all vlan records
        network_sets = db.netset.find()

    except:
        error = "Failed to read the net-set database"
        return render_template('init/dberror.html', error=error)


    return render_template('init/show_network_sets.html', network_sets=network_sets)

@init_app.route('/show_lig', methods=('GET', 'POST'))
def show_lig():
    '''
    # Reports on vlans learned from OneView
    '''
    client = MongoClient('mongo', 27017)

    # Define credentials database
    db = client.pov2

    try:
        # Read all vlan records
        ligs = db.lig.find()

    except:
        error = "Failed to read the LIG database"
        return render_template('init/dberror.html', error=error)

    # Parse the lig info..it will be a List...make some list to store info
    link = []
    links = []
    newNets = []
    lig_data = []
    lig_list = []
    # print c7000/Synergy port configurations

    for i in ligs:
        name = i['name']
        desc = i['description']
        state = i['state']
        for j in i['uplinkSets']:
            for k in j['logicalPortConfigInfos']:
                for l in k['logicalLocation']['locationEntries']:
                    ident = l['type']
                    value = l['relativeValue']
                    info = ident+'-'+str(value)
                    link.append(info)
                    link.sort()
                links.append(link)
                link = []
        sets = links            # List of uplinks ports on frame

        for vlan in j['networkUris']:
            try:
                # Read all vlan records
                result = db.vlan.find({'uri': vlan})
            except:
                error = "Failed to read the vlan database resolve network uri"
                return render_template('init/dberror.html', error=error, i = vlan)
            for x in result:
                netName = x['name']
                vlanId = x['vlanId']
                network = netName+'-'+str(vlanId)
                newNets.append(network)


        lig_data = [name,desc,state,newNets,sets]
        lig_list.append(lig_data)

    return render_template('init/show_lig.html', lig_list=lig_list )
