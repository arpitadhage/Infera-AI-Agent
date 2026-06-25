from faster_whisper import WhisperModel


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(state):

    files = state.get("files", [])

    audio_texts = []

    for file_path in files:

        if file_path.lower().endswith((".mp3", ".mp4", ".wav", ".m4a")):

            segments, info = model.transcribe(file_path)

            transcript = ""

            for segment in segments:
                transcript += segment.text + " "

            audio_texts.append({
                "text": transcript.strip(),
                "duration": getattr(info, "duration", None),
                "source": file_path
            })

    state["contents"]["audio"] = audio_texts

    return state
