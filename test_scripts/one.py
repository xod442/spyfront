#!/usr/bin/env python
'''
 Copyright 2016 wookieware.

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
__copyright__ = "Copyright 2017, wookieware."
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

script prints out different messages from the OneView scmb


'''
import pika, ssl
from optparse import OptionParser
from pika.credentials import ExternalCredentials
import json
import logging
import pprint
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost',27017)

# Define database
db = client.pov2

# define the collections
vlans = db.vlan
netsets = db.netset
ligs = db.lig

r = {u'status': u'OK', u'category': u'ethernet-networks', u'ethernetNetworkType': u'Tagged', u'name': u'dev77', u'created': u'2017-08-28T20:14:47.807Z', u'description': None, u'uri': u'/rest/ethernet-networks/a8e8f284-e8ba-464f-8641-4a5ab161f677', u'state': u'Active', u'vlanId': 77, u'modified': u'2017-08-28T20:14:47.808Z', u'fabricUri': u'/rest/fabrics/a4ab21c2-b121-4801-aacf-746b5576bb1a', u'eTag': u'1ef7e926-4d9a-416e-828d-58231ccae399', u'scopeUris': [], u'purpose': u'General', u'subnetUri': None, u'connectionTemplateUri': u'/rest/connection-templates/76a66aaa-35af-42ca-ad21-c660327357fd', '_id': ObjectId('59a479dfc2f3f376df9cd136'), u'type': u'ethernet-networkV300', u'smartLink': False, u'privateNetwork': False}

x = {
        "type":"ethernetnetworkV300",
         "ethernetNetworkType":"Tagged",
         "vlanId":99,
         "smartLink":False,
         "purpose":"General",
         "privateNetwork":False,
         "fabricUri":"/rest/fabrics/a4ab21c2-b121-4801-aacf-746b5576bb1a",
         "connectionTemplateUri":"/rest/connection-templates/602e4e7a-73a1-4873-80ec-acd61cccbdac",
         "subnetUri":'Null',
         "scopeUris":[],
         "name":"x-22",
         "state":"Active",
         "description":'Null',
         "status":"OK",
         "created":"2017-08-24T20:31:47.547Z",
         "eTag":"ef32609d-1a31-482b-806f-abd2f4ef8422",
         "modified":"2017-08-24T20:31:47.548Z",
         "category":"ethernet-networks",
         "uri":"/rest/ethernet-networks/14be9449-c56c-4412-a2ed-c06180e839db"
    }
# This is what is returned as resource from logical interconnect group

y = {
"type":"logical-interconnect-groupV300",
"enclosureType":"SY12000",
"uplinkSets":
            [
            {
            "networkType":"Ethernet",
            "ethernetNetworkType":"Tagged",
            "lacpTimer":"Short",
            "logicalPortConfigInfos":
            [
            {
                "logicalLocation":
                            {
                            "locationEntries":
                                [
                                {"relativeValue":76,"type":"Port"},
                                {"relativeValue":3,"type":"Bay"},
                                {"relativeValue":1,"type":"Enclosure"}
                                ]
                            },
                            "desiredSpeed":"Auto"
            },
            {
                "logicalLocation":
                            {
                            "locationEntries":
                                [
                                {"relativeValue":76,"type":"Port"},
                                {"relativeValue":1,"type":"Enclosure"},
                                {"relativeValue":6,"type":"Bay"}
                                ]
                            },
                            "desiredSpeed":"Auto"
            }
                                                    ],
            "networkUris":
                [
                "/rest/ethernet-networks/dad6976e-cc10-4b4b-a181-d8a71b1126ff",
                "/rest/ethernet-networks/14be9449-c56c-4412-a2ed-c06180e839db"
                ],
            "reachability":'null',
            "primaryPort":'null',
            "nativeNetworkUri":'null',
            "mode":"Auto",
            "name":"x-22-set-set"
            }
            ],
      "redundancyType":"Redundant",
      "ethernetSettings":
        {
            "type":"EthernetInterconnectSettingsV201",
            "lldpIpv6Address":"",
            "lldpIpv4Address":"",
            "interconnectType":"Ethernet",
            "enableIgmpSnooping":True,
            "igmpIdleTimeoutInterval":260,
            "enableFastMacCacheFailover":True,
            "macRefreshInterval":5,
            "enableNetworkLoopProtection":True,
            "enablePauseFloodProtection":True,
            "enableRichTLV":False,
            "enableTaggedLldp":True,
            "dependentResourceUri":"/rest/logical-interconnect-groups/1f88c930-5403-46a1-a68e-d9648c213e21",
            "name":"name262286835-1503606861335",
            "id":"55881fad-c21f-4841-85d6-53c46ae7a6dd",
            "state":'null',
            "description":'null',
            "status":'null',
            "created":"2017-08-24T20:34:21.335Z",
            "eTag":'null',
            "modified":"2017-08-24T20:34:21.335Z",
            "category":'null',
            "uri":"/rest/logical-interconnect-groups/1f88c930-5403-46a1-a68e-d9648c213e21/ethernetSettings"
        },
      "interconnectBaySet":3,
      "name":"lig-4",
      "state":"Active",
      "description":'null',
      "status":'null'
      "uri":"/rest/logical-interconnect-groups/1f88c930-5403-46a1-a68e-d9648c213e21"}


#print json.dumps(y,sort_keys=True, indent=4)

#vlans.insert(r)
#ligs.insert(y)

lig_data = ligs.find()

for connect in lig_data:
    print ('----------------------------------------')
    print (connect)
    print ('----------------------------------------')
'''

lig_data = ligs.find()
vlan_data = vlans.find()

for record in lig_data:
  print record

for record in vlan_data:
  print record
'''
