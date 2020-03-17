#!/bin/bash
mkdir ~/.kube
mv ./deployment-setup/build_scripts/kubeconfig ~/.kube/config
 
#decrypt the large secrets
openssl aes-256-cbc -K $encrypted_430356ab93ce_key -iv $encrypted_430356ab93ce_iv -in deployment-setup/build_scripts/kube-secrets.txt.enc -out deployment-setup/build_scripts/kube-secrets.txt -d
 
# run the script to get the secrets as environment variables
source ./deployment-setup/build_scripts/kube-secrets.txt
export $(cut -d= -f1 ./deployment-setup/build_scripts/kube-secrets.txt)
 
 
# Set kubernetes secrets
./kubectl config set clusters.cs4300.k8s.mycourseindex.vpc.certificate-authority-data $CERTIFICATE_AUTHORITY_DATA
./kubectl config set users.cs4300.k8s.mycourseindex.vpc.client-certificate-data "$CLIENT_CERTIFICATE_DATA"
./kubectl config set users.cs4300.k8s.mycourseindex.vpc.client-key-data "$CLIENT_KEY_DATA"
./kubectl config set users.cs4300.k8s.mycourseindex.vpc.password "$KUBE_PASSWORD"
./kubectl config set users.cs4300.k8s.mycourseindex.vpc.net-basic-auth.password "$KUBE_PASSWORD"
 
# set AWS secrets
mkdir ~/.aws
touch ~/.aws/credentials
echo '[default]' >> ~/.aws/credentials
echo "aws_access_key_id = $AWS_KEY">> ~/.aws/credentials
echo "aws_secret_access_key = $AWS_SECRET_KEY" >> ~/.aws/credentials
 
# set AWS region
touch ~/.aws/config
echo '[default]' >> ~/.aws/config
echo "output = json">> ~/.aws/config
echo "region = us-east-1" >> ~/.aws/config

# Set docker username + password and login
echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin
# echo "DOCKER_USER=$DOCKER_USERNAME" >> ~/.bashrc
# echo "DOCKER_PASS=$DOCKER_PASSWORD" >> ~/.bashrc