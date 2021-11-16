import socket
from typing import Tuple


class Server:
    def __init__(self, ipAddress: str, port: str) -> None:
        self.clients: set[socket.AddressInfo] = set()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ipAddress, port))

    def recv(self) -> Tuple[str, socket.AddressInfo]:
        message, address = self.server.recvfrom(2048)
        self.clients.add(address)
        return message.decode('utf-8'), address

    def broadcast(self, address: socket.AddressInfo, message: str) -> None:
        for addr in self.clients:
            if addr != address:
                self.server.sendto(message.encode('utf-8'), address)

    def send(self, address: socket.AddressInfo, message: str) -> None:
        self.server.sendto(message.encode('utf-8'), address)

    def remove(self, client: socket.AddressInfo):
        self.clients.remove(client)
