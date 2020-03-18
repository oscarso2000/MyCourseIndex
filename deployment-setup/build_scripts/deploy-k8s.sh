GREEN='\033[0;32m'
NC='\033[0;0m'
export PATH=$PATH:$(pwd)

echo "nameserver 172.31.36.87" | sudo tee -a /etc/resolv.conf

# echo -e "${GREEN}==== Deploying RBAC role ====${NC}"
# cd deployment-setup/rbac/
# for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do kubectl apply -f $f; done
# echo -e "${GREEN}==== Done deploying RBAC role ====${NC}"
# echo ''

docker build -t dummytest -f deployment-setup/dockerfile-kube-deploy
docker run -it dummytest /bin/bash &
export TEMPID=docker ps | grep dummytest | awk '{print $1;}'

echo -e "${GREEN}==== Deploying RBAC role ====${NC}"
cd deployment-setup/rbac/
for f in $(find ./ -name '*.yaml' -or -name '*.yml'); do docker exec -it $TEMPID kubectl apply -f deployment-setup/rbac/$f; done
echo -e "${GREEN}==== Done deploying RBAC role ====${NC}"
echo ''

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
