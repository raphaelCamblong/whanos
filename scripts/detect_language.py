import os
import json
import typer


def get_all_files(root_dir: str):
    if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
        raise ValueError(f"The specified path '{root_dir}' is not a valid directory.")

    return [file for _, _, files in os.walk(root_dir) for file in files]


def compute_prob(detection_lists: list, files: list) -> int:
    return sum(
        1
        for detection in detection_lists
        for file in files
        if detection.get("type") == "file_existence"
        and file == detection.get("filename")
    )


def detect_language(config, files: list) -> str:
    detection_config = config["languages"]
    language_score = {
        config["name"]: compute_prob(config["detection"], files)
        for config in detection_config
    }
    return max(language_score, key=language_score.get, default="unknown")


DEFAULT_CONFIG = "./language_detection_rules.json"


def detect_main(context: str, config_path=typer.Argument(default=DEFAULT_CONFIG)):
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
        language = detect_language(config, get_all_files(context))
        print(f"{language.lower()}")
        return language if language else "undefined"


if __name__ == "__main__":
    typer.run(detect_main)
