import socket
import pyaudio
import wave
# Socket
# HOST = socket.gethostname()
HOST = '127.0.0.1'
PORT = 5000

# Audio
p = pyaudio.PyAudio()
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

frames = []
with socket.socket() as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print("Connection from " + address[0] + ":" + str(address[1]))

    data = conn.recv(4096)
    print(data)
    while data != "":
        try:
            data = conn.recv(4096)
            stream.write(data)
        except socket.error:
            print("Client Disconnected")
            break

# print(stream)
stream.stop_stream()


stream.close()

wf = wave.open('output.wav','wb')
wf.setnchannels(2)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(stream))
p.terminate()