#!/usr/bin/python

import subprocess
import time

print('start up t1.micro instance and call setup.sh to get the dotfiles.')
subprocess.call(['ec2-run-instances', 
  '--instance-count', '1', 
  '--instance-type', 't1.micro', 
  '--key', 'new-dev-ssh-key', 
  '--group', 'ssh-http-https',
  'ami-d0f89fb9'])

time.sleep(3)
running_instances = {}
instance_info = subprocess.Popen('ec2-describe-instances', stdout=subprocess.PIPE)
for line in instance_info.stdout:
  tokens = line.split()
  if (tokens[0] == 'INSTANCE') :
    running_instances[tokens[9]] = tokens[3]

print('\nrewrite .ssh config for all amazon ec2 instances')
from os.path import expanduser
home = expanduser("~")
ssh_config = open( '{home}/.ssh/config'.format(home = home), 'w')
count = 1
for key in sorted(running_instances.iterkeys()):
  ssh_config.write('Host awshost-{id}\n'.format(id=count))
  ssh_config.write('\tHostName {name}\n'.format(name=running_instances[key]))
  ssh_config.write('\tUser ubuntu\n')
  ssh_config.write('\tIdentityFile "~/.ssh/vm-dev-as-at.pem"\n\n')
  count = count + 1
ssh_config.close()

