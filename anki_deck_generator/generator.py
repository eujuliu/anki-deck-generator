import io
import soundfile as sf
import requests
import genanki
import random
import re

from anki_deck_generator import (
    SUCCESS,
    ERRORS,
    WORD_EXISTS_ERROR,
    APP_ERROR,
    WORD_NOT_FOUND_ERROR,
    TTS_ERROR,
    FETCH_ERROR,
    ENVS,
)

from kokoro import KPipeline
from pathlib import Path


class Generator:
    deck_name: str
    deck_language: str
    tts_language: str
    audios_path: str
    decks_path: str

    def __init__(self, deck_name: str, deck_language: str):
        tts_languages = {"en": "a", "pt": "p", "es": "e"}
        self.deck_name = deck_name
        self.deck_language = deck_language
        self.tts_language = tts_languages[deck_language]
        self.audios_path = f"{Path.home()}/Anki/audios"
        self.decks_path = f"{Path.home()}/Anki/decks"

        Path(self.audios_path).mkdir(parents=True, exist_ok=True)
        Path(self.decks_path).mkdir(parents=True, exist_ok=True)

    def dictionary(self, word: str):
        status, data = self._fetch(
            f"https://www.dictionaryapi.com/api/v3/references/learners/json/{word}?key={ENVS["MERRIAM_WEBSTER_DICTIONARY_API"]}"
        )

        if status in ERRORS:
            return status, data

        ipa, meaning, example = self._format_merriam_webster_json(data)

        result = {
            "word": word,
            "meaning": meaning,
            "example": example,
            "ipa": ipa,
        }

        return SUCCESS, result

    def text_to_speech(self, words: tuple, create=False):
        try:
            text = ""
            audios = {}
            for word in words:
                text += f"{word}|"

            pipeline = KPipeline(
                lang_code=self.tts_language, repo_id="hexgrad/Kokoro-82M"
            )
            generator = pipeline(text, voice="af_heart", speed=1, split_pattern=r"\|")

            for i, (gs, ps, audio) in enumerate(generator):
                file_name = self._format_string(gs)

                if create:
                    path = f"{self.audios_path}/{file_name}.mp3"
                    sf.write(path, audio, 24000)
                    audios[file_name] = f"{file_name}.mp3"
                else:
                    audio_path = io.BytesIO()
                    sf.write(audio_path, audio, 24000, format="mp3")
                    audio_path.seek(0)
                    audios[file_name] = audio_path.read()

            return SUCCESS, audios
        except Exception as err:
            return TTS_ERROR, err

    def create_anki_deck(
        self,
        word: str,
        ipa: str,
        meaning: str,
        example: str,
        sound: str,
        sound_meaning: str,
        sound_example: str,
    ):
        try:
            model = genanki.Model(
                "EDM 1",
                "Model",
                fields=[
                    {"name": "Word"},
                    {"name": "Meaning"},
                    {"name": "Example"},
                    {"name": "IPA"},
                    {"name": "Sound"},
                    {"name": "Sound_Meaning"},
                    {"name": "Sound_Example"},
                ],
                templates=[
                    {
                        "name": "Template",
                        "qfmt": '<div style="display:flex;justify-content:center;align-items:center;flex-direction:column;height:90vh"><div style="font-family:Arial;font-size:70px;color:#ff80dd">{{Word}}</div><br>{{Sound}}<br><div style="font-family:Arial;font-size:70px;color:#ff80dd">{{IPA}}</div></div>',
                        "afmt": '<div style="display:flex;justify-content:center;align-items:center;flex-direction:column;height:90vh"><div style="font-family:Arial;color:#ff80dd;font-size:30px">{{Word}}</div><br><div style="font-family:Arial;color:#0aa;font-size:25px">{{Sound_Meaning}} Meaning: {{Meaning}} </div><br><br><div style="font-family:Arial;color:#9cfffa;font-size:25px">{{Sound_Example}} Example: {{Example}} </div></div>',
                    }
                ],
            )

            note = genanki.Note(
                model=model,
                fields=[
                    word,
                    meaning,
                    example,
                    ipa,
                    f"[sound:{sound}]",
                    f"[sound:{sound_meaning}]",
                    f"[sound:{sound_example}]",
                ],
            )

            deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), self.deck_name)

            deck.add_note(note)
            deck.add_model(model)

            package = genanki.Package(deck)
            package.media_files = [
                f"{self.audios_path}/{sound}",
                f"{self.audios_path}/{sound_meaning}",
                f"{self.audios_path}/{sound_example}",
            ]

            package.write_to_file(f"{self.decks_path}/{word}.apkg")

            return SUCCESS, None
        except Exception as err:
            return APP_ERROR, err

    def _fetch(self, url: str, timeout=None, headers: dict = {}):
        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()

            if response.json() == []:
                return WORD_NOT_FOUND_ERROR, ERRORS[WORD_NOT_FOUND_ERROR]

            return SUCCESS, response.json()
        except requests.exceptions.RequestException as err:
            return FETCH_ERROR, err

    def _format_merriam_webster_json(self, data: list):
        example = None
        meaning = None
        ipa = None

        for obj in data:
            if "hwi" in obj and ipa is None:
                if "prs" in obj["hwi"]:
                    for prs in obj["hwi"]["prs"]:
                        ipa = prs["ipa"]

                if "altprs" in obj["hwi"]:
                    ipa = obj["hwi"]["altprs"][0]["ipa"]

            if "def" in obj:
                for definition in obj["def"]:
                    if "sseq" in definition:
                        for sseq in definition["sseq"]:
                            for sense in sseq:
                                if "dt" in sense[1]:
                                    for dt in sense[1]["dt"]:
                                        if (
                                            dt[0] == "text" and meaning is None
                                        ):  # meaning
                                            meaning = re.sub(
                                                r"\{.*?\}", "", dt[1]
                                            ).strip()

                                            if meaning == "":
                                                meaning = obj["shortdef"][0]

                                        if example is None:  # example
                                            if dt[0] == "vis":
                                                for vis in dt[1]:
                                                    example = re.sub(
                                                        r"\{.*?\}", "", vis["t"]
                                                    )
                                            if dt[0] == "uns":
                                                for uns in dt[1][0]:
                                                    if uns[0] == "vis":
                                                        example = re.sub(
                                                            r"\{.*?\}",
                                                            "",
                                                            uns[1][0]["t"],
                                                        )

        return ipa, meaning, example

    def _format_string(self, string: str):
        return re.sub(r"[^a-zA-Z0-9_]", "", string.replace(" ", "_")).lower()
