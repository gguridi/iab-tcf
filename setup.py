import os
import subprocess
import logging
import re
from time import time
from typing import List
from setuptools import setup, find_packages
from pathlib import Path


release_file = "RELEASE-VERSION"
requirements_file = "requirements.txt"


logging.basicConfig(format="%(asctime)-15s %(clientip)s %(user)-8s %(message)s")
logger = logging.getLogger(__name__)


def get_version_from_envvar() -> str:
    return os.getenv("RELEASE_VERSION")


def get_version_from_file() -> str:
    try:
        return Path(release_file).read_text().strip()
    except Exception:
        logger.exception(f"Unable to load {release_file} file with static version")


def get_version_from_git() -> str:
    try:
        version = subprocess.check_output(["git", "describe", "--dirty"])
        git_version = version.strip().decode()
        return re.sub(r"-.*$", "-dev" + str(int(time())), git_version)
    except Exception as e:
        logger.exception(f"Unable to load version from git {e}")


def write_version_to_file(version: str):
    Path(release_file).write_text(version)


def get_version() -> str:
    envvar_version = get_version_from_envvar()
    file_version = get_version_from_file()
    git_version = get_version_from_git()
    if not envvar_version and not file_version and not git_version:
        raise Exception("Unable to get the package version.")
    if envvar_version and envvar_version != file_version:
        write_version_to_file(envvar_version)
        return envvar_version
    if git_version and git_version != file_version:
        write_version_to_file(git_version)
        return git_version
    return file_version


def get_requirements() -> List[str]:
    return Path(requirements_file).read_text().strip().splitlines()


setup(
    name="iab-tcf",
    description="A Python implementation of the IAB consent strings (v1.1 and v2)",
    author="Gorka Guridi",
    url="https://github.com/gguridi/iab-tcf",
    author_email="gorka.guridi@gmail.com",
    version=get_version(),
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
