#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import armor_auth
import requests

#######################################
##### Global Variables ################
#######################################

DEBUG       = None
# DEBUG       = True
account_id  = 4464

#######################################
### Main Function #####################
#######################################

def main():
    baseurl, token   = armor_auth.main()

    headers = {
        "Accept": "application/json",
        "Authorization": "FH-AUTH " + token,
        "X-Account-Context": str(account_id)
    }

    vms     = get_vm_list(baseurl, headers)

    print vms


#######################################
### Program Specific Functions ########
#######################################

def get_vm_list(baseurl, headers):
    URL = baseurl + '/vms'
    out = requests.get(URL, headers=headers)

    print out.json()
    return out.json()

#######################################
##### Execution #######################
#######################################

if __name__ == "__main__":
    main()
