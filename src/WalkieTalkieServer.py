import os
import time
import logging
import socket
from threading import Thread


class WalkieTalkieServer:
    """Class implementing a simple walkie-talkie server"""

    def __init__(self):
        """Instantiate the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queue_depth = 200
        self.default_chunk_size = 1024
        self.current_clients = []

    def _get_server_port(self):
        """Returns the port associated with the server"""
        return int(os.environ.get('SERVER_PORT', '5000'))

    def _get_server_host(self):
        """Return the host name associated with the server"""
        return os.environ.get('SERVER_HOST', socket.gethostname())

    def _handle_client(self, client_dict):
        """Handles work for each client, multithreaded"""
        logging.info('Registering client: {}'.format(client_dict['address']))
        client_is_connected = True
        while client_is_connected:
            try:
                self._broadcast(client_dict, client_dict['socket'].recv(self.default_chunk_size))
            except socket.error:
                logging.info('Disconnecting client: {}'.format(client_dict['address']))
                self.client_dict['socket'].close()
                self.current_clients.remove(client_dict)
                client_is_connected = False

    def _accept_incoming_clients(self):
        """Accept incoming client connections"""
        while True:
            client_socket, address = self.socket.accept()
            client_dict = {
                'address': address,
                'socket': client_socket,
            }
            self.current_clients.append(client_dict)
            Thread(target=self._handle_client, args=(client_dict,)).start()

    def _broadcast(self, author, broadcast_data):
        """Broadcast data from a client to all clients"""
        for client_dict in self.current_clients:
            if client_dict == author:
                continue
            if client_dict == self.socket:
                continue
            try:
                client_dict['socket'].send(broadcast_data)
                logging.info('broadcasting {}'.format(int(time.time())))
            except Exception as e:
                logging.error(e)
                continue

    def run(self):
        """Run the walkie talkie server"""
        host = self._get_server_host()
        port = self._get_server_port()
        logging.info('Starting server at {}:{}'.format(host, port))
        self.socket.bind((host, port))
        self.socket.listen(self.queue_depth)
        self._accept_incoming_clients()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    WalkieTalkieServer().run()
