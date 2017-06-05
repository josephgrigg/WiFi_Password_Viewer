import os
import xml.etree.ElementTree as elementTree
from decrypting import decrypt_password as decrypt

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
		else:
			pwd = ''
		networks[network_name] = pwd
		print(network_name, pwd)
