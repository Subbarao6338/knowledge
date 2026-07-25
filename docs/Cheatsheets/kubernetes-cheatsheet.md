---
layout: default
title: "Kubernetes (K8s) Cheatsheet"
---

# Kubernetes (K8s) Cheatsheet

Kubernetes is an open-source container orchestration platform designed to automate application deployment, scaling, and management.

---

## 1. Core Kubectl Commands

```bash
# Cluster Information
kubectl cluster-info                     # Display cluster info
kubectl get nodes                        # List nodes in the cluster
kubectl describe node <node-name>        # Show detailed node information

# Resource Creation & Management
kubectl apply -f manifest.yaml           # Create/update resource(s) from a manifest file
kubectl delete -f manifest.yaml          # Delete resource(s) defined in a manifest
kubectl delete pod <pod-name>            # Delete a specific pod
```

---

## 2. Viewing & Inspecting Resources

```bash
# Get Commands (List resources)
kubectl get pods                         # List all pods in the active namespace
kubectl get pods -A                      # List all pods across all namespaces
kubectl get services                     # List services
kubectl get deployments                  # List deployments
kubectl get namespaces                   # List namespaces

# Output Formatting
kubectl get pods -o wide                 # List pods with more detailed columns (IP, Node)
kubectl get pod <pod-name> -o yaml       # Output the pod definition in YAML format
kubectl get pods --sort-by='.metadata.creationTimestamp' # Sort list by creation date

# Describe (Deep dive)
kubectl describe pod <pod-name>          # Deep inspect pod events and specifications
kubectl describe deployment <deploy-name># Deep inspect deployment
```

---

## 3. Debugging & Troubleshooting

```bash
# Logging
kubectl logs <pod-name>                  # Stream logs from a single-container pod
kubectl logs <pod-name> -c <container>   # Stream logs for a specific container in a pod
kubectl logs -f <pod-name>               # Follow log stream (real-time tail)
kubectl logs --tail=100 <pod-name>       # Print the last 100 lines of logs

# Shell Execution
kubectl exec -it <pod-name> -- /bin/sh   # Open interactive shell inside pod
kubectl exec -it <pod-name> -c <container> -- /bin/bash # Open shell inside multi-container pod

# Networking & Port Forwarding
kubectl port-forward <pod-name> 8080:80  # Forward local port 8080 to pod port 80
kubectl port-forward svc/<service> 8080:80 # Forward local port 8080 to service port 80
```

---

## 4. Standard Manifest Examples

### Pod Manifest (`pod.yaml`)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: frontend-pod
  labels:
    app: frontend
spec:
  containers:
    - name: web-app
      image: nginx:alpine
      ports:
        - containerPort: 80
```

### Deployment Manifest (`deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  labels:
    app: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: web-app
          image: nginx:alpine
          ports:
            - containerPort: 80
          resources:
            requests:
              memory: "64Mi"
              cpu: "250m"
            limits:
              memory: "128Mi"
              cpu: "500m"
```

### Service Manifest (`service.yaml`)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: ClusterIP
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
```

---

## 5. Common Gotchas & Troubleshooting Steps

1. **`CrashLoopBackOff`:** The container starts, crashes, restarts, and crashes again. Check logs immediately with `kubectl logs <pod-name>`. Often caused by incorrect commands, missing environment variables, or application errors.
2. **`ImagePullBackOff`:** Kubernetes is unable to pull the container image. Check image name capitalization, spelling, tag/version, and ensure pull secrets are present if using a private registry.
3. **Namespace Scope:** If you cannot find your resource, you might be in the wrong namespace. Append `-n <namespace>` to check, or use `-A` to see everything.
4. **Service Matching Labels:** A Service forwards traffic to Pods via selector matching. If your Service is not routing traffic, verify that `spec.selector` matches the labels defined on your Pods exactly.

---

## 6. Advanced Kubernetes Features

### ConfigMaps & Secrets
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "jdbc:postgresql://db:5432/prod"
  max_connections: "20"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  db_password: dGhlLXNlY3JldC1wYXNzd29yZA== # base64 encoded
```

### Pod Scheduling & Node Affinity
```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-east-1a
```
