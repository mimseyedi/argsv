from setuptools import (
    setup,
    find_packages,
)
from pathlib import Path


ROOT_PATH = Path(__file__).parent
META_PATH = Path(ROOT_PATH, 'src', 'argsv', '_meta.py')

exec(open(META_PATH).read())
README = Path(ROOT_PATH, "README.md").read_text()


setup(
    name=__pkg_name__,
    version=__version__,
    description=__description__,
    long_description=README,
    long_description_content_type="text/markdown",

    author=__author__,
    author_email=__email__,

    url=__url__,

    keywords=__keywords__,
    license=__license__,

    packages=find_packages(where="src"),
    package_dir={"": "src"},

    python_requires=__python_v__,

    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
)