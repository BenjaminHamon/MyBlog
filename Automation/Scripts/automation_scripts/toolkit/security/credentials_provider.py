import abc

from automation_scripts.toolkit.security.credentials import Credentials


class CredentialsProvider(abc.ABC):

    @abc.abstractmethod
    def get_credentials(self, identifier: str) -> Credentials:
        pass
