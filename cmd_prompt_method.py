"""
This script parses the output of the command prompt function
"netsh wlan show profile" in order to retrieve all of the network names and
passwords.
"""
import subprocess


def get_networks_and_pwds():
	# Get all of the network names/SSIDs.
	command_output = subprocess.run("netsh wlan show profile key=clear",
					stdout=subprocess.PIPE).stdout
	command_output = command_output.split(b'\r\n')

	networks = []
	result = []
	for row in command_output:
		if b' : ' in row:
			networks.append(str(row.split(b' : ')[1])[2:-1])

	# For each network, get the password.
	for network in networks:
		network_details = subprocess.run(["netsh", "wlan", "show", "profile", network, "key=clear"], stdout=subprocess.PIPE).stdout
		network_details = network_details.split(b'\r\n')
		password = ""
		authentication_method = ""

		for line in network_details:
			if b'Key Content' in line:
				password = str(line.split(b' : ')[1])[2:-1]
			elif b'Authentication' in line:
				authentication_method = str(line.split(b' : ')[1])[2:-1]

		result.append((network, password, authentication_method))

	return result
