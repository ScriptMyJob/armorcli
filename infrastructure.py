#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import os
import requests
import json

#######################################
##### Global Variables ################
#######################################

DEBUG   = os.environ.get('Debug', None)

#######################################
### Program Specific Functions ########
#######################################

def get_vm_list(baseurl, headers):
    URL = baseurl + '/vms'
    out = requests.get(URL, headers=headers)

    if DEBUG:
        print(
            json.dumps(
                out.json(),
                indent=4,
                sort_keys=True
            )
        )

    return out.json()

def get_app_list(baseurl, headers):
    URL = baseurl + '/apps'
    out = requests.get(URL, headers=headers)

    if DEBUG:
        print(
            json.dumps(
                out.json(),
                indent=4,
                sort_keys=True
            )
        )

    return out.json()

