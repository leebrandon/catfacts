import sys
import os
import requests
import configargparse
import requests
import json
import twilio
import twilio.rest
from twilio.rest import TwilioRestClient

# ====================================================


def setup():
    p = configargparse.ArgParser(default_config_files=['settings.txt'])
    p.add('--CAT_FACTS_API_URL', required=True, env_var='CAT_FACTS_API_URL')
    p.add('--ACCOUNT_SID', required=True)
    p.add('--AUTH_TOKEN', required=True)
    p.add('--CAT_LEVEL', required=False)
    p.add('--TO_NUMBER', required=False)
    p.add('--FROM_NUMBER', required=False)
    options = p.parse_args()
    return options

# ====================================================


def get_catfacts_right_meow(url):
    r = requests.get(url, verify=False)
    if(r.status_code != 200):
        print 'Error: %s' % url
        return 'NONE'

    try:
        jsonResponse = json.loads(r.content)
    except:
        print 'Unable to decode json'
        sys.exit(1)

    return jsonResponse.get('facts', 'NONE')

# ====================================================


def send_catfacts_right_meow(sid, auth_token, to_number, from_number, message):
    client = TwilioRestClient(sid, auth_token)

    try:
        message = client.messages.create(
            body='Cat Facts: %s' % message,
            to=to_number,
            from_=from_number)
    except twilio.TwilioRestException as e:
        print e
        sys.exit(1)

    return message.sid

# ====================================================

if __name__ == "__main__":
    options = setup()
    catfact = get_catfacts_right_meow(options.CAT_FACTS_API_URL)[0]     # Only take the first one

    if catfact is 'NONE':
        print 'Unable to get cat facts'
        sys.exit(1)

    sid = send_catfacts_right_meow(options.ACCOUNT_SID, options.AUTH_TOKEN, options.TO_NUMBER, options.FROM_NUMBER, catfact)
    print 'Your message has been sent (SID: %s)' % sid
