from datetime import datetime
from pathlib import Path
from typing import List

from src.models.deployment_package import DeploymentPackage


def get_deployment_packages(web_app: str | None):

    deployment_package_path = 'data/deployment/'

    def strptime(s: str):
        try:
            return datetime.strptime(s, '%Y%m%dT%H%M%S')
        except ValueError:
            return None

    deployment_packages: List[DeploymentPackage] = sorted(
        [
            package
            for package in (
                DeploymentPackage(file=path, date=strptime(path.stem.split('_')[-1]))
                for path in Path(deployment_package_path).iterdir()
                if path.suffix == '.zip' and (web_app is None or web_app in path.name)
            )
            if package.date is not None
        ],
        key=lambda p: p.date,
    )

    return deployment_packages
