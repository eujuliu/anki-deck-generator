from flask import Flask, request, jsonify
from marshmallow import ValidationError
from schemas.card import Content

from helpers.delete_files_in_directory import delete_files_in_directory

from workers.dictionary import dictionary
from workers.tts import tts
from workers.gen_aki_deck import gen_aki_deck

app = Flask(__name__)


@app.route("/card", methods=["POST"])
def create():
    request_data = request.json
    schema = Content()

    try:
        content = schema.load(request_data)
    except ValidationError as err:
        app.logger.error(err.messages)
        return jsonify(err.messages), 400

    data = dictionary(content["word"], content["language"])

    if isinstance(data, Exception):
        return jsonify(data), 404

    tts(
        lang_code=content["language"],
        words=tuple(data.values()),
    )

    gen_aki_deck(
        word=data["word"],
        meaning=data["meaning"],
        example=data["example"],
        sound=f"{data['word']}.mp3",
        sound_meaning=f"{data['meaning']}.mp3",
        sound_example=f"{data['example']}.mp3",
    )

    delete_files_in_directory(f"outputs/audios")

    return (
        jsonify(
            {
                "word": data["word"],
                "meaning": data["meaning"],
                "example": data["example"],
            }
        ),
        201,
    )
