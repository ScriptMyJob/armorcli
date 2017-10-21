#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import os
import requests
import json

#
# This is imported by armorcli and never executed by itself.
#

#######################################
##### Global Variables ################
#######################################

DEBUG   = os.environ.get('Debug', None)

#######################################
### Program Specific Functions ########
#######################################

def get_armor_contacts(baseurl, headers):
    out = get_request(baseurl, '/account/contacts', headers)
    return out


def get_user_info(baseurl, headers):
    out = get_request(baseurl, '/me', headers)
    return out


def get_associated(baseurl, headers):
    out = get_request(baseurl, '/accounts', headers)
    return out


def get_account_info(baseurl, headers, a_id):
    out = get_request(baseurl, '/accounts', headers, "/" + str(a_id))
    return out


def get_request(base, uri, headers, uri2=None):
    if uri2:
        URL = base + uri + uri2
    else:
        URL = base + uri

    if DEBUG:
        print('Request URL: ' + URL)

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
