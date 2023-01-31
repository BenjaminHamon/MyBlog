import datetime
import logging
from typing import Any, Optional

import requests


logger = logging.getLogger("WebClient")


class WebClient:


    def __init__(self, authentication: Optional[Any] = None) -> None:
        self._authentication = authentication
        self.timeout = datetime.timedelta(seconds = 30)


    def upload_file(self, url: str, file_path: str) -> None:
        with open(file_path, mode = "rb") as file_to_upload:
            files = { "file": file_to_upload }

            logger.debug("PUT %s", url)
            response = requests.put(url, auth = self._authentication, files = files, timeout = self.timeout.total_seconds())
            response.raise_for_status()
