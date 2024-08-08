
<h1 style="color: #4CAF50; font-size: 2.5em; text-align: center;">
    Helm Integration Guide: ⚡️
</h1>

## 1. Install Helm (WSL)
```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```


## 2. Create Pet Breed Chart
```bash
helm create pet-breed
```
> 📌 Creates files describing your K8s application


## 3. Move Existing Manifests
```bash
mv deployment.yaml kafka-statefulset.yaml zookeeper-statefulset.yaml \
   service.yaml zookeeper-service.yaml pet-breed/templates/
```


## 4. Configure Default Values
```bash
nano pet-breed/values.yaml
```
> 🔧 Define defaults for Kafka, ZooKeeper, producer, consumer


## 5. Create Environment-Specific Files
```bash
touch pet-breed/values-{dev,prod}.yaml
```
> 🌍 Customize for dev/prod (e.g., consumer image, replicas)


## 6. Templatize Manifests
Update `pet-breed/templates/*.yaml`:
```yaml
spec:
  replicas: {{ .Values.kafka.replicas }}
```
> 🔄 Use Helm variables for flexibility


## 7. Deploy Chart
```bash
helm install pet-pipeline-dev ./pet-breed -f pet-breed/values-dev.yaml
```
> ✈️ Deploys app to K8s using chart, dev values, under the name 'pet-pipeline-dev'
```