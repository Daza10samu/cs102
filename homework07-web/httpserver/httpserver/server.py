import concurrent.futures
import socket
import threading
import typing as tp
from concurrent.futures import ThreadPoolExecutor

from .handlers import BaseHTTPRequestHandler, BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        # @see: https://stackoverflow.com/questions/36594400/what-is-backlog-in-tcp-connections
        self.backlog_size = backlog_size
        self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout = timeout
        self._threads: tp.List[threading.Thread] = []

    def serve_forever(self) -> None:
        # @see: http://veithen.io/2014/01/01/how-tcp-backlog-works-in-linux.html
        # @see: https://en.wikipedia.org/wiki/Thundering_herd_problem
        # @see: https://stackoverflow.com/questions/17630416/calling-accept-from-multiple-threads
        sock = socket.socket()
        sock.bind(self.server_address)
        sock.listen(self.backlog_size)

        with ThreadPoolExecutor(max_workers=self.max_workers) as exec:
            futures = []

            try:
                while True:
                    conn, addr = sock.accept()
                    conn.settimeout(self.timeout)
                    futures.append(exec.submit(self.handle_accept, conn))
            except KeyboardInterrupt:
                for future in futures:
                    future.cancel()
                concurrent.futures.wait(futures, timeout=self.timeout)
                print("Exit")

        sock.close()

    def handle_accept(self, server_socket: socket.socket) -> None:
        handler = self.request_handler_cls(server_socket, self.server_address, self)
        handler.handle()


class HTTPServer(TCPServer):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseHTTPRequestHandler,
    ):
        super().__init__(host, port, backlog_size, max_workers, timeout, request_handler_cls)
