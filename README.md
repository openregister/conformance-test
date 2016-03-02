# Conformance test

A tool to search for [specification][] violations.  Requires Python 3.

Usage:

    $ mkvirtualenv -p python3 conform
    $ workon openregister
    (openregister) $ pip install -r requirements.txt
    (openregister) $ py.test --endpoint https://url-of-register

You can pass more than one `--endpoint` parameter to test multiple
registers.

Note that passing all of the tests does not guarantee that you have a
fully-conformant implementation.

[specification]: https://openregister.github.io/specification/
