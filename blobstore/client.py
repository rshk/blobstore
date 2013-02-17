#!/usr/bin/env python

# This is the client; just a wrapper around calls in the server..

import optparse
import sys
import zerorpc

def main():
    parser = optparse.OptionParser()
    parser.disable_interspersed_args()
    parser.add_option("--port", action='store', dest='server_port')
    parser.add_option("--address", action='store', dest='server_address')
    opts, args = parser.parse_args()

    from . import DEFAULT_PORT, DEFAULT_ADDR
    server_port = opts.server_port or DEFAULT_PORT
    server_address = opts.server_address or DEFAULT_ADDR

    client = zerorpc.Client()
    client.connect("tcp://{}:{}".format(server_address, server_port))

    command = args[0]

    if command == 'store':
        try:
            filename = args[1]
            if filename == '-':
                filename = None
        except IndexError:
            filename = None

        if filename is None:
            blob = sys.stdin.read()

        else:
            with open(filename, 'rb') as f:
                blob = f.read()

        print client.store(blob)

    elif command == 'retrieve':
        blob_id = args[1]
        sys.stdout.write(client.retrieve(blob_id))

    elif command == 'delete':
        blob_id = args[1]
        client.delete(blob_id)

    elif command == 'list':
        for blob_id in client.list():
            print blob_id

if __name__ == '__main__':
    main()
