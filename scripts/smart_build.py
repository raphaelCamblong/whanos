import os
import typer
import subprocess
from dataclasses import dataclass

app = typer.Typer()

DOCKER_REGISTRY = "velocipastor/"
BASE_TAG = "base-latest"


def execute(command: str):
    return subprocess.run(command.split(" "))


def custom_dockerfile(dockerfile_path, new_image):
    with open(dockerfile_path, "r") as file:
        lines = file.readlines()
    if lines and lines[0].startswith("FROM "):
        lines[0] = f"FROM {new_image}\n"
    with open(dockerfile_path, "w") as file:
        file.writelines(lines)


@dataclass
class WhanosDockerImage:
    language: str
    tag: str
    id: str = None
    registry_id: str = None

    def __post_init__(self):
        self.id = f"whanos-{self.language}:{self.tag}"
        self.registry_id = f"{DOCKER_REGISTRY}whanos-{self.language}:{self.tag}"

    def push_image(self):
        execute(f"docker tag {self.id} {self.registry_id}")
        execute(f"docker push {self.registry_id}")

    def build_image(self, context: str, dockerfile_path: str):
        execute(f"docker build -f {dockerfile_path} {context} -t {self.id}")

    def build_from_dockerfile(self, context: str, dockerfile_path: str):
        base_image = f"{DOCKER_REGISTRY}whanos-{self.language}:{BASE_TAG}"
        custom_dockerfile(dockerfile_path, base_image)
        self.build_image(context, dockerfile_path)


@app.command()
def build_base_image(language: str, resource_images_path: str):
    image = WhanosDockerImage(language=language, tag=BASE_TAG)
    dockerfile_path = f"{resource_images_path}/{language}/Dockerfile.base"
    image.build_image(context=".", dockerfile_path=dockerfile_path)
    image.push_image()


@app.command()
def build_from_context(
    context: str, language: str, build_number: str, resource_images_path: str
):
    image = WhanosDockerImage(language, build_number)
    print(f"Building image {image.registry_id} at {context}")
    print(f"Resource images located at {resource_images_path}/{language}")

    if os.path.exists(f"{context}/Dockerfile"):
        dockerfile_path = f"{context}/Dockerfile"
        image.build_from_dockerfile(context, dockerfile_path)
        image.push_image()
    else:
        dockerfile_path = f"{resource_images_path}/{language}/Dockerfile.standalone"
        image.build_image(context, dockerfile_path)
        image.push_image()


if __name__ == "__main__":
    app()
