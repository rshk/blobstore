BlobStore
#########

A very simple, `zerorpc`_-based key-value store for binary objects.

This thing works in a way very similar to `git objects storage`_, but
in a client/server fashion.

.. _`zerorpc`: http://zerorpc.dotcloud.com/
.. _`git objects storage`: http://git-scm.com/book/en/Git-Internals-Git-Objects


Example usage
=============

Installation::

    $ python setup.py install


Server::

    $ blobstore_server --storage=/tmp/blobstore-storage


Client::

    $ fortune | blobstore_client store

    $ blobstore_client retrieve cf6e2f0589d303caba3da35b7bac046a5dabe9a2
    O Lord, grant that we may always be right, for Thou knowest we will
    never change our minds.

    $ blobstore_client list
    a86c4d19c567400a917e9574231ae1ebdeb51653
    cf6e2f0589d303caba3da35b7bac046a5dabe9a2
    812807330e2398d90a998aa98ce6851a9d849886
    d2e886096ebb7c7dfa9733b639a298b45acf92fe

    $ blobstore_client delete cf6e2f0589d303caba3da35b7bac046a5dabe9a2

    $ blobstore_client list
    a86c4d19c567400a917e9574231ae1ebdeb51653
    812807330e2398d90a998aa98ce6851a9d849886
    d2e886096ebb7c7dfa9733b639a298b45acf92fe


Testing
=======

To run the test cases, simply install and run ``tests.py``::

    $ python tests.py
