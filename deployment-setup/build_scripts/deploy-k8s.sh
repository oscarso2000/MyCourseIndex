GREEN='\033[0;32m'
NC='\033[0;0m'
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"
CLEAR="\033[0K"

# Check out our ip address
# curl ifconfig.me
# echo ''

export PATH=$PATH:$(pwd)

# echo "nameserver 34.230.68.125" | sudo tee -a /etc/resolv.conf
export branch="$TRAVIS_BRANCH" #$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')

echo -e "${YELLOW}==== TESTING NAMESERVER RESOLUTION ====${NC}"
dummyempty=$(dig +short api.cs4300.k8s.mycourseindex.com)
failure=true
if [ -z "$dummyempty" ];
then
    echo -e "${RED}====             FAILURE             ====${NC}"
elif [ "$dummyempty" = ";; connection timed out; no servers could be reached" ];
then
    echo -e "${RED}====             FAILURE             ====${NC}"
else
    failure=false
    echo -e "${GREEN}====             SUCCESS             ====${NC}"
fi
echo -e "${YELLOW}==== DONE TESTING NAMESERVER RESOLUTION ====${NC}"

echo -e "${YELLOW}==== TESTING KUBECTL CONNECTION ====${NC}"

dummybool=$(kubectl get nodes | grep NAME)
failure=true

if [ "$dummybool" = "NAME                             STATUS   ROLES    AGE   VERSION" ]; then
    failure=false
    echo -e "${GREEN}====             SUCCESS             ====${NC}"
else
    echo -e "${RED}====             FAILURE             ====${NC}"
    kubectl get nodes
fi

echo -e "${YELLOW}==== DONE TESTING KUBECTL CONNECTION ====${NC}"

# if [ "$failure" = true ]; then
#     exit 1
# fi

# echo -e "${GREEN}==== Deploying RBAC role ====${NC}"
# cd deployment-setup/rbac/
# for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do kubectl apply -f $f; done
# echo -e "${GREEN}==== Done deploying RBAC role ====${NC}"
# echo ''

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
if [ "$branch" == "master" ]
then
    echo -e "${GREEN}==== Updating deployment to VER: $TRAVIS_BUILD_NUMBER ====${NC}"
    sed -i 's|oscarso2000/cs4300piazza:|oscarso2000/cs4300piazza:'$TRAVIS_BUILD_NUMBER'|g' deployment.yaml
    echo -e "${GREEN}==== Updated deployment to VER: $TRAVIS_BUILD_NUMBER ====${NC}"

    echo -e "${GREEN}==== Deploying Updated Application ====${NC}"
    kubectl apply -f deployment.yaml
    echo -e "${GREEN}==== Done deploying external dns ====${NC}"
    echo ''

    echo -e "${GREEN}==== Updating docs to VER: $TRAVIS_BUILD_NUMBER ====${NC}"
    sed -i 's|oscarso2000/cs4300docs:|oscarso2000/cs4300docs:'$TRAVIS_BUILD_NUMBER'|g' docs/doc_deployment.yaml
    echo -e "${GREEN}==== Updated docs to VER: $TRAVIS_BUILD_NUMBER ====${NC}"

    echo -e "${GREEN}==== Deploying Docs ====${NC}"
    kubectl apply -f docs/doc_deployment.yaml
    echo -e "${GREEN}==== Done Docs ====${NC}"
    echo ''
elif [ "$branch" == "dev" ]
then
    echo -e "${GREEN}==== Updating deployment to VER: $TRAVIS_BUILD_NUMBER ====${NC}"
    sed -i 's|oscarso2000/mciDev:|oscarso2000/mciDev:'$TRAVIS_BUILD_NUMBER'|g' deployment.dev.yaml
    echo -e "${GREEN}==== Updated deployment to VER: $TRAVIS_BUILD_NUMBER ====${NC}"

    echo -e "${GREEN}==== Deploying Updated Application ====${NC}"
    kubectl apply -f deployment.dev.yaml
    echo -e "${GREEN}==== Done deploying external dns ====${NC}"
    echo ''
else
    echo 'Nothing deployed.'
fi

echo 'Successfully deployed'
