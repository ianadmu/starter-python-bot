#!/usr/bin/python
#This script will make an api call with the given acces token to check if it is valid

import dropbox

access_token = raw_input("Enter the access token: ")
client = dropbox.client.DropboxClient(access_token)

print "requesting account info..."
print client.account_info()