# Justfile whanos manager
set dotenv-load := true

# ╭────────────────────────╮
# │     Docker Images      │
# ╰────────────────────────╯

# Build and push a docker image from the images/ folder
docker-build-and-push-image image:
    python3 scripts/smart_build.py build-base-image {{image}} ./images

# Build and push all the images
docker-build-and-push-all-basse-images:
    just docker-build-and-push-image befunge
    just docker-build-and-push-image c
    just docker-build-and-push-image java
    just docker-build-and-push-image javascript
    just docker-build-and-push-image python

# ╭─────────────────────────╮
# │     Docker Jenkins      │
# ╰─────────────────────────╯

# Run the docker jenkins image
docker-build-jenkins:
    docker build -t whanos-jenkins:latest -f jenkins/Dockerfile .

# Run the docker jenkins image
docker-run-jenkins-dev:
    docker run -d \
      --name whanos-jenkins \
      -p 8080:8080 \
      -e GITHUB_TOKEN=${GITHUB_TOKEN} \
      -e ADMIN_PASSWORD=${ADMIN_PASSWORD} \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v ./jenkins/jobs/:/var/jenkins_home/resource/jobs/ \
      whanos-jenkins:latest

# Publish the docker jenkins image to the registry
docker-publish-jenkins:
    docker tag whanos-jenkins:latest velocipastor/whanos-jenkins:latest
    docker push velocipastor/whanos-jenkins:latest

# ╭────────────────────────────╮
# │     Helm / Kubernetes      │
# ╰────────────────────────────╯

# Set k8s secret for whanos
create-secrets:
    kubectl create secret docker-registry docker-credentials \
    --docker-username=${DOCKER_ACCOUNT_USERNAME} \
    --docker-password=${DOCKER_ACCOUNT_TOKEN} \
    --namespace default

# Delete secret k8s
delete-secrets:
    kubectl delete secret docker-credentials --namespace default

# Deploy using helm and kubectl
helm-deploy-jenkins:
    #!/bin/bash
    kubectl config current-context
    helm install \
      whanos-chart \
      ./helm/jenkins \
      -f ./helm/jenkins/values.yaml \
      --set env.secret.ADMIN_PASSWORD=${ADMIN_PASSWORD} \
      --set env.secret.GITHUB_TOKEN=${GITHUB_TOKEN}

    kubectl get deployments

# Get running Jenkins instance URL
get-jenkins:
    @kubectl get service/whanos-jenkins-service
    @kubectl get service/whanos-jenkins-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}:{.spec.ports[?(@.name=="http")].port}'


# Update the deployed helm chart using helm and kubectl
helm-update-jenkins:
    helm upgrade whanos-chart helm/jenkins

# Shutdown the deployed helm chart using helm and kubectl
helm-teardown-jenkins:
    helm uninstall whanos-chart


# ╭───────────────────╮
# │     Justfile      │
# ╰───────────────────╯

start:
    just create-secrets
    just helm-deploy-jenkins
    just get-jenkins

stop:
    just helm-teardown-jenkins
    just delete-secrets

# Default recipe to display help information
default:
  @just --list
