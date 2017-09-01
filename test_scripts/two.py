
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

Script reads state change messages from OneView and builds local mongo databases

1. Vlan database
2. Network-set database
3  Internetconnect Group database
----------------------------------------------------------------------------------------------------
'''
import pymongo
from pymongo import MongoClient

client = MongoClient('mongo', 27017)

# Define database
db = client.pov3

# define the collections
vlans = db.vlan
x = {"type":"ethernetnetworkV300",
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
                 "uri":"/rest/ethernet-networks/14be9449-c56c-4412-a2ed-c06180e839db"}
vlans.insert(x)
print 'Record inserted: vlans'
