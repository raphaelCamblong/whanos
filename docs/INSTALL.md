# Install the Whanos Project

1. **Link your `kubectl` to your Kubernetes cluster (AWS, GKE, Digital Ocean):**

   Follow the instructions for linking `kubectl` to your specific Kubernetes cluster.

2. **Run the following command in the terminal at the repository root:**
   
   ```bash
   just start
   ```

- Link your kubectl to ur kubernetes cluster (AWS, GKE, Digital Ocean)

- In a terminal at the repository root run the following command:
    just start
    
Then you would have an output with the jenkins insatance url

Once in jenkins you will have to set up the cloud and your github token
to setup the cloud go to settings->cloud then sellect kubernetes and follow the steps
- 
go to settings->credentials->general->github-token and then modify the password with your token
