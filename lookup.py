#!/usr/bin/python


#!/usr/bin/env python

#################################################################################################
#
#  lookup.py -- Look up subscription ID from email address or user name
#
USAGE = """
Usage: python lookup.py -e User's email address -l User's login ID -n User's name -u Username -p Password
"""
#################################################################################################

import sys, os, getopt, json
import httplib, urllib, urllib2
from base64 import b64encode
import cookielib, Cookie, os
import csv

#################################################################################################
errout = sys.stderr.write
#################################################################################################

def main(argv):

	opts, args = getopt.getopt(argv,"e:l:n:u:p:")

	my_username = ''
	my_password = ''
	query = ''

	for opt, arg in opts:
		if opt == '-e':
			query = '(EmailAddress CONTAINS "%s")' % arg

		elif opt == '-l':
			query = '(UserName CONTAINS "%s")' % arg

		elif opt == '-n':
			query = '(((FirstName CONTAINS "%s") OR (LastName CONTAINS "%s")) OR (DisplayName CONTAINS "%s"))' % arg

		elif opt == '-u':
			my_username = arg

		elif opt == '-p':
			my_password = arg

	rally_host = "rally1.rallydev.com"
	authentication_endpoint = "slm/webservice/v2.0/security/authorize"
	authentication_url="https://%s/%s" % (rally_host, authentication_endpoint)

	# Construct API URL
	api_endpoint = "slm/webservice/v2.0/user?query=%s&fetch=SubscriptionID,DisplayName,FirstName,LastName,UserName,EmailAddress" % (urllib.quote(query))
	rally_url = "https://%s/%s" % (rally_host, api_endpoint)

	# Cookie Manager
	cookiejar = cookielib.CookieJar()
	url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar),urllib2.HTTPHandler())
	authentication_request = urllib2.Request(authentication_url)

	# Base64-encode credentials and set headers
	userAndPass = b64encode("%s:%s" % (my_username,my_password)).decode("ascii")
	authentication_headers = { 'Authorization' : 'Basic %s' %  userAndPass }
	pData = None

	# Authenticate vs. WSAPI2 auth endpoint
	authenticationHttpReq = urllib2.Request(authentication_url, pData, authentication_headers)
	authenticate_response = url_opener.open(authenticationHttpReq)

	# Now go get the user data
	api_headers = { 'Accept' : 'application/json' }
	apiHttpReq = urllib2.Request(rally_url, pData, api_headers)
	api_response = url_opener.open(apiHttpReq)
	api_content = json.loads(api_response.read())

    # Parse the returned collection
	print api_content['QueryResult']['Results'][0]['SubscriptionID']

if __name__ == '__main__':
    main(sys.argv[1:])

