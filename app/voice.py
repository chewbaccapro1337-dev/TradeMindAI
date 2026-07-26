from openai import OpenAI


client = OpenAI()


def transcribe_voice(file_path):

    with open(file_path, "rb") as audio:

        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio
        )

    return result.text