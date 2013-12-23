import socket
import json


class CGResponse(object):
    def __init__(self, response):
        self.response = response

    def __iter__(self):
        return iter(self.response)

    def json(self):
        return json.dumps(self.response)

    def dict(self):
        return self.response


class CGMiner(object):
    def __init__(self, api_ip='127.0.0.1', api_port=4028):
        self.api_ip = api_ip
        self.api_port = api_port

    def __del__(self):
        self.s.close()

    def __linesplit(self, socket):
        buffer = socket.recv(4096)
        done = False
        while not done:
            more = socket.recv(4096)
            if not more:
                done = True
            else:
                buffer = buffer+more
        if buffer:
            return buffer

    def close(self):
        self.s.close()

    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            raise
        self.s.connect((self.api_ip, self.api_port))
        return self.s

    def command(self, command, options=None):
        # TODO figure out options format
        # TODO figure out best way to handle socket state/connects etc
        s = self.connect()
        s.send(json.dumps({"command": command}))
        response = self.__linesplit(self.s)
        response = response.replace('\x00', '')
        response = json.loads(response)
        s.close()
        return CGResponse(response)
