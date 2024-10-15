import asyncio
import numpy as np
import sounddevice as sd
from pedalboard import Compressor, HighpassFilter, Invert, LowpassFilter, NoiseGate, Pedalboard, PitchShift

from pedalboard.io import AudioStream

# Voicemeeter AUX Input
DEFAULT_SOUND_DEVICE = 18

def playback_tts(text,volume=1):
    audio_result = asyncio.run(generate_tts_audio(text))
    audio_playback(audio_result,volume)


async def async_playback_tts(text, volume=1):
    audio_result = await generate_tts_audio(text)
    audio_playback(audio_result, volume)


def audio_playback(audio, volume = 1):
    sd.default.device = (None, DEFAULT_SOUND_DEVICE)
    # audio_data = np.frombuffer(audio, dtype=np.int16)
    # # volume adjust
    audio_data = np.frombuffer(audio, dtype=np.int16)
    audio_data = (audio_data * volume).astype(np.int16)
    float_data = audio_data.astype(np.float32)/ 32768.0
    board = Pedalboard([
        PitchShift(semitones=1),
        ])
    
    processed_audio = board(float_data, 22050)
    sd.play(processed_audio, 22050, blocking=True)
    sd.wait()


async def generate_tts_audio(text):
    encoded_text = text.encode('utf-8')

    piper_cmd = [
        './piper-win/piper.exe',
        '-m', './voices/north/en_GB-alba-medium.onnx',
        '--output-raw',
    ]

    proc = await asyncio.create_subprocess_exec(
        *piper_cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate(input=encoded_text)
    if proc.returncode == 0:
        # print(f'TTS generation successful.')
        print()
    else:
        print(f'TTS generation failed with return code {proc.returncode} {stderr}.')

    return stdout
