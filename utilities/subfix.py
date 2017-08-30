
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

Flask script that build a list of devices with specific attributes and
creates a list of vxlan interfaces
'''

from jsonrpclib import Server

cvp_user = 'cvpadmin'
cvp_word = 'Grape123'

switch_list = ['10.132.0.180','10.132.0.181','10.132.0.182','10.132.0.183','10.132.0.184','10.132.0.185','10.132.0.186','10.132.0.187','10.132.0.188','10.132.0.189',]

for i in switch_list:
    # Create an empty dictionary and clear it each time through the loop


    # Get the vlan information from the switch and make a list
    url = 'http://%s:%s@%s/command-api' % (cvp_user,cvp_word,i)
    switcher = Server(url)
    try:
        print 'trying........'
        response = switcher.runCmds(1,['configure terminal', 'no interface vxlan 1', 'write'])

    except:
        pass
