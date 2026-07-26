from openai import OpenAI


client = OpenAI()


def text_to_voice(text, filename="answer.mp3"):

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    response.write_to_file(filename)

    return filename