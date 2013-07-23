#!/bin/bash

RUNNING_HOSTS=
for HOST in `ec2-describe-instances | grep INSTANCE | grep -v terminated | cut -f 2`
do
  RUNNING_HOSTS="${RUNNING_HOSTS} ${HOST}"
done

echo ec2-terminate-instances ${RUNNING_HOSTS}
ec2-terminate-instances ${RUNNING_HOSTS}
