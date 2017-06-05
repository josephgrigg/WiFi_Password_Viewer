import subprocess

network_names = subprocess.run("netsh wlan show profile key=clear", stdout=subprocess.PIPE).stdout
network_names = network_names.split(b'\r\n')

networks = dict()
for row in network_names:
	if b' : ' in row:
		networks[str(row.split(b' : ')[1])[2:-1]] = ""

for network in networks.keys():
	network_details = subprocess.run(["netsh", "wlan", "show", "profile", network, "key=clear"], stdout=subprocess.PIPE).stdout
	network_details = network_details.split(b'\r\n')
	password = ""
	for line in network_details:
		if b'Key Content' in line:
			password = str(line.split(b' : ')[1])[2:-1]
	networks[network] = password
