# Nerd Dictation

**Nerd Dictation** is an offline speech-to-text utility for Desktop Linux, designed to be simple, hackable, and with zero background overhead. It uses the [VOSK-API](https://github.com/alphacep/vosk-api) for speech recognition.

## Project Overview

*   **Type:** Python Utility (Single-file script)
*   **Core Technology:** Python 3.6+ (3.8+ recommended), VOSK-API
*   **Platforms:** Linux (X11/Wayland support via external tools)
*   **Architecture:**
    *   `nerd-dictation`: The main executable script. It handles audio recording (via `parec`, `sox`, etc.), speech recognition (VOSK), and output simulation (`xdotool`, `ydotool`, etc.).
    *   **Configuration:** User-defined Python script (`~/.config/nerd-dictation/nerd-dictation.py`) for custom text processing.
    *   **No Daemon:** The process runs only when manually triggered (`begin`/`end`), ensuring zero idle CPU usage.

## Setup & Usage

### Dependencies

1.  **Python Libraries:**
    ```bash
    pip3 install vosk
    ```
2.  **System Tools:**
    *   Audio: `parec` (PulseAudio), `sox`, or `pw-cat` (PipeWire).
    *   Input Simulation: `xdotool` (X11), `ydotool` (Universal), `dotool`, or `wtype` (Wayland).
3.  **VOSK Model:**
    Download a model from [VOSK Models](https://alphacephei.com/vosk/models) and extract it to a directory (e.g., `./model` or `~/.config/nerd-dictation/model`).

### Running

*   **Start Dictation:**
    ```bash
    ./nerd-dictation begin --vosk-model-dir=./model &
    ```
*   **End Dictation:**
    ```bash
    ./nerd-dictation end
    ```

*Note: It is recommended to bind these commands to keyboard shortcuts.*

## Development

### Structure

*   `nerd-dictation`: Main application logic.
*   `readme.rst`: User documentation.
*   `hacking.rst`: Developer guidelines.
*   `tests/`: Unit tests.
*   `package/`: Packaging configuration for different distros.
*   `examples/`: Example user configuration scripts.

### Testing

The project includes unit tests, specifically for text-to-digit conversion logic.

*   **Run Tests:**
    ```bash
    python3 tests/from_words_to_digits.py
    ```
*   **Continuous Testing (Linux):**
    The test file header suggests using `inotifywait` for auto-running tests on change:
    ```bash
    while true; do inotifywait -e close_write nerd-dictation tests/from_words_to_digits.py ; tests/from_words_to_digits.py ; done
    ```

### Code Style & Conventions

*   **Formatting:** Uses `black`.
    ```bash
    black nerd-dictation
    ```
*   **Type Checking:** Uses `mypy`.
    ```bash
    mypy --strict nerd-dictation
    ```
*   **Linting:** Uses `pylint` with specific suppressions (see `hacking.rst` for the full command).
*   **Logging:** All status/debug messages must be printed to `sys.stderr` to avoid interfering with `stdout` text output.

### Security & Privacy

*   **No Hardcoded Paths:** NEVER hardcode the user's home directory (e.g., `/home/mchang`). 
    *   In **Shell Scripts**, use `$HOME`.
    *   In **Systemd Units**, use `%h`.
    *   In **Python**, use `os.path.expanduser("~")`.
*   **Data Sanitization:** Ensure all scripts and documentation are sanitized of personal identifiers before committing or pushing to public repositories.

