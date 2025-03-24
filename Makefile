.PHONY: test, install

test:
	python -m pytest tests/

install:
	@echo "Setting up environment variables..."
	@touch anki_deck_generator/.env

	@read -p "Enter your MERRIAM_WEBSTER_DICTIONARY_API key: " MERRIAM_WEBSTER_DICTIONARY_API; \
	echo "MERRIAM_WEBSTER_DICTIONARY_API=$$MERRIAM_WEBSTER_DICTIONARY_API" >> anki_deck_generator/.env

	@echo "Environment setup complete."

	@echo "Installing the package..."
	pip install .

	@rm anki_deck_generator/.env

	@echo "Run anki_deck --help for see all commands"