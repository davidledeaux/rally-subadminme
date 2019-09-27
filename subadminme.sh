#!/bin/bash

MY_USERNAME="user@company.com"
MY_PASSWORD="top\$3cr3t"
INSTALL_DIR="/Users/mydomainusername/Documents/rally-subadminme-master"
PYTHON="/usr/bin/python"

while getopts e:l:s: option
do
case "${option}" in
    e) EMAIL=${OPTARG};;
    l) USERNAME=${OPTARG};;
    s) SUBSCRIPTION_ID=${OPTARG};;
esac
done

if [ -z "$1" ]; then
    echo "Usage: subadminme.sh [-e | -l | -s]"
    echo "    -e : Search by email address"
    echo "    -l : Search by login ID"
    echo "    -s : Lookup by subscription ID"
    exit
fi

if [ "$EMAIL" ]; then
    SUBSCRIPTION_ID=`${PYTHON} ${INSTALL_DIR}/lookup.py -e ${EMAIL} -u ${MY_USERNAME} -p ${MY_PASSWORD}`
fi

if [ "$USERNAME" ]; then
    SUBSCRIPTION_ID=`${PYTHON} ${INSTALL_DIR}/lookup.py -l ${USERNAME} -u ${MY_USERNAME} -p ${MY_PASSWORD}`
fi

if [ -z "$SUBSCRIPTION_ID" ]; then
    echo "Could not determine subscription ID"
    exit
fi

echo
echo "Subscription Admins for SubID ${SUBSCRIPTION_ID}"
echo "================================================"

${PYTHON} ${INSTALL_DIR}/usage.py -s ${SUBSCRIPTION_ID} -d 1 -u ${MY_USERNAME} -p ${MY_PASSWORD} | \
    awk -F '",' -f ${INSTALL_DIR}/parseUsage.awk | sort

echo
