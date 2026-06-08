import mido
import argparse
import numpy as np
import sounddevice as sd
from scipy import signal

DEBUG = False
vlm_cntrl = lambda x: x
SAMPLE_RATE = 44100

current_note = 69
is_playing = False


def note_to_freq(note, ref_freq = 440, ref_note = 69):
    """ Get the frequency of a note given the number of 
    semitones it is away from the base tone (default: A4-440Hz)
    """
    return ref_freq * 2**((note-ref_note)/12)

def generate_sawtooth(note, t, wave_width=0.1):
    freq = note_to_freq(note)
    print(note, ": ", freq)
    sample = signal.sawtooth(2*np.pi*freq*t, width=wave_width) #type:ignore
    return sample
    


def callback(outdata, frames, time, status):
    global current_note, is_playing

    if is_playing:
        t = np.arange(frames, dtype='float32')/SAMPLE_RATE
        wave = generate_sawtooth(current_note, t)
    else:
        wave=np.zeros(frames)
    
    outdata[:] = wave.reshape(-1,1) #type:ignore


def main():
    global current_note, is_playing
    # print out some information about the midi connecting
    port_name = mido.get_input_names()[0] #type:ignore
    print("using port ", port_name )#type:ignore

    # set up the audio stream
    stream = sd.OutputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback)
    stream.start()

    try:
        with mido.open_input(port_name) as port: #type:ignore
            print("Listening for MPK Mini 2 messages... Press Ctrl+C to stop.")
            for msg in port:
                if DEBUG: print(msg)
                if msg.type == "note_on":
                    is_playing=True
                    current_note = int(msg.note)
                elif msg.type == "note_off":
                    is_playing = False
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stream.stop()
        stream.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog='Synth to work with MPK Mini 2',
                    description='Generates basic sounds for MPK Mini 2',
                    epilog='Code by Shane :)')
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    DEBUG = args.debug
    main()

    

