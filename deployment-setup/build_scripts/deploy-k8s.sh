GREEN='\033[0;32m'
NC='\033[0;0m'
export PATH=$PATH:$(pwd)

echo -e "${GREEN}==== Deploying RBAC role ====${NC}"
cd deployment-setup/rbac/
for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do kubectl apply -f $f; done
echo -e "${GREEN}==== Done deploying RBAC role ====${NC}"
echo ''

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
