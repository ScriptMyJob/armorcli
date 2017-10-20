#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import requests
import creds
import sys, os
from datetime import datetime, timedelta
import json

#######################################
##### Global Variables ################
#######################################

username    = creds.username()
password    = creds.password()
baseurl     = 'https://api.armor.com'
DEBUG       = None
# DEBUG       = True

#######################################
### Main Function #####################
#######################################

def main():
    token_file  = 'token_info.json'
    try:
        token   = check_token_file(token_file)
    except Exception as exc:
        print(exc)
        token   = fetch_token()

    return baseurl, token


#######################################
### Program Specific Functions ########
#######################################

def check_token_file(token_file):
    if os.path.isfile(token_file):
        if DEBUG:
            print('Token file found...')
        with open(token_file) as token_json:
            data    = json.load(token_json)

        datestr = data['expiration'].split(".")[0]
        exptime = datetime.strptime(
            datestr,
            '%Y-%m-%d %H:%M:%S'
        )

        check_token_time(exptime, datestr)
    else:
        raise Exception('Token file not found')

    return data['token']


def check_token_time(exptime, datestr):
    if exptime > datetime.now():
        if DEBUG:
            print("Token still valid until " + datestr)
    else:
        raise Exception['Token has expired']


def fetch_token():
    auth_code   = get_info(
        'Reauthenticating (check your phone)...',
        '/auth/authorize',
        'POST',
        'code',
        {
            "username": username,
            "password": password
        }
    )

    token_json  = get_info(
        'Retrieving Token...',
        '/auth/token',
        'POST',
        None,
        {
            "grant_type": "authorization_code",
            "code": auth_code
        }
    )

    token       = token_json['access_token']
    tlife       = token_json['expires_in']

    print('Fetched token: ' + token)

    exptime     = datetime.now() + timedelta(seconds=tlife)

    token_info  = {
        "token": token,
        "expiration": str(exptime)
    }

    file = open("token_info.json", "w")
    file.write(
        json.dumps(
            token_info,
            indent=4,
            sort_keys=True
        ) + "\n"
    )

    return token


def get_info(message, uri, action, parse=None, JSON=None):
    print("\n" + message)

    URL         = baseurl + uri

    if DEBUG:
        print(str(JSON))

    if action   == 'POST':
        out         = requests.post(
            URL,
            data=JSON
        )
    elif action == 'GET':
        out         = requests.get(
            URL,
            data=JSON
        )

    if out.status_code != 200:
        message = "Encountered an issue: " + \
            str(out.status_code) + \
            "\n\n" + out.text

        die(message)

    if parse:
        resp        = out.json()[parse]
        if DEBUG:
            print('Fetched Information (' + parse + '): ' + resp)

    else:
        resp        = out.json()

        if DEBUG:
            print(
                'Fetched JSON Information: ' +
                json.dumps(
                    resp,
                    indent=4,
                    sort_keys=True
                )
            )

    return resp


def die(message, code=1):
    print(message)
    sys.exit(code)


#######################################
##### Execution #######################
#######################################

if __name__ == "__main__":
    main()
