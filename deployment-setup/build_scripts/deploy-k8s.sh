GREEN='\033[0;32m'
NC='\033[0;0m'
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"
CLEAR="\033[0K"

# Check out our ip address
curl ifconfig.me
echo ''

export PATH=$PATH:$(pwd)

echo "nameserver 172.31.36.87" | sudo tee -a /etc/resolv.conf

echo -e "${YELLOW}==== TESTING NAMESERVER RESOLUTION ====${NC}"
dummyempty=$(dig api.cs4300.k8s.mycourseindex.vpc)
failure=true
if [ -z "$dummyempty" ];
then
    echo -e "${RED}====             FAILURE             ====${NC}"
else
    failure=false
    echo -e "${GREEN}====             SUCCESS             ====${NC}"
    echo -e "${GREEN}====     NAMESERVER: $dummyempty     ====${NC}"
fi
echo -e "${YELLOW}==== DONE TESTING NAMESERVER RESOLUTION ====${NC}"

echo -e "${YELLOW}==== TESTING KUBECTL CONNECTION ====${NC}"

dummybool=$(kubectl get nodes | grep NAME)
failure=true

if [ "$dummybool" = "NAME STATUS ROLES AGE VERSION" ]; then
    failure=false
    echo -e "${GREEN}====             SUCCESS             ====${NC}"
else
    echo -e "${RED}====             FAILURE             ====${NC}"
fi

echo -e "${YELLOW}==== DONE TESTING KUBECTL CONNECTION ====${NC}"

if [ "$failure" = true ]; then
    exit 1
fi

# echo -e "${GREEN}==== Deploying RBAC role ====${NC}"
# cd deployment-setup/rbac/
# for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do kubectl apply -f $f; done
# echo -e "${GREEN}==== Done deploying RBAC role ====${NC}"
# echo ''

# docker build -t dummytest ./deployment-setup/ \
#     --build-arg KUBE_PASSWORD=$KUBE_PASSWORD \
#     --build-arg AWS_KEY=$AWS_KEY \
#     --build-arg AWS_SECRET_KEY=$AWS_SECRET_KEY \
#     --build-arg DOCKER_USERNAME=$DOCKER_USERNAME \
#     --build-arg DOCKER_PASSWORD=$DOCKER_PASSWORD \
#     --build-arg CERTIFICATE_AUTHORITY_DATA=$CERTIFICATE_AUTHORITY_DATA \
#     --build-arg CLIENT_CERTIFICATE_DATA=$CLIENT_CERTIFICATE_DATA \
#     --build-arg CLIENT_KEY_DATA=$CLIENT_KEY_DATA

# docker run -it dummytest /bin/bash &
# export TEMPID=docker ps | grep dummytest | awk '{print $1;}'

# echo -e "${GREEN}==== Deploying RBAC role ====${NC}"
# cd deployment-setup/rbac/
# for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do docker exec -it $TEMPID kubectl apply -f deployment-setup/rbac/$f; done
# echo -e "${GREEN}==== Done deploying RBAC role ====${NC}"
# echo ''

# docker exec -it $TEMPID kubectl get nodes

# echo -e "${GREEN}==== Deploying iam role ====${NC}"
# cd ../kube2iam/
# for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do kubectl apply -f $f --validate=false; done
# echo -e "${GREEN}==== Done deploying iam role ====${NC}"
# echo ''
# echo -e "${GREEN}==== Deploying external dns ====${NC}"
# cd ../external_dns/
# for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do kubectl apply -f $f --validate=false; done
# echo -e "${GREEN}==== Done deploying external dns ====${NC}"
# echo ''
