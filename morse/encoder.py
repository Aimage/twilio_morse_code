import sys, os
import time
from pydub import AudioSegment
from pydub.playback import play
from .code import CODE, SEVEN_UNITS, ONE_UNIT, THREE_UNITS


def verify_message(string):
    is_message_valid = True
    error = ""
    keys = CODE.keys()
    for char in string:
        if char.upper() not in keys and char != ' ':
            is_message_valid = False
            error = 'Error the charcter ' + char +' cannot be translated to Morse Code'
            break
    return is_message_valid, error


def message_to_morse_sound(message: str,
                           sound_base_path: str = 'morse_sound_files/',
                           output_file: str = 'output',
                           output_format: str = 'ogg'):
    final_sound = AudioSegment.silent(1)
    for char in message:
        if char == ' ':
            print(' ' * 7)
            time.sleep(SEVEN_UNITS)
            final_sound = final_sound + AudioSegment.silent(SEVEN_UNITS * 1000)
        else:
            print(CODE[char.upper()])
            sound_path = os.path.join(sound_base_path,
                                      char.upper() + '_morse_code.ogg')
            print("Path: ", sound_path)
            sound = AudioSegment.from_ogg(sound_path)
            final_sound = final_sound + sound
            # play(sound)
            time.sleep(THREE_UNITS)
            final_sound = final_sound + AudioSegment.silent(THREE_UNITS * 1000)
    final_sound.export(output_file, format=output_format)
    print(f"morse code written in: {output_file}")
    # play(final_sound)
