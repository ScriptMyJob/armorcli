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
    out = get_request(baseurl, '/vms', headers)
    return out


def get_app_list(baseurl, headers):
    out = get_request(baseurl, '/apps', headers)
    return out


def get_request(base, uri, headers):
    URL = base + uri
    out = requests.get(URL, headers=headers)

    if DEBUG:
        print(type(out))
        print(
            json.dumps(
                out.json(),
                indent=4,
                sort_keys=True
            )
        )

    return out.json()
