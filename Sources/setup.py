import setuptools

from automation_scripts.helpers import automation_helpers


def run_setup() -> None:
    resource_patterns = [
        'static/**/*.css',
        'templates/**/*.html',
    ]

    parameters = {
        "name": "bhamon-blog",
        "packages": setuptools.find_packages(include = [ "bhamon_blog", "bhamon_blog.*" ]),
        "python_requires": "~= 3.7",

        "install_requires": [
            "Flask ~= 2.2.2",
            "python-dateutil ~= 2.8.2",
            "PyYAML ~= 6.0",
        ],

        "package_data": {
            "bhamon_blog": automation_helpers.list_package_data("bhamon_blog", resource_patterns),
        },
    }

    setuptools.setup(**parameters)


run_setup()
