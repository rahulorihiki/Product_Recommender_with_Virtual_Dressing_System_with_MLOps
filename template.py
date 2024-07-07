import os
from pathlib import Path
import logging

# It means whenever we use logging.info, it will print the message in the told format only i.e. timestamp and then the  message, and logging has many other levels like debug, warning, error, etc. and each levels are used for different purposes, you can explore them in the official documentation clearly.
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


project_name = "myFashionRecommender"

list_of_files = [
    # The reason for creating .gitkeep file is to make sure that the directory is created in the git repository, because git does not allow to push empty directories, so we need to create a file in the directory to make sure that the directory is created in the git repository.
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html"
]



for filepath in list_of_files:
    # Path(filepath) is used to convert the string into a path object, so that we can use the path object to get the directory name and the file name, and also to check if the file exists or not.
    # Plus we know ".github/workflows/.gitkeep" in windows we use backslash and in linux we use forward slash, so to make it platform independent we use Path(filepath) as it will automatically detect the operating system and convert it into the correct format.
    filepath = Path(filepath)
    # ".github/workflows/.gitkeep" for this example filedir will be ".github/workflows" and filename will be ".gitkeep"
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")