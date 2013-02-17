#!/usr/bin/env python

import hashlib
import optparse
import os
import zerorpc



class NotFound(Exception): pass


class StorageRPC(object):
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir

    def store(self, blob):
        blob_id = hashlib.sha1(blob).hexdigest()
        blob_path = self._get_blob_path(blob_id)
        if not os.path.exists(blob_path):
            with self._open(blob_path, 'wb') as f:
                f.write(blob)
        return blob_id

    def retrieve(self, blob_id):
        blob_path = self._get_blob_path(blob_id)
        try:
            with self._open(blob_path, 'rb') as f:
                return f.read()
        except IOError:
            raise NotFound(
                "Unable to retrieve blob with id: {}".format(blob_id))

    def delete(self, blob_id):
        try:
            os.remove(self._get_blob_path(blob_id))
        except OSError:
            raise NotFound(
                "Unable to retrieve blob with id: {}".format(blob_id))

    @zerorpc.stream
    def list(self):
        ## ok, now go and figure out the list of stored blobs :P
        for l1dir in os.listdir(self.storage_dir):
            l1dir_path = os.path.join(self.storage_dir, l1dir)
            for blobfile in os.listdir(l1dir_path):
                yield l1dir + blobfile

    def _get_blob_path(self, blob_id):
        return os.path.join(self.storage_dir, blob_id[:2], blob_id[2:])

    def _open(self, name, mode='rb'):
        _basedir = os.path.dirname(name)
        if 'b' not in mode:
            mode += 'b' # We always want binary mode!
        if not os.path.exists(_basedir):
            os.makedirs(_basedir)
        return open(name, mode)



def main():
    parser = optparse.OptionParser()
    parser.disable_interspersed_args()
    parser.add_option("--port", action='store', dest='listen_port')
    parser.add_option("--address", action='store', dest='listen_address')
    parser.add_option("--storage", action='store', dest='storage_dir')
    opts, args = parser.parse_args()

    # Setup the storage on folder..

    assert opts.storage_dir is not None
    from . import DEFAULT_PORT, DEFAULT_ADDR
    listen_port = opts.listen_port or DEFAULT_PORT
    listen_address = opts.listen_address or DEFAULT_ADDR

    s = zerorpc.Server(StorageRPC(opts.storage_dir))
    s.bind("tcp://{}:{}".format(listen_address, listen_port))

    print "Listening on {}:{}".format(listen_address, listen_port)

    s.run()

if __name__ == '__main__':
    main()
