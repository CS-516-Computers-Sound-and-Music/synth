import mido
import argparse
import numpy as np
import sounddevice as sd
from scipy import signal

DEBUG = False
vlm_cntrl = lambda x: x
SAMPLE_RATE = 88200

# Callback Parameters
notes_playing = []
def generate_sawtooth(note, t, wave_width=0.5):
    freq = note_to_freq(note)
    print(note, ": ", freq)
    sample = signal.sawtooth(2*np.pi*freq*t, width=wave_width) #type:ignore
    return sample
def generate_sinwave(note,t):
    freq = note_to_freq(note)
    sample = np.sin(2 * np.pi * freq * t)
    return sample
wave_gen = generate_sinwave


def fade(wave, fade_length=80):
    fade_in = np.linspace(0.0,1,fade_length)
    fade_out = np.linspace(1,0.0,fade_length)
    bowl = np.ones(wave.shape[0] - 2*fade_length)

    mask = np.concatenate((fade_in,bowl,fade_out))
    # wave = np.concatenate((fade_in,wave[fade_length:-fade_length],fade_out))

    return wave*mask

def note_to_freq(note, ref_freq = 440, ref_note = 69):
    """ Get the frequency of a note given the number of 
    semitones it is away from the base tone (default: A4-440Hz)
    """
    return ref_freq * 2**((note-ref_note)/12)


def callback(outdata, frames, time, status):
    global notes_playing, wave_gen
    
    wave=np.zeros(frames)
    t = np.arange(frames, dtype='float32')/SAMPLE_RATE
    for note in notes_playing:
        wave = np.add(wave, 
                      wave_gen(note, t))
    
    if len(notes_playing)>0:
        wave = fade(wave) #ramp over 0.1 MS
        wave = wave/np.max(wave)*0.708
    
        
    outdata[:] = wave.reshape(-1,1) #type:ignore


def main(wave_generator):
    global notes_playing, wave_gen
    wave_gen=wave_generator
    # print out some information about the midi connecting
    print(f'Ports available: {mido.get_input_names()}')
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
                    notes_playing.append(int(msg.note))
                elif msg.type == "note_off":
                    notes_playing.remove(int(msg.note))
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
    parser.add_argument("--sin", action='store_true')
    args = parser.parse_args()
    DEBUG = args.debug
    
    main(wave_generator=generate_sinwave if args.sin else generate_sawtooth)

    

