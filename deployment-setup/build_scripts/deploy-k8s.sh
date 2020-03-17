GREEN='\033[0;32m'
NC='\033[0;0m'
export PATH=$PATH:$(pwd)

echo -e "${GREEN}==== Deploying RBAC role ====${NC}"
cd ../rbac/
for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do kubectl apply -f $f --validate=false; done
echo -e "${GREEN}==== Done deploying RBAC role ====${NC}"
echo ''