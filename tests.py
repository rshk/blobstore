# -*- coding: utf-8 -*-

"""
:author: samu
:created: 2/18/13 3:27 PM
"""


import hashlib
import os
import shutil
import subprocess
import unittest


class StorageTestCase(unittest.TestCase):
    """We test the scripts, using subprocess"""

    def setUp(self):
        self.tmp_dir = os.tmpnam()
        print "-- TMP DIR {}".format(self.tmp_dir)
        os.makedirs(self.tmp_dir)
        self.server_process = subprocess.Popen([
            'blobstore_server',
            '--storage={}'.format(self.tmp_dir),
            '--address=127.0.0.1',
            '--port=16135',
        ])

    def tearDown(self):
        self.server_process.terminate()
        shutil.rmtree(self.tmp_dir)

    def test_store_blobs(self):
        """Test storage/retrieval of some blobs"""

        BLOBS = [
            "First string of example text",
            "Second string of example text",

            # Blobs cannot be unicode! We must encode 'em first..
            u"Ju§t áñóth€r lĩnẽ øf ünïcödë ƭẻxt".encode('utf-8'),

            "Some non-printables: \x01\x02\x03\x04\x80\x81\x82\x83",
        ]
        BLOB_ASSIGNED_IDS = {}

        ## Store the blobs
        for i, blob in enumerate(BLOBS):
            client_process = subprocess.Popen([
                'blobstore_client',
                '--address=127.0.0.1',
                '--port=16135',
                'store',
                '-',
            ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )

            stdoutdata, stderrdata = client_process.communicate(input=blob)
            blob_id = stdoutdata.rstrip()
            self.assertNotIn("\n", blob_id,
                             'output must be a single-line blob_id')
            self.assertRegexpMatches(blob_id, r'^[0-9a-z]{40}$',
                                     'blob_id must be a valid SHA-1 sum')
            self.assertEqual(blob_id, hashlib.sha1(blob).hexdigest(),
                             'blob_id must be the blob SHA-1 sum')
            BLOB_ASSIGNED_IDS[i] = blob_id

        ## Check that the list contains all and only the actual ids
        client_process = subprocess.Popen([
            'blobstore_client',
            '--address=127.0.0.1',
            '--port=16135',
            'list',
        ], stdout=subprocess.PIPE)
        stdoutdata, stderrdata = client_process.communicate(None)
        ids_in_list = []
        for line in stdoutdata.splitlines():
            ids_in_list.append(line.rstrip())
        self.assertListEqual(
            sorted(ids_in_list),
            sorted(BLOB_ASSIGNED_IDS.values()),
            'The blobs list must match the list of ids of inserted blobs.')

        ## Check that stored data is correct
        for i, blob in enumerate(BLOBS):
            client_process = subprocess.Popen([
                'blobstore_client',
                '--address=127.0.0.1',
                '--port=16135',
                'retrieve',
                BLOB_ASSIGNED_IDS[i],
            ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )

            stdoutdata, stderrdata = client_process.communicate(input=blob)
            self.assertEqual(stdoutdata, blob,
                             "The retrieved blob must match the stored one")

    def test_no_duplicates(self):
        """Test that stored data contains no duplicates"""

        BLOBS = [
            'This is the BLOB-0',
            'This is the BLOB-1',
            'This is the BLOB-1',
            'This is the BLOB-0',
            'This is the BLOB-2',
            'This is the BLOB-0',
            'This is the BLOB-1',
        ]
        STORED_IDS = set()

        for i, blob in enumerate(BLOBS):
            client_process = subprocess.Popen([
                'blobstore_client', '--address=127.0.0.1', '--port=16135',
                'store', '-',
            ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
            stdoutdata, stderrdata = client_process.communicate(input=blob)
            blob_id = stdoutdata.rstrip()
            STORED_IDS.add(blob_id)

        client_process = subprocess.Popen([
            'blobstore_client',
            '--address=127.0.0.1',
            '--port=16135',
            'list',
        ], stdout=subprocess.PIPE)
        stdoutdata, stderrdata = client_process.communicate(None)
        ids_in_list = []
        for line in stdoutdata.splitlines():
            ids_in_list.append(line.rstrip())

        self.assertListEqual(
            sorted(ids_in_list),
            sorted(list(STORED_IDS)),
            'The blobs list must match the list of ids of inserted blobs.')


if __name__ == '__main__':
    unittest.main()
