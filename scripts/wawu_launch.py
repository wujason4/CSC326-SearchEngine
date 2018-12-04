from boto import ec2
import os


# Create connection
print "\n\nConnecting to region us-east-1"
conn = ec2.connect_to_region("us-east-1")


# Record all instances
all_instances = conn.get_all_instances()
existing = []

for i in all_instances:
	for j in i.instances:
		existing.append(j)

for instance in existing:
	if instance.state == "terminated":
		continue
	else:
		# Terminate instance
		instance.terminate()

		# Wait for instance to terminate
		while instance.update() != "terminated":
			pass


# Run new instance
print "\nTrying to run new instance..."
resp = conn.run_instances("ami-0922553b7b0369273", instance_type="t2.micro", key_name="wawu_keyPair", security_groups=["csc326-group1"])
inst = resp.instances[0]

# Poll to check instance state, wait if not running
while inst.update() != "running":
	pass

# Currently running
print "\nInstance: {} is currently running!".format(inst)


print "Copying over sourcecode..."
# Copy folder to AWS virtual machine
scp_command = "scp -o StrictHostKeyChecking=no -i ~/CSC326-SearchEngine/key/wawu_keyPair.pem -r ~/CSC326-SearchEngine ubuntu@" + inst.ip_address + ":~/"
os.system(scp_command)

# Install any missing packages
os.system("ssh -o StrictHostKeyChecking=no -i ~/CSC326-SearchEngine/key/wawu_keyPair.pem ubuntu@{} sudo pip install httplib2".format(inst.ip_address))
os.system("ssh -o StrictHostKeyChecking=no -i ~/CSC326-SearchEngine/key/wawu_keyPair.pem ubuntu@{} sudo pip install beaker".format(inst.ip_address))
os.system("ssh -o StrictHostKeyChecking=no -i ~/CSC326-SearchEngine/key/wawu_keyPair.pem ubuntu@{} sudo pip install oauth2client".format(inst.ip_address))
os.system("ssh -o StrictHostKeyChecking=no -i ~/CSC326-SearchEngine/key/wawu_keyPair.pem ubuntu@{} sudo pip install google-api-python-client".format(inst.ip_address))


# Run mybottle.py using screen
screen_command = "screen sudo python ~/CSC326-SearchEngine/mybottle.py"


# Print local IP Address
print "\nRunning with local IP: {}, on instance ID: {}".format(inst.ip_address, inst)

