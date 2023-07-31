
Note from messing with freeipa:
```
# Download cacert.p12 from freeipa server
openssl pkcs12 -in cacert.p12 -clcerts -nokeys -out freeipa.crt
# Password is the admin password for freeipa

# Make keytab with:
kinit admin
ipa host-add
ipa service-add HTTP/auth.jackhil.de
ipa-getkeytab -p HTTP/auth.jackhil.de -s klefki.jackhil.de -k ./keycloak.keytab

# Create the namespace
kubectl create ns keycloak

# Import both into kubernetes
kubectl create secret generic keycloak-freeipa-cert --from-file=./freeipa.crt-n keycloak
kubectl create secret generic keycloak-freeipa-keytab --from-file=./keycloak.keytab -n keycloak

# Install
helm install keycloak codecentric/keycloak -f values.yaml -n keycloak
```
