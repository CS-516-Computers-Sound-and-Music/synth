# synth

My first step in this assignment was connecting 
my (really Gatlin's - thank you, Gatlin) MPK mini 2 to my Mac to see if I could read imports
through the mido library. I used the code below to print 
out messages from the midi:
```
port_name = mido.get_input_names()[0] #type:ignore
print("using port ", port_name )#type:ignore

with mido.open_input(port_name) as port: #type:ignore
    print("Listening for MPK Mini messages... Press Ctrl+C to stop.")
    for msg in port:
        print(msg)
```

After pressing a few keys, I found the following
- `key on` has a velocity > 0
- `key off` has velocity 0
- True `velocity` can go between 1 and 127 (I am assuming that there are 7 bits allocated for the velocity). Velocity does not
change between key off events.
- There are two octaves on the midi. 
The bottom `C` key is note 48. The high `C` key is note 72. There 
are 3 `C` keys and two of every other key. 
-  There is a pitchwheel that outputs many messages when its 
activated. I'm not sure how to incorporate these at the moment.
- There are 8 drum pads. While the _keys are mapped to channel 1_
while _drum pads are mapped to channel 0_ and notes 44 through 50. 


I used basically the same `note_to_freq` method as from aleatoric. The only change that I made here was to use the note provided by the midi to calculate the semitone offset by subtracting 69 (where I want the A5 note to be on the keyboard) from the note provided.

## Envoloping and buzzing
Though my envelope worked fine for the aleatoric music, I have noticed continued buzzing (low end noise that I assume is from some sort of aliasing). This occurs even with a sin wave, which I find frustrating. However, the sawtooths sound pretty much how I'd expect. 

Overall, this has been pretty fun and I'm excited to play around more with the Midi! I had no issues with latency, but because of the callback function, though, I have been struggling to create a sense of continuity between samples in the buffer.