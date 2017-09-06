from flask import Blueprint, render_template, request, redirect, session, url_for, abort, flash
import os
from werkzeug import secure_filename
import pymongo
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader, Template
from hpOneView.oneview_client import OneViewClient



client = MongoClient('mongo', 27017)
db = client.creds
# define the collections
auth_info = db.keyz.find()
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
print (config)
# Switch to the main database
db = client.pov2

# define the collections
vlans = db.vlan
netsets = db.netset
ligs = db.lig

# Create OneView Client connection
oneview_client = OneViewClient(config)

# Get all, etheret-networks and write to the vlan collection
ethernet_nets = oneview_client.ethernet_networks.get_all()
for net in ethernet_nets:
    print (net)

sets = oneview_client.network_sets.get_all()
for setz in sets:
    print (setz)


ligz = oneview_client.logical_interconnect_groups.get_all()
for lig in ligz:
    print (lig)
