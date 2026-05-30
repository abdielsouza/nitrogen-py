# The "Nitrogen" Project Structure

This project is divided into two major folders:

- `src`: The framework source.
- `tests`: The framework test scripts.

The project source is located in the `src/nitrogen` folder and it's divided into some minor modules:

- `core`: This folder keeps the core functionalities and structures that will be used in the other modules.
- `backends`: This folder contains the backend modules to connect the framework with external platforms and systems, making the interaction between them possible.
- `engine`: It's the engine that does the heavy job for you. This engine is an interface to deal with spreadsheets more easily.
- `parser`: An experimental parser module to handle complex syntax trees when dealing with spreadsheet formulas.
- `cli`: The nitrogen support for CLI tools.