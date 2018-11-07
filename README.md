# Conformance test

A tool to search for [specification][] violations.  Requires Python 3.

Usage:

    $ python3 -m venv conform
    $ source conform/bin/activate
    (conform) $ pip install -e . -r requirements.txt
    (conform) $ openregister-conformance --api-version version-number https://url-of-register [https://another-register ...]

Example of running tests against `localhost`:
```
openregister-conformance --no-https --register school --register-domain openregister.local:8080  --api-version 1 http://localhost:8080/v1/
```

The `api-version` option should be set to the version of the [specification][] you want to test against. Currently only one version is available, but we are working on a new version, which will include any backwards-incompatable API changes from [accepted RFCs](https://github.com/openregister/registers-rfcs). To test against this version, run:

```
openregister-conformance --no-https --register school --register-domain openregister.org:8080  --api-version 2 http://localhost:8080/next/
```

There may be tests for future work that has not been implemented yet.
These are marked with [`xfail`][xfail] annotations.  The
`openregister-conformance` script currently runs these tests but does
not worry if they fail.  To force these tests to run, run them with
`py.test` using the `--runxfail` parameter:

    py.test --runxfail --endpoint 'http://localhost:8080' --api-version 1 --register school --register-domain 'openregister.org:8080' -m 'not https'

Note that passing all of the tests does not guarantee that you have a
fully-conformant implementation.

## License

Unless stated otherwise, this codebase is released under [the MIT
license](./LICENSE).


[specification]: https://openregister.github.io/specification/
[xfail]: https://pytest.org/latest/skipping.html
