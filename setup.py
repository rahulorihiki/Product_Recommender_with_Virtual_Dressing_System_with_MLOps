import setuptools

# Read the README.md file and store it in long_description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

# Write the name of the repository where the code is stored and the corresponding author name and email
REPO_NAME = "Fashion_Recommender_with_MLOps_EndtoEnd"
AUTHOR_USER_NAME = "rahulorihiki"
SRC_REPO = "myFashionRecommender" # This is the name of the package. It should be the same as the name of the directory where the code is stored i.e. basically it should be same as "project_name" variable in template.py. We can install the pacakge as pip install myFashionRecommender.
AUTHOR_EMAIL = "krahulgovind@gmail.com"

# Setup the package details, giving a basic description to the package
setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for Fashion CNN app",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src") # This mentions where the packages are stored. In our case, it is stored in the "src" directory
)