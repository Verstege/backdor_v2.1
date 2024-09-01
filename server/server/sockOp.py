import struct
import json


def send_data(connection, data):
    size = len(data)
    size_bytes = struct.pack("<I", size)
    connection.send(size_bytes)
    connection.send(data)


def receive_data(connection):
    size_bytes = connection.recv(4)
    size = struct.unpack("<I", size_bytes)[0]

    data = b''
    while len(data) < size:
        data += connection.recv(size - len(data))

    return data


def send_string(connection, string):
    send_data(connection, string.encode('utf-8'))


def receive_string(connection):
    return receive_data(connection).decode('utf-8')


def send_json(connection, data):
    send_string(connection, json.dumps(data))


def receive_json(connection):
    return json.loads(receive_string(connection))
