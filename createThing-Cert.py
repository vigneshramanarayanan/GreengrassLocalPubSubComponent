################################################### Connecting to AWS
import boto3
import os
import json
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
thingArn = ''
thingId = ''
thingName_old = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
defaultPolicyName = 'IOT_GreenGrass'
###################################################

def createThing(vehicle):
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = vehicle
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  for element in data: 
   if element == 'thingArn':
        thingArn = data['thingArn']
   elif element == 'thingId':
        thingId = data['thingId']
  createCertificate(vehicle)

def createCertificate(vehicle):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
			setAsActive = True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
	for element in data: 
			if element == 'certificateArn':
					certificateArn = data['certificateArn']
			elif element == 'keyPair':
					PublicKey = data['keyPair']['PublicKey']
					PrivateKey = data['keyPair']['PrivateKey']
			elif element == 'certificatePem':
					certificatePem = data['certificatePem']
			elif element == 'certificateId':
					certificateId = data['certificateId']
							
	path = './Vehicles/' + vehicle
	if not os.path.exists(path):
		os.mkdir(path)
	path = path + '/'
	with open(path + 'public.key', 'w') as outfile:
			outfile.write(PublicKey)
	with open(path + 'private.key', 'w') as outfile:
			outfile.write(PrivateKey)
	with open(path + 'cert.pem', 'w') as outfile:
			outfile.write(certificatePem)

	response = thingClient.attach_policy(
			policyName = defaultPolicyName,
			target = certificateArn
	)
	response = thingClient.attach_thing_principal(
			thingName = vehicle,
			principal = certificateArn
	)

thingClient = boto3.client('iot', region_name='us-east-1')  # Replace 'us-east-1' with your desired region

for i in range(1,501):
	createThing("vehicle"+str(i))
