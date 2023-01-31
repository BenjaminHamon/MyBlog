import setuptools


def run_setup() -> None:
    parameters = {
        "name": "automation-scripts",
        "packages": setuptools.find_packages(include = [ "automation_scripts", "automation_scripts.*" ]),
        "python_requires": "~= 3.7",

        "install_requires": [
            "Markdown ~= 3.4.1",
            "PyYAML ~= 6.0",
            "requests ~= 2.28.2",
            "twine ~= 4.0.2",
        ],

        "extras_require": {
            "dev": [
                "pylint ~= 2.15.6",
                "pytest ~= 7.2.0",
            ],
        },
    }

    setuptools.setup(**parameters)


run_setup()
