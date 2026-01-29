# Initial Concept
Offline Speech to Text for Desktop Linux using VOSK-API.

# Product Definition

## Target Audience
- Linux power users who prefer keyboard-centric/CLI workflows.
- Developers and prompt engineers who use CLI-based AI agents (Gemini, Claude, OpenCode) and want a "talk to agent" experience similar to mobile apps but without the limitations.
- Users who write code and specify complex prompts via voice.

## Goals
- Provide a low-latency, "zero-overhead" bridge between voice and the command line.
- Maintain absolute privacy by ensuring no audio or text ever leaves the local machine.
- Enable seamless voice interaction specifically designed for CLI agentic interfaces.
- Create the "Siri equivalent" for CLI agents.

## Key Features
- **Universal Input Compatibility:** CRITICAL: The system MUST work reliably with the text entry boxes of CLI agents like OpenCode, Gemini, and Claude. It must function as a seamless keyboard replacement for these specific interfaces.
- **Configurable Voice Macros:** Allow voice commands to trigger specific agent actions, context switches, or complex prompt templates.
- **Voice Feedback Loop:** Integrated Text-to-Speech (TTS) that reads CLI agent responses back to the user, creating a conversational loop.
- **Agent Integration:** Specialized support for piping voice input into and reading output from Gemini, Claude, and OpenCode CLI tools.
