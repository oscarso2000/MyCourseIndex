#!/bin/bash

#script to recursively travel a dir of n levels


function traverse() {

for file in `ls $1`
do
    #current=${1}{$file}
    if [ ! -d ${1}${file} ] ; then
    echo ''
    else

        echo -e "${GREEN}==== Deploying TF in ${1}/${file} ====${NC}"
        cd ${1}${file}

        if ls | grep -q .tf;
        then
            terraform init
            terraform plan
            terraform apply -auto-approve
        fi

         echo -e "${GREEN}==== Done deploying TF in ${1}/${file} ====${NC}"
        ls
        echo "Traversing ${1}/${file} next"
        traverse "${1}/${file}"
    fi
done
}


GREEN='\033[0;32m'
NC='\033[0;0m'
export PATH=$PATH:$(pwd)
export AWS_DEFAULT_REGION="us-east-1"

echo -e "${GREEN}==== Deploying terraform ====${NC}"


cd build-scripts
traverse ../

echo -e "${GREEN}==== Done deploying terraform  ====${NC}"
echo ''