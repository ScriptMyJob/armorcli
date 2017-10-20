#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import armor_auth
import infrastructure

# import json
import os

#######################################
##### Global Variables ################
#######################################

DEBUG   = os.environ.get('DEBUG', None)

account_id  = 4464
baseurl, token   = armor_auth.main()

headers = {
    "Accept": "application/json",
    "Authorization": "FH-AUTH " + token,
    "X-Account-Context": str(account_id)
}

#######################################
### Main Function #####################
#######################################

def main():
    if DEBUG:
        print('Retrieving VM List')

    out = infrastructure.get_vm_list(baseurl, headers)

    if DEBUG:
        print('Returning output')

    return out


#######################################
### Program Specific Functions ########
#######################################

#######################################
##### Execution #######################
#######################################

if __name__ == "__main__":
    main()
