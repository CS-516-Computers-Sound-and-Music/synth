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
- `key on` has a velocity
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

