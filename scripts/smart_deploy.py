from dataclasses import dataclass
import os
import subprocess
import yaml
import typer
import shutil

VALUES_PATH = "./values.yaml"
WHANOS_YML = "whanos.yml"
DOCKER_REGISTRY = "velocipastor/"

app = typer.Typer()


def execute(command: str):
    return subprocess.run(command.split(" "))


def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    return data


@dataclass
class Values:
    _values = None
    filepath: str
    name: str
    image_repository: str
    image_tag: str

    service_type: str = "LoadBalancer"
    deployment_replicas: int = 1

    def __post_init__(self):
        self._values = yaml_loader(self.filepath)
        self._values["name"] = self.name
        self._values["image"]["repository"] = self.image_repository
        self._values["image"]["tag"] = self.image_tag

    def write(self):
        with open(self.filepath, "w") as file_descriptor:
            yaml.dump(self._values, file_descriptor)

    def merge_with_provided_settings(self, settings_filepath):
        if not os.path.exists(settings_filepath):
            print(os.getcwd())
            print(f"no deployments settings found at {settings_filepath}")
            return
        provided_values = yaml_loader(settings_filepath)
        if provided_values.get("deployment"):
            self._values["deployment"] = provided_values["deployment"]


def initialize_deployment(chart_filepath):
    shutil.copy2(f"{chart_filepath}/values.yaml", ".")


def deploy(deployment_name, value_filepath, chart_filepath):
    print(f"helm install {deployment_name} {chart_filepath} -f {value_filepath}")
    execute(f"helm install {deployment_name} {chart_filepath} -f {value_filepath}")


@app.command()
def dry_deploy():
    return


@app.command()
def deploy_app(
    context: str,
    deployment_name: str,
    language: str,
    build_number: str,
    chart_filepath: str = typer.Argument(default="/var/jenkins_home/resources/helm"),
):
    container_image = f"{DOCKER_REGISTRY}whanos-{language}"
    initialize_deployment(chart_filepath)
    values = Values(
        filepath=VALUES_PATH,
        name=deployment_name,
        image_repository=container_image,
        image_tag=build_number,
    )

    values.merge_with_provided_settings(f"{context}/{WHANOS_YML}")
    values.write()
    deploy(deployment_name, values.filepath, chart_filepath)


if __name__ == "__main__":
    app()
