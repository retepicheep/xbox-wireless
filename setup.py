from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = "A python module for using a bluetooth xbox controller from a mac."
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text()
AUTHOR = "Peter Dillow"
AUTHOR_EMAIL = "peter.dillow@proton.me"
GITHUB_URL = "https://github.com/retepicheep/xbox_input_finder/"
PROJECT_URLS = {"Source Code": GITHUB_URL}
INSTALL_REQUIRES = [
    "hidapi",
]
EXTRAS_REQUIRE = {
    "dev": [
        "black",
        "flake8",
        "pre-commit",
        "pydocstyle",
        "pytest",
        "pytest-black",
        "pytest-clarity",
        "pytest-flake8",
        "tox",
    ]
}

with open("xbox_wireless/version.py") as v:
    exec(v.read())

setup(
    name="xbox-wireless",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version=__version__,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="MIT",
    url=GITHUB_URL,
    project_urls=PROJECT_URLS,
    packages=find_packages(
        include=[
            "xbox_wireless",
        ],
    ),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
