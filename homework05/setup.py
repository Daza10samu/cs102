from setuptools import setup

import pyvcs

AUTHOR = "Andrew Khairnasov"
AUTHOR_EMAIL = "andreyhigher@gmail.com"
HOME_PAGE = "https://github.com/Daza10samu/cs102"

setup(
    name="vkapi",
    version=pyvcs.__version__,
    description="The stupid content tracker",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=["vkapi", "research"],
    url=HOME_PAGE,
    license="GPLv3",
    python_requires=">=3.6.0",
)
