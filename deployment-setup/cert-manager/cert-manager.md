# Cert-Manager Deployment for HTTPS (setting up certificates)

The NGINX ingress controller supports TLS termination. We do this using
cert-manager.

To install the cert-manager controller in an RBAC-enabled cluster, we used the
following helm install command:

```bash
# Install the CustomResourceDefinition resources separately
kubectl apply --validate=false -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.13/deploy/manifests/00-crds.yaml

# Label the cert-manager namespace to disable resource validation
kubectl label namespace cert-manager cert-manager.io/disable-validation=true

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install \
  cert-manager \
  --namespace cert-manager \
  --version v0.13.0 \
  --set ingressShim.defaultACMEChallengeType=dns01 \
  --set ingressShim.defaultACMEDNS01ChallengeProvider=route53 \
  --set ingressShim.defaultIssuerName=letsencrypt-prod \
  --set ingressShim.defaultIssuerKind=ClusterIssuer \
  jetstack/cert-manager
```

To delete everything:

```
kubectl delete namespace cert-manager
kubectl get ClusterRole --no-headers=true | awk '/cert-manager-*/{print $1}' | xargs kubectl delete ClusterRole
kubectl get ClusterRoleBinding --no-headers=true | awk '/cert-manager-*/{print $1}' | xargs kubectl delete ClusterRoleBinding
kubectl get Role -n kube-system --no-headers=true | awk '/cert-manager-*/{print $1}' | xargs kubectl delete -n kube-system Role
kubectl get MutatingWebhookConfiguration --no-headers=true | awk '/cert-manager-*/{print $1}' | xargs kubectl delete MutatingWebhookConfiguration
kubectl get ValidatingWebhookConfiguration --no-headers=true | awk '/cert-manager-*/{print $1}' | xargs kubectl delete ValidatingWebhookConfiguration
```