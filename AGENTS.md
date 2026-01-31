# AI Agent Instructions

## Voice Input Handling
When you receive input that appears to be from a voice memo (often characterized by missing punctuation, run-on sentences, or "hallucinated" words like "You" or "Okay" at the start), you MUST:
1.  **Parse and Organize:** Treat the text as raw intent. Organize it into coherent thoughts or commands before interpreting.
2.  **Safety:** Never execute bash commands or system modifications directly from voice input without first presenting a cleaned-up version of the command to the user for confirmation.
3.  **Organized Output:** If the user is speaking a long prompt, summarize your understanding of their request before providing a full response.