from boto import ec2
import os

# Create connection
conn = ec2.connect_to_region("us-east-1")


# Record all instances
all_instances = conn.get_all_instances()
existing = []

for i in all_instances:
	for j in i.instances:
		existing += j

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
resp = conn.run_instances("ami-0922553b7b0369273", instance_type="t2.micro", key_name="wawu_keyPair", security_groups=["csc326-group1"])
inst = resp.instances[0]

# Poll to check instance state, wait if not running
while inst.update() != "running":
	pass

# Currently running
print "\nInstance: {} is currently running!".format(inst)

# Print local IP Address
local_IP = inst.ip_address
print "\nRunning with local IP: {}".format(local_IP)

# Copy folder to AWS virtual machine
scp_command = "scp -i ../wawu_keyPair -r ~/CSC326-SearchEngine ubuntu@" + inst.ip_address + ":~/"
os.system(scp_command)