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

DEBUG       = os.environ.get('Debug', None)
token_file  = os.environ.get('TokenFile', 'token_info.json')
account_id  = os.environ.get('AccountId', 4464)

#######################################
### Main Function #####################
#######################################

def main():
    try:
        token   = check_token_file()
    except Exception as exc:
        print(exc)
        token   = fetch_token()

    return account_id, baseurl, token


#######################################
### Program Specific Functions ########
#######################################

def check_token_file():
    if os.path.isfile(token_file):
        if DEBUG:
            print('Token file found...')

        data    = load_json_from_file(token_file)

        datestr = data['expiration'].split(".")[0]
        exptime = datetime.strptime(
            datestr,
            '%Y-%m-%d %H:%M:%S'
        )
        token   = data['token']
        check_token_time(token, exptime, datestr)
    else:
        raise Exception('Token file not found')

    return token


def load_json_from_file(filename):
    with open(filename) as jsonfile:
        jsondata = json.load(jsonfile)
    jsonfile.close()

    return jsondata


def check_token_time(token, exptime, datestr):
    if exptime > datetime.now():
        renew_token(token)
        if DEBUG:
            print("Token still valid until " + datestr)
    else:
        raise Exception('Token has expired')


def renew_token(token):
    URL     = baseurl + '/auth/token/reissue'
    headers = {
            "Accept": "application/json",
            "Authorization": "FH-AUTH " + token,
            "X-Account-Context": str(account_id)
    }
    payload = {
        "token": token
    }

    if DEBUG:
        print("\n" + 'Headers: ' + json.dumps(headers))
        print("\n" + 'Payload: ' + json.dumps(payload))
        print("\n" + 'Renewing Token')

    out = requests.post(URL, data=payload, headers=headers)

    if DEBUG and out.status_code == 200:
        print('Token Renewed')
    elif DEBUG:
        print(str(out.status_code))
        print(json.dumps(out.json()))

    tlife = out.json()['expires_in']

    exptime     = datetime.now() + timedelta(seconds=tlife)

    write_toke_to_file(token, exptime)


def fetch_token():
    auth_code   = get_info(
        'Reauthenticating (check your phone)...',
        '/auth/authorize',
        'code',
        {
            "username": username,
            "password": password
        }
    )

    token_json  = get_info(
        None,
        '/auth/token',
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

    write_toke_to_file(token, exptime)

    return token


def write_toke_to_file(token, exptime):
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

    file.close()


def get_info(message, uri, parse=None, JSON=None):
    URL         = baseurl + uri

    if message:
        print("\n" + message)

    if DEBUG and JSON:
        print(
            json.dumps(
                JSON,
                indent=4,
                sort_keys=True
            )
        )

    out         = requests.post(
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
    print("\n" + message)
    sys.exit(code)


#######################################
##### Execution #######################
#######################################

if __name__ == "__main__":
    main()
