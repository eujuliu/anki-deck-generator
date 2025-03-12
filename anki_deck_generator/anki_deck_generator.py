import io
import soundfile as sf
import requests
import genanki
import random

from anki_deck_generator import (
    SUCCESS,
    ERRORS,
    WORD_EXISTS_ERROR,
    SERVER_ERROR,
    WORD_NOT_FOUND_ERROR,
    TTS_ERROR,
    FETCH_ERROR,
    ENVS,
)

from kokoro import KPipeline
from pathlib import Path


class AnkiDeckGenerator:
    id: str
    deck_name: str
    deck_language: str
    tts_language: str
    audios_path: str
    decks_path: str

    def __init__(self, id: str, deck_name: str, deck_language: str):
        languages = {"en": "a", "pt": "p", "es": "e"}

        self.id = id
        self.deck_name = deck_name
        self.deck_language = deck_language
        self.tts_language = languages[deck_language]
        self.audios_path = f"{Path.home()}/Anki/audios"
        self.decks_path = f"{Path.home()}/Anki/decks/English_Words"

        Path(self.audios_path).mkdir(parents=True, exist_ok=True)
        Path(self.decks_path).mkdir(parents=True, exist_ok=True)

    def dictionary(self, word: str):
        status, data = self._fetch(
            f"https://www.dictionaryapi.com/api/v3/references/learners/json/{word}?key={ENVS["MERRIAM_WEBSTER_DICTIONARY_API"]}"
        )

        if status in ERRORS:
            if data.response.status_code == 404:
                return WORD_NOT_FOUND_ERROR, ERRORS[WORD_NOT_FOUND_ERROR]
            return SERVER_ERROR, data

        ipas, meanings, examples = self._format_merriam_webster_json(data)

        result = {
            "word": word,
            "meaning": meanings[0],
            "example": examples[0],
            "ipa": ipas[0],
        }

        return SUCCESS, result

    def text_to_speech(self, words: tuple, create=False):
        try:
            text = ""
            audios = {}
            for word in words:
                text += f"{word}|"

            pipeline = KPipeline(lang_code=self.tts_language)
            generator = pipeline(text, voice="af_heart", speed=1, split_pattern=r"\|")

            for i, (gs, ps, audio) in enumerate(generator):
                file_name = self._forma_string(gs)

                if create:
                    path = f"{self.audios_path}/{file_name}.mp3"
                    sf.write(path, audio, 24000)
                    audios[file_name] = path
                else:
                    audio_path = io.BytesIO()
                    sf.write(audio_path, audio, 24000, format="mp3")
                    audio_path.seek(0)
                    audios[file_name] = audio_path.read()

            return SUCCESS, audios
        except Exception as err:
            return TTS_ERROR, err

    def get_anki_deck(
        self,
        word: str,
        meaning: str,
        example: str,
        sound: str,
        sound_meaning: str,
        sound_example: str,
    ):
        try:
            id = random.randrange(1 << 30, 1 << 31)
            sound = self._format_string(sound)
            sound_meaning = self._format_string(sound_meaning)
            sound_example = self._format_string(sound_example)

            model = genanki.Model(
                id,
                "Model",
                fields=[
                    {"name": "Word"},
                    {"name": "Meaning"},
                    {"name": "Example"},
                    {"name": "Sound"},
                    {"name": "Sound_Meaning"},
                    {"name": "Sound_Example"},
                ],
                templates=[
                    {
                        "name": "Template",
                        "qfmt": """
                        <div style="font-family:Arial;font-size:70px;color:#FF80DD;">{{Word}}</div><hr>{{Sound}}<hr><div style="font-family:Arial;font-size:70px;color:#FF80DD;"></div>
                        <style>.card{font-family:Arial;font-size:20px;text-align:center;color:#000;background-color:#f3f3f3;line-height:1.5em}#typeans{text-align:center;max-width:300px}input#typeans{border-radius:9px}.Translation{font-family:Lucida Sans Unicode;color:gray;padding-top:.5em}img{border-radius:19px}div span{max-width:555px;display:inline-block;text-align:left}#typeans span{background-color:#f3f3f3}.typeBad{color:#dc322f;font-weight:700;font-size:23px}.typeMissed,.typePass{color:#268bd2;font-weight:700;font-size:23px}.typeGood{color:#2ed85a;font-weight:700}.smartstep{position:absolute;top:7px;right:27px;background:url(_sse_vk.png) top right no-repeat;display:block;width:50px;height:50px}.small{color:#27AE60;font-size:.7em}.Deck{position:absolute;top:7px;left:0;width:100%}#Deck{font-size:8pt;vertical-align:top;line-height:10pt}</style>
                        """,
                        "afmt": """
                        <div style="font-family:Arial;color:#FF80DD;">{{Word}}</div><hr><div style="font-family:Arial;color:#00aaaa;text-align:left;">Meaning: {{Meaning}} {{Sound_Meaning}}</div><hr><div style="font-family:Arial;color:#9CFFFA;text-align:left;">Example: {{Example}} {{Sound_Example}}</div>
                        <style>.card{font-family:Arial;font-size:20px;text-align:center;color:#000;background-color:#f3f3f3;line-height:1.5em}#typeans{text-align:center;max-width:300px}input#typeans{border-radius:9px}.Translation{font-family:Lucida Sans Unicode;color:gray;padding-top:.5em}img{border-radius:19px}div span{max-width:555px;display:inline-block;text-align:left}#typeans span{background-color:#f3f3f3}.typeBad{color:#dc322f;font-weight:700;font-size:23px}.typeMissed,.typePass{color:#268bd2;font-weight:700;font-size:23px}.typeGood{color:#2ed85a;font-weight:700}.smartstep{position:absolute;top:7px;right:27px;background:url(_sse_vk.png) top right no-repeat;display:block;width:50px;height:50px}.small{color:#27AE60;font-size:.7em}.Deck{position:absolute;top:7px;left:0;width:100%}#Deck{font-size:8pt;vertical-align:top;line-height:10pt}</style>
                        """,
                    }
                ],
            )

            note = genanki.Note(
                model=model,
                fields=[
                    word,
                    meaning,
                    example,
                    f"[sound:{sound}]",
                    f"[sound:{sound_meaning}]",
                    f"[sound:{sound_example}]",
                ],
            )

            deck = genanki.Deck(id, self.deck_name)

            deck.add_note(note)
            deck.add_model(model)

            package = genanki.Package(deck)
            package.media_files = [
                f"{self.audios_path}/{sound}",
                f"{self.audios_path}/{sound_meaning}",
                f"{self.audios_path}/{sound_example}",
            ]

            package.write_to_file(f"{self.decks_path}/{word}.apkg")
        except Exception as err:
            return WORD_EXISTS_ERROR, err

    def _fetch(self, url: str, timeout=None, headers: dict = {}):
        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()

            return SUCCESS, response.json()
        except requests.exceptions.RequestException as err:
            return FETCH_ERROR, err

    def _format_merriam_webster_json(self, data: list):
        examples = []
        meanings = []
        ipas = []

        for obj in data:
            if "hwi" in obj:
                if "prs" in obj["hwi"]:
                    for prs in obj["hwi"]["prs"]:
                        ipas.append(prs["ipa"])

            if "def" in obj:
                for definition in obj["def"]:
                    if "sseq" in definition:
                        for sseq in definition["sseq"]:
                            for sense in sseq:
                                if "dt" in sense[1]:
                                    for dt in sense[1]["dt"]:
                                        if dt[0] == "text":
                                            meanings.append(dt[1])
                                        if dt[0] == "vis":
                                            for vis in dt[1]:
                                                examples.append(vis["t"])

        return ipas, meanings, examples

    def _forma_string(string: str):
        return string.replace(" ", "_").lower()
