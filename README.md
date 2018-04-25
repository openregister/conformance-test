# Conformance test

A tool to search for [specification][] violations.  Requires Python 3.

Usage:

    $ python3 -m venv conform
    $ source conform/bin/activate
    (conform) $ pip install -e . -r requirements.txt
    (conform) $ openregister-conformance https://url-of-register [https://another-register ...]

Example of running tests against `localhost`:
```
openregister-conformance --no-https --register school --register-domain openregister.org:8080 http://localhost:8080
```

There may be tests for future work that has not been implemented yet.
These are marked with [`xfail`][xfail] annotations.  The
`openregister-conformance` script currently runs these tests but does
not worry if they fail.  To force these tests to run, run them with
`py.test` using the `--runxfail` parameter:

    py.test --runxfail --endpoint https://url-of-register [--endpoint https://another-register ...]

Note that passing all of the tests does not guarantee that you have a
fully-conformant implementation.

## License

Unless stated otherwise, this codebase is released under [the MIT
license](./LICENSE).


[specification]: https://openregister.github.io/specification/
[xfail]: https://pytest.org/latest/skipping.html
