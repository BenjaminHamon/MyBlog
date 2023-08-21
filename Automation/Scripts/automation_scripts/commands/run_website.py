import argparse
import importlib
import logging
import os

from bhamon_development_toolkit.automation.automation_command import AutomationCommand


logger = logging.getLogger("Main")


class RunWebsiteCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("run-website", help = "run the website")
        parser.add_argument("--address", required = True, help = "set the address for the server to listen to")
        parser.add_argument("--port", required = True, type = int, help = "set the port for the server to listen to")
        return parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        address: str = arguments.address
        port: int = arguments.port

        logging.getLogger("werkzeug").setLevel(logging.WARNING)

        title = "Benjamin Hamon's blog"
        content_directory = os.path.abspath("Content")
        application_module = importlib.import_module("benjaminhamon_blog.application_factory")
        application = application_module.create_application(title, content_directory)
        website_link = "http://%s:%s/" % (address, port)

        logger.info("Website available at '%s'", website_link)

        if not simulate:
            application.run(address = address, port = port, debug = True)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Not supported")
