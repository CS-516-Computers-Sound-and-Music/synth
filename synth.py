import mido
port_name = mido.get_input_names()[0] #type:ignore
print("using port ", port_name )#type:ignore

with mido.open_input(port_name) as port: #type:ignore
    print("Listening for MPK Mini messages... Press Ctrl+C to stop.")
    for msg in port:
        print(msg)


