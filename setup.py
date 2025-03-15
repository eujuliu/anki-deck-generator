from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="anki-deck-generator",
    version="0.1.0",
    license="GPL-2.0",
    author="Julio Martins",
    author_email="contact.juliomartins@gmail.com",
    description="This tool allows users to create Anki cards with words, meanings, examples, and IPA pronunciations, and convert text to speech for audio files.",
    packages=find_packages(),
    install_requires=read_requirements(),
    include_package_data=True,
    package_data={"": [".env"]},
    entry_points={
        "console_scripts": [
            "anki_deck=anki_deck_generator.__main__:main",
        ],
    },
)
