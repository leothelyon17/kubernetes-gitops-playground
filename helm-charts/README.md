# Slurp'it

### k8s helm chart (slurpit folder is helm chart for kubernetes)

create namespace for deployment

```
kubectl create ns slurpit-ns
```

helm show values slurpit/ > custom-values.yaml

edit custom-values.yaml file according to your environment i.e. timezone and site domain where ingress accept connections
```
global:
  imageRegistry: ""
  imagePullSecrets: []

  persistence:
    enabled: true
    storageClass: "longhorn" # <- use your default storageclass name here

...
portal:
  enabled: true
...
...
  env:
    - name: TZ
      value: "Europe/Amsterdam"
    - name: PORTAL_BASE_URL
      value: "http://slurpit.gtc.local"
...
```

deploy
```
$ helm install my-slurpit slurpit/ --namespace slurpit-ns -f custom-values.yaml
```

update release
```
$ helm upgrade --install my-slurpit slurpit/ --namespace slurpit-ns -f custom-values.yaml
```

uninstall release
```
$ helm uninstall my-slurpit --namespace slurpit-ns
```

helm charts could be compressed as slurpit-0.1.0.tgz archive and pushed to repository (chart musuem or nexus or any other supported)
```
$ helm repo add slurpit-charts https://<helmchart repositoty link>
$ helm repo list
```

helm chart could be used as tgz archive also. in that case, download helm chart using following command

```
$ helm pull <chart-name>
```

above command will look like
```
$ helm upgrade --install my-slurpit slurpit-0.1.0.tgz --namespace slurpit-ns -f custom-values.yaml
```
