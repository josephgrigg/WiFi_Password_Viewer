"""
This must be run under SYSTEM context. To do so:
1) Download psexec.exe
2) Run command prompt as administrator and change directory to the location of psexec.exe
3) Run the following command:
	psexec.exe -i -s -d cmd.exe
	This will open a new command prompt for you to use. If you type 'whoami',
	it should say 'nt authority\system'
4) Now you are ready to run this python script from the command prompt.

These steps are necessary in order to correctly decrypt the stored wifi
passwords since they were originally encrypted under System context.
"""

import os, pickle
import xml.etree.ElementTree as elementTree
from windows_cryptography import decrypt_password as decrypt
# from binascii import unhexlify
# import binascii


networks = dict()
folder = os.getenv("PROGRAMDATA") + '\Microsoft\Wlansvc\Profiles\Interfaces'

for dirpath, dirnames, filenames in os.walk(folder):
	for file in filenames:

		# Parse the XML file
		tree = elementTree.parse(dirpath + '\\' + file)
		root = tree.getroot()
		namespace = root.tag.split('}')[0] + '}'

		# Find the network name.
		network_name = root.find(namespace + 'name').text
		# Find the encrypted password. Passwords are encrypted using Microsoft's DPAPI.
		encrypted_password = b''
		keyType = ''
		for node in root.iter(namespace + 'keyMaterial'):
			encrypted_password = node.text
		for node in root.iter(namespace + 'keyType'):
			keyType = node.text
		if (keyType == 'passPhrase'):
			pwd = decrypt(encrypted_password).decode('UTF-8', errors='ignore')
		# elif (keyType == 'networkKey'):
			# pwd = binascii.b2a_hex(decrypt(encrypted_password)).decode('UTF-8', errors='ignore')
			# pwd = decrypt(encrypted_password)
			#pwd = unhexlify(decrypt(encrypted_password))
		else:
			pwd = ''
		networks[network_name] = pwd



# Write networks and passwords to a text file.
with open('Output.txt', 'w') as output:
	for network in networks.keys():
		output.write("network: %s \n\t password: %s \n" % (network, networks[network]))
output.close()

with open('pickle-example.p', 'wb') as pfile:
	pickle.dump(networks, pfile)
