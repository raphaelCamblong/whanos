import typer
from detect_language import detect_main
from smart_build import build_from_context
from smart_deploy import deploy_app


def detect(context: str, config_path: str) -> str:
    print("Detecting language...")
    return detect_main(context, config_path)


def build(context: str, language: str, build_number: str, resource_images_path: str):
    print("Building...")
    build_from_context(context, language, build_number, resource_images_path)


def deploy(
    context: str,
    deployment_name: str,
    language: str,
    build_number: str,
    resource_helm_path: str,
):
    print("Deploying on cluster...")
    deploy_app(context, deployment_name, language, build_number, resource_helm_path)


def main(
    context: str,
    build_number: str,
    config_path: str,
    resource_image_path: str,
    resource_helm_path: str,
):
    language = detect(
        context,
        config_path,
    )
    if language == "undefined":
        print("language not supported")
        return
    print(f"-->Language detected {language}")
    build(
        context,
        language,
        build_number,
        resource_image_path,
    )
    deploy(
        context,
        f"deployment-whanos-{build_number}",
        language,
        build_number,
        resource_helm_path,
    )


if __name__ == "__main__":
    typer.run(main)
