from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.txt").read_text()

setup(
    name='splashscreen_ctk',
    version='0.2.1',
    long_description=long_description,
    long_description_content_type="text/plain"
)
