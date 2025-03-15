<a name="readme-top"></a>

# 🗃️ Anki Deck Generator

An application to generate Anki decks from a dictionary and text-to-speech data. This tool allows users to create Anki cards with words, meanings, examples, and IPA pronunciations, and convert text to speech for audio files.


<p align="center">
<a href="https://github.com/eujuliu/anki-deck-generator/issues">Have a question?</a>
  ·
  <a href="https://github.com/eujuliu/anki-deck-generator/fork">Request Feature</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12.9-blue" alt="Python Version">
  <img src="https://img.shields.io/github/last-commit/eujuliu/anki-deck-generator" alt="Last Update">
  <img src="https://img.shields.io/github/issues/eujuliu/anki-deck-generator" alt="Issues">
  <img src="https://img.shields.io/github/forks/eujuliu/anki-deck-generator" alt="Forks">
  <img src="https://img.shields.io/github/stars/eujuliu/anki-deck-generator" alt="Stars">
  <img src="https://img.shields.io/github/license/eujuliu/anki-deck-generator" alt="License">
</p>

![Image](https://github.com/user-attachments/assets/b3c17053-a1e8-4551-8e89-3011be4a74c7) ![Image](https://github.com/user-attachments/assets/094d61c3-ef0e-4758-970f-577fbbb673cf)

## Table of Contents
  - [Technologies](#technologies)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
  - [Contributing](#contributing)
  - [Backlog](#backlog)
  - [Motivation](#motivation)
  - [Author](#author)

## Technologies

This project was built with `Python` and `Typer`, a library for creating command-line interfaces (CLI). For text-to-speech functionality, it uses the [`Kokoro-82M`](https://huggingface.co/hexgrad/Kokoro-82M) AI model. To search for words, it utilizes the [`Merriam-Webster Learner's Dictionary API`](https://dictionaryapi.com/products/api-learners-dictionary). The Anki decks are generated using the [`genakin`](https://github.com/kerrickstaley/genanki) library.

## Getting Started

### Prerequisites

For run this project, you will need the following things:

- [`Python 3.12.9`](https://www.python.org/)
- [`Merriam Webster API Key`](https://dictionaryapi.com/)

You need to create `.env` file into the project folder with the following keys: `MERRIAM_WEBSTER_DICTIONARY_API`

### Installation
After fill all the [`prerequisites`](#prerequisites) you can create a `.venv` folder for local installation of the required packages.

For install the `required` packages for the project you need to run:

```bash
pip install -r requirements.txt
```

If you want to install in your machine for use any time, you need to run this command in the project folder:

```bash
pip install .
```

### Usage

If you only want to run the project directly in the folder you can run the following command for see all the commands:

```bash
python -m anki_deck_generator --help
```

or if you install in your machine run this command:

```bash
anki_deck --help
```

## Contributing

If you'd like to contribute to this project, please follow these steps:

1.  Fork this repository.
2.  Create a branch: `git checkout -b feature/your-feature`.
3.  Make your changes and commit them: `git commit -m 'Add some feature'`.
4.  Push to the original branch: `git push origin feature/your-feature`.
5.  Create a pull request.


## Backlog
 - [x] Create a place to store words that have already been added to avoid extra work (a CSV with word, status headers).
 - [ ] Use an offline dictionary to improve performance.
 - [ ] Allow adding cards to existing decks (currently, a new deck must be created).
 - [ ] Use default values for IPA, meaning, and example if they are not found in the dictionary.
 - [ ] Add a Rich progress bar to display what is happening behind the scenes.

## Motivation
In 2025, I set a goal to improve my English to secure a job earning in dollars, euros, or any other currency stronger than the Brazilian real. To achieve this, I started a routine of studying for 2 hours every day, divided as follows:

- Reading: 30 minutes.
- Listening: 30 minutes.
- Grammar: 30 minutes.
- Conversation: 30 minutes.

My idea was to take words I didn't know during reading and listening and add them to my Anki deck for later study. However, this process became problematic. To add a new card, I had to look up the word in a dictionary, get the meaning and an example, generate text-to-speech for each, and then transfer everything to Anki in the correct fields.

Basically, it took me 5 minutes to add a new word. So, the best solution was to automate this process.

That's how I decided to create this CLI to automate the creation of my flashcards. 

## Author

<img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/49854105?v=4" width="100px;" alt=""/>
<br />
<sub><b>Julio Martins</b></sub></a>

Made by Julio Martins 👋🏽 Contact me!

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-1262BF?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ojuliomartins/) 
[![Email Badge](https://img.shields.io/badge/-Email-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:contact.juliomartins@gmail.com)


<p align="right">(<a href="#readme-top">back to top</a>)</p>
