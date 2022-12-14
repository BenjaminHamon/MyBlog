# MyBlog


## Overview

MyBlog is a personal website for Benjamin Hamon, hosted at blog.benjaminhamon.com.

The project is open source software. See [About](about.md) for more information.


## Development

To set up a workspace for development, run the `setup.py` script with a python3 interpreter.

```
python3 ./Automation/Setup/setup.py
```

Activate the virtual environment, then run the website:

```
.venv/Scripts/activate
python ./development/website.py --address localhost --port 5000

# OR

.venv/Scripts/python -m automation_scripts.run_command --address localhost --port 5000
```
