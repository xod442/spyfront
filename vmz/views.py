
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
from utilities import getvminfo

vmz_app = Blueprint('vmz_app', __name__)

@vmz_app.route('/vminit', methods=('GET', 'POST'))
def vminit():
    '''
    Create a Mongo database to store the virtual machines
    '''

    # Create client connector (db is running in a container)
    client = MongoClient('mongo', 27017)

    # Define credentials database
    db = client.pov2

    # define the collections
    vmz = db.machines

    # Get the credentials from the log in screen
    vmip = request.form['vmip']
    vm_user = request.form['vm_user']
    vm_word = request.form['vm_word']

    machines = getvminfo.main(vmip,vm_user,vm_word)

    if 'machines' in db.collection_names:
            return render_template('init/database.html', hint='db.exists')

    else:
        for vm in machines:
            try:
                # Read all vlan records, look for matching uri
                vmz.insert(vm)
            except:
                error = "Failed to write to the MACHINES collection"
                return render_template('init/dberror.html', error=error, i = vm)

        return render_template('init/database.html', hint='System Normal')

@vmz_app.route('/getcreds', methods=('GET', 'POST'))
def getcreds():
    '''
    Create a Mongo database to store the virtual machines
    '''
    return render_template('main/main_vmz.html')

@vmz_app.route('/show_machines', methods=('GET', 'POST'))
def show_machines():
    '''
    # Reports on VMs learned from vCenter
    '''
    client = MongoClient('mongo', 27017)

    # Define credentials database
    db = client.pov2

    # define the collections
    vmz = db.machines

    try:
        # Read all vm records
        machine = vmz.find()

    except:
        error = "Failed to read the MACHINE database"
        return render_template('init/dberror.html', error=error)

    return render_template('init/show_machines.html', machine=machine)
