# 🐾 Pet Data Streaming with Kafka on Kubernetes 🚀

## 📖 Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
- [Cleanup](#cleanup)
- [Contributing](#contributing)
- [License](#license)

## 🎉 Introduction

Welcome to the Pet Data Streaming project! This application fetches pet data every 60 seconds, streams it through a Kafka cluster, and outputs the data to stdout. All components run on a Kubernetes cluster, providing a scalable and robust solution.

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:
- Docker 🐳
- Kubernetes cluster (Minikube, Docker Desktop, or cloud-based solution) ☸️
- kubectl CLI tool 🖥️
- Python 3.9+ 🐍

## 📂 Project Structure

```
.
├── producer/
│   ├── main.py
│   └── requirements.txt
├── consumer/
│   ├── main.py
│   └── requirements.txt
├── k8s/
│   ├── deployment.yaml
│   ├── kafka-statefulset.yaml
│   ├── zookeeper-statefulset.yaml
│   ├── service.yaml
│   └── zookeeper-service.yaml
├── Dockerfile
└── README.md
```

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/pet-data-streaming.git
   cd pet-data-streaming
   ```

2. **Build the Docker images:**
   ```
   docker build -t pet-data-producer:latest -f Dockerfile .
   docker build -t pet-data-consumer:latest -f Dockerfile .
   ```

3. **Push the images to your container registry:**
   ```
   docker tag pet-data-producer:latest your-registry/pet-data-producer:latest
   docker tag pet-data-consumer:latest your-registry/pet-data-consumer:latest
   docker push your-registry/pet-data-producer:latest
   docker push your-registry/pet-data-consumer:latest
   ```

4. **Update the Kubernetes manifests:**
   Edit `k8s/deployment.yaml` to use your image names.

## 🏃‍♀️ Running the Application

1. **Deploy Zookeeper:**
   ```
   kubectl apply -f k8s/zookeeper-service.yaml
   kubectl apply -f k8s/zookeeper-statefulset.yaml
   ```

2. **Deploy Kafka:**
   ```
   kubectl apply -f k8s/service.yaml
   kubectl apply -f k8s/kafka-statefulset.yaml
   ```

3. **Deploy the producer and consumer:**
   ```
   kubectl apply -f k8s/deployment.yaml
   ```

## 🔍 Monitoring and Troubleshooting

- **Check pod status:**
  ```
  kubectl get pods
  ```

- **View logs:**
  ```
  kubectl logs -f deployment/pets-producer
  kubectl logs -f deployment/pets-consumer
  ```

- **Describe resources:**
  ```
  kubectl describe statefulset kafka
  kubectl describe statefulset zookeeper
  ```

## 🧹 Cleanup

To remove all resources created by this project:

```
kubectl delete -f k8s/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy streaming! 🎉🐶🐱
