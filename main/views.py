

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

Flask script that reads a mongo database for oneView statechange messages
'''
from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import uuid
import os

main_app = Blueprint('main_app', __name__)


@main_app.route('/index', methods=('GET', 'POST'))
@main_app.route('/', methods=('GET', 'POST'))
def main():
    '''
    display the login screen
    '''
    # Display main menu
    return render_template('main/main.html')

@main_app.route('/main', methods=('GET', 'POST'))
def mainx():
    '''
    display the background main menu
    '''
    # Display main menu
    return render_template('main/mainx.html')

@main_app.route('/help', methods=('GET', 'POST'))
def help():

    return render_template('main/help.html')

@main_app.route('/logout', methods=('GET', 'POST'))
def logout():
    Inventory.objects().delete()
    Vxlan.objects().delete()
    return render_template('main/main.html')
