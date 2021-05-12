import os
import logging
import socket
from threading import Thread
import pyaudio
import wave
import time


class WalkieTalkieClient:
    """Class implementing a simple walkie-talkie client"""

    def __init__(self):
        """Instantiate the walkie talkie client"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_HOST = os.environ.get('SERVER_HOST')
        self.SERVER_PORT = int(os.environ.get('SERVER_PORT', '5000'))
        self.default_chunk_size = 1024
        self.default_audio_framerate = 20000
        self.default_audio_format = pyaudio.paInt16
        self.default_audio_channels = 1
        self._setup_system_audio()
        self.is_connected = False

    def _setup_system_audio(self):
        """Set up the audio source and sink for the client"""
        pa = pyaudio.PyAudio()
        self.sink = pa.open(
            format=self.default_audio_format,
            channels=self.default_audio_channels,
            rate=self.default_audio_framerate,
            output=True,
            frames_per_buffer=self.default_chunk_size)
        self.source = pa.open(
            format=self.default_audio_format,
            channels=self.default_audio_channels,
            rate=self.default_audio_framerate,
            input=True,
            frames_per_buffer=self.default_chunk_size)

    def _play_startup_sound(self):
        """Play a startup sound to test the installation"""
        logging.info('Playing startup sound')
        startup_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'sounds/startup.wav')
        wavefile = wave.open(startup_path, 'rb')
        data = wavefile.readframes(self.default_chunk_size)
        temp_sink = pyaudio.PyAudio().open(
            format=self.default_audio_format,
            channels=2,
            rate=44100,
            output=True,
            frames_per_buffer=self.default_chunk_size)
        while data:
            temp_sink.write(data)
            data = wavefile.readframes(self.default_chunk_size)
        temp_sink.stop_stream()
        temp_sink.close()
        logging.info('Done')

    def _send_messages(self):
        """Sends audio messages from the client to the server"""
        logging.info('Starting send message thread')
        while self.is_connected:
            try:
                self.socket.sendall(self.source.read(self.default_chunk_size))
            except Exception as e:
                logging.error(e)
                pass

    def _test_audio(self, seconds=3):
        """Connects input to output device for x seconds to test audio"""
        logging.info('Testing Audio: Speak now')
        test_data = []
        for i in range(0, int(self.default_audio_framerate / self.default_chunk_size * seconds)):
            test_data.append(self.source.read(self.default_chunk_size))
        logging.info('Testing Audio: Playing back')
        for data in test_data:
            self.sink.write(data, self.default_chunk_size)
        logging.info('Testing Audio: Complete')

    def _receive_messages(self):
        """Receives audio messages from the server and play it to the sink"""
        logging.info('Starting receive message thread')
        while self.is_connected:
            try:
                self.sink.write(self.socket.recv(self.default_chunk_size))
                logging.info('receiving')
            except Exception as e:
                logging.error(e)

    def _refresh_audio_streams(self):
        """Refresh audio streams"""
        self._close_audio_streams()
        self._setup_system_audio()

    def _close_audio_streams(self):
        """Closes audio streams"""
        self.sink.close()
        self.source.close()

    def _refresh_socket(self):
        """Refresh a failed socket connection"""
        self._close_socket()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def _close_socket(self):
        """Closes the open socket"""
        self.socket.close()

    def run(self):
        """Run the walkie talkie client"""
        try:
            while True:
                try:
                    self.socket.connect((self.SERVER_HOST, self.SERVER_PORT))
                    self.is_connected = True
                    logging.info('Connected to server successfully: {}:{}'.format(
                        self.SERVER_HOST, self.SERVER_PORT))
                    Thread(target=self._receive_messages).start()
                    self._send_messages()
                except Exception as e:
                    logging.error(e)
                    # self._refresh_audio_streams()
                    self._refresh_socket()
                    logging.error('Unable to connect to {}:{}, reattempting...'.format(
                        self.SERVER_HOST, self.SERVER_PORT))
                    time.sleep(2)
        except KeyboardInterrupt:
            logging.info('Disconnecting client')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    WalkieTalkieClient().run()
