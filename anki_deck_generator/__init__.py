from dotenv import dotenv_values, find_dotenv

__app_name__ = "Anki Deck Generator"
__version__ = "0.1.0"

(
    SUCCESS,
    WORD_EXISTS_ERROR,
    APP_ERROR,
    WORD_NOT_FOUND_ERROR,
    TTS_ERROR,
    FETCH_ERROR,
) = range(6)

ENVS = {**dotenv_values(find_dotenv())}

ERRORS = {
    WORD_EXISTS_ERROR: "CONFLICT_ERROR: word already exists",
    APP_ERROR: "APP_ERROR: app error, try again later",
    WORD_NOT_FOUND_ERROR: "SEARCH_ERROR: word not found",
    TTS_ERROR: "TTS_ERROR: text-to-speech error",
    FETCH_ERROR: "FETCH_ERROR: error fetching data",
}
