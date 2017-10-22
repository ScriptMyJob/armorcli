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

def get_tickets(baseurl, headers):
    out = get_request(baseurl, '/tickets', headers)
    return out


def get_ticket_count(baseurl, headers):
    out = get_request(baseurl, '/tickets/count', headers)
    return out


def open_ticket(baseurl, headers, title, first_comment):
    data = {
        "starred": False,
        "type": "ticket",
        "status": "New",
        "title": title,
        "tags": [
            "Created via Armor API"
        ],
        "comments": [
            first_comment
        ],
        "recipients": [],
        "relatedServers": [],
        "relatedTickets": []
    }

    out = post_request(baseurl, '/tickets/create', headers, data)
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


def post_request(base, uri, headers, data=None, uri2=None):
    if uri2:
        URL = base + uri + uri2
    else:
        URL = base + uri

    if DEBUG:
        print('Request URL: ' + URL)

    out = requests.post(URL, headers=headers, data=data)

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
