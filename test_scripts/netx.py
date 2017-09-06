# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from pprint import pprint

from hpOneView.oneview_client import OneViewClient

config = {
    "ip": '10.1.9.175',
    "credentials": {
        "userName": "administrator",
        "password": "Welcome2hp!"
    }
}

oneview_client = OneViewClient(config)

# Get all, with defaults
ethernet_nets = oneview_client.ethernet_networks.get_all()
for net in ethernet_nets:
    print(net)

print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


sets = oneview_client.network_sets.get_all()
for setz in sets:
    print (setz)
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

ligz = oneview_client.logical_interconnect_groups.get_all()
for lig in ligz:
    print (lig)
