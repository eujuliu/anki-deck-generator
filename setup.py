from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="anki-deck-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "anki_deck=anki_deck_generator.__main__:main",
        ],
    },
)
