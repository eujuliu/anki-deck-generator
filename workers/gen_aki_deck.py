import genanki
import random
from helpers.format_string import format_string


def gen_aki_deck(
    word: str,
    meaning: str,
    example: str,
    sound: str,
    sound_meaning: str,
    sound_example: str,
):
    sound = format_string(sound)
    sound_meaning = format_string(sound_meaning)
    sound_example = format_string(sound_example)

    id = random.randrange(1 << 30, 1 << 31)
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
                "qfmt": "<div style='font-family: Arial; font-size: 70px;color:#FF80DD;'>{{Word}}</div><hr>{{Sound}}<hr><div style='font-family: Arial; font-size: 70px;color:#FF80DD;'></div>",
                "afmt": "<div style='font-family: Arial; color:#FF80DD;'>{{Word}}</div><hr><div  style='font-family: Arial; color:#00aaaa; text-align:left;'>Meaning: {{Meaning}} {{Sound_Meaning}}</div><hr><div  style='font-family: Arial; color:#9CFFFA; text-align:left;'>Example: {{Example}} {{Sound_Example}}</div>",
                "css": ".card{font-family:arial;font-size:20px;text-align:center;color:#000;background-color:#fff;line-height:1.5em}#typeans{text-align:center;max-width:300px}input#typeans{border-radius:9px}.Translation{font-family:Lucida Sans Unicode;color:gray;padding-top:.5em}}IMG{border-radius:19px}div span{max-width:555px;display:inline-block;text-align:left}.card{color:#000;background-color:#f3f3f3}#typeans span{background-color:#f3f3f3}.typeBad{color:#dc322f;font-weight:700;font-size:23px}.typeMissed,.typePass{color:#268bd2;font-weight:700;font-size:23px}.typeGood{color:#2ed85a;font-weight:700}.smartstep{position:absolute;top:7px;right:27px;background:url(_sse_vk.png) top right no-repeat;display:block;width:50px;height:50px}.small{color:#27AE60;font-size:.7em}.Deck{position:absolute;top:7px;left:0;width:100%}#Deck{font-size:8pt;vertical-align:top;line-height:10pt}",
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

    deck = genanki.Deck(id, "English Leaning")

    deck.add_note(note)
    deck.add_model(model)

    package = genanki.Package(deck)
    package.media_files = [
        f"outputs/audios/{sound}",
        f"outputs/audios/{sound_meaning}",
        f"outputs/audios/{sound_example}",
    ]
    package.write_to_file(f"outputs/{word}.apkg")
