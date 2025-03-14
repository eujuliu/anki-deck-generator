from dotenv import dotenv_values

__app_name__ = "Anki Deck Generator"
__version__ = "0.1.0"

(
    SUCCESS,
    WORD_EXISTS_ERROR,
    APP_ERROR,
    WORD_NOT_FOUND_ERROR,
    TTS_ERROR,
    FETCH_ERROR,
    PATH_IS_NOT_JSON_ERROR,
) = range(7)

ENVS = {**dotenv_values(".env")}

ERRORS = {
    WORD_EXISTS_ERROR: "CONFLICT_ERROR: word already exists",
    APP_ERROR: "APP_ERROR: app error, try again later",
    WORD_NOT_FOUND_ERROR: "SEARCH_ERROR: word not found",
    TTS_ERROR: "TTS_ERROR: text-to-speech error",
    FETCH_ERROR: "FETCH_ERROR: error fetching data",
    PATH_IS_NOT_JSON_ERROR: "JSON_ERROR: path is not a json file",
}
