from kokoro import KPipeline
import soundfile as sf
from helpers.format_string import format_string


def tts(lang_code: str, words: tuple):
    languages = {"en": "a", "pt": "p", "es": "e"}
    text = ""
    for word in words:
        text += f"{word}|"

    pipeline = KPipeline(lang_code=languages[lang_code])
    generator = pipeline(text=text, voice="af_heart", speed=1, split_pattern=r"\|")

    audios = {}

    for i, (gs, ps, audio) in enumerate(generator):
        audios[gs] = audio

        sf.write(f"outputs/audios/{format_string(gs)}.mp3", audio, 24000)

    return audios
