#!/usr/bin/python

import subprocess
import time

# first start an t1.micro instance
print('start up t1.micro instance and call setup.sh to get the dotfiles.')
subprocess.call(['ec2-run-instances', 
  '--instance-count', '1', 
  '--instance-type', 't1.micro', 
  '--key', 'new-dev-ssh-key', 
  '--group', 'ssh-http-https',
  'ami-d0f89fb9'])

# get info about all running ec2 instances
time.sleep(10)
running_instances = {}
instance_info = subprocess.Popen('ec2-describe-instances', stdout=subprocess.PIPE)
for line in instance_info.stdout:
  tokens = line.split()
  if (tokens[0] == 'INSTANCE' and tokens[3] <> 'terminated') :
    running_instances[tokens[9]] = tokens[3]

# write logoninfo to ssh config
print('\nrewrite .ssh config for all amazon ec2 instances')
from os.path import expanduser
home = expanduser("~")
ssh_config = open( '{home}/.ssh/config'.format(home = home), 'w')
count = 1
last_hostname = ''
for key in sorted(running_instances.iterkeys()):
  last_hostname = 'awshost{}'.format(count)
  ssh_config.write('Host {alias}\n'.format(alias=last_hostname))
  ssh_config.write('\tHostName {name}\n'.format(name=running_instances[key]))
  ssh_config.write('\tStrictHostKeyChecking no\n')
  ssh_config.write('\tUser ubuntu\n')
  ssh_config.write('\tIdentityFile "~/.ssh/vm-dev-as-at.pem"\n\n')
  count = count + 1
ssh_config.close()

# copy setup.sh out to newly launched ec2 instance and execute it to create developer environment
subprocess.call(['scp', 'setup.sh', 'ubuntu@{host}:~'.format(host=last_hostname)])
subprocess.call(['ssh', 'ubuntu@{host}'.format(host=last_hostname), '\'./setup.sh\''])

print('setup new aws t1.micro instance: {}'.format(last_hostname))
