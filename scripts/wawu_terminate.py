from boto import ec2
import os
import sys


# Grab instance ID from command line argument
instance_to_kill = sys.argv[1]

if instance_to_kill == None:
	print "\n\nNo instance ID provided, please run script again with target instance ID."

else:
	# Create connection
	print "\nConnecting to us-east-1..."
	conn = ec2.connect_to_region("us-east-1")
	print "Success!"


	# Record all instances
	all_instances = conn.get_all_instances()
	existing = []

	for i in all_instances:
		for j in i.instances:
			existing.append(j)

	for instance in existing:
		if instance.state == "terminated":
			continue
		elif instance.id == instance_to_kill:
			print "\nFound instance {}, trying to terminate...".format(instance_to_kill)

			# Terminate instance
			instance.terminate()

			# Wait for instance to terminate
			while instance.update() != "terminated":
				pass

			print "Instance terminated!"