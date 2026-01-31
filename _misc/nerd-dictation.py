import re

def nerd_dictation_process(text):
    # 1. Basic Punctuation & Formatting
    # VOSK often returns raw words; let's map common spoken commands to symbols.
    replacements = {
        "period": ".",
        "dot": ".",
        "comma": ",",
        "question mark": "?",
        "exclamation mark": "!",
        "new line": "\n",
        "next line": "\n",
        "open quote": "\"",
        "close quote": "\"",
        "semicolon": ";",
        "colon": ":",
        # 2. ADHD/Productivity Macros
        "make todo": "- [ ] ",
        "check box": "- [ ] ",
        "email signature": "\nBest,\n\n--\n", # Add your name here if you want
        "shrug": r"¯\_(ツ)_/¯",
    }
    
    # Apply simple replacements
    for k, v in replacements.items():
        text = text.replace(f" {k} ", f"{v} ")
        text = text.replace(f" {k}", v)
        if text.startswith(k + " "):
            text = text.replace(k + " ", v, 1)
        if text == k:
            text = v
            
    # 3. Capitalize first letter (basic heuristic)
    if len(text) > 0:
        text = text[0].upper() + text[1:]

    return text
