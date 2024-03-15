FROM jenkins/jenkins:latest

EXPOSE 8080
EXPOSE 50000

USER root

# Install dependencies
RUN apt-get update -qq && \
    apt-get install -qqy apt-transport-https ca-certificates curl gnupg2 software-properties-common

## Install docker CLI
RUN curl https://get.docker.com/ > dockerinstall && \
    chmod 777 dockerinstall && \
    ./dockerinstall

## Install kubectl
RUN apt update && \
      apt install -y curl && \
      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl

## Install helm
RUN curl https://raw.githubusercontent.com/helm/helm/master/scripts/get > get_helm.sh && \
    chmod 700 get_helm.sh && \
    ./get_helm.sh

# Install python and pip
RUN apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Set Jenkins var
ENV CASC_JENKINS_CONFIG /var/jenkins_home/casc.yaml
ENV JENKINS_HOME /var/jenkins_home
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

WORKDIR $JENKINS_HOME

# Install Jenkins plugins
COPY jenkins/plugins.txt plugins.txt
RUN jenkins-plugin-cli --plugin-file plugins.txt

# Get Jenkins config
COPY ./jenkins/jenkins-configuration.yml $JENKINS_HOME/casc.yaml

# Get Jenkins jobs and resource
COPY jenkins/jobs/job_dsl.groovy $JENKINS_HOME/resource/jobs/
COPY jenkins/agent/kaniko_builder.yml $JENKINS_HOME/resource/jobs/
COPY images $JENKINS_HOME/resource/images
COPY scripts $JENKINS_HOME/resource/scripts
COPY helm/app $JENKINS_HOME/resource/helm
ENV JENKINS_RESOURCE $JENKINS_HOME/resource

# Install script dependencies
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV
RUN /opt/venv/bin/pip install -r $JENKINS_HOME/resource/scripts/requirements.txt
