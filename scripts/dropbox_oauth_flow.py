#!/usr/bin/python
# this file should be used by the developer when a new dropbox access token is required. In zac's config, the access token should be called "dropbox_access_token" and the user id is called "dropbox_user_id"
# remember to update the pinned config line in #zac-dev! 

import dropbox

appkey = raw_input("Enter the api key: ")
appsecret = raw_input("Enter the app secret")

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(appkey,appsecret)
auth_url = flow.start()

print "Go to "+auth_url+ " to allow the app and copy the authorization code."
code = raw_input("Enter the authorization code: ")
access_token, user_id = flow.finish(code)
print "Access token: "+access_token
print "User id: "+user_id # im not sure what this is yet but we should probably save it anyway
