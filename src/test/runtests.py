import unittest
import sys 
import io

TEST_MODULES = [
    "test.server_test"
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


def test_runner_factory(stderr):
    class TornadoTextTestRunner(unittest.TextTestRunner):
        def __init__(self, *args, **kwargs):
            kwargs["stream"] = stderr
            super().__init__(*args, **kwargs)

        def run(self, test):
            result = super().run(test)
            if result.skipped:
                skip_reasons = set(reason for (test, reason) in result.skipped)
                self.stream.write(  # type: ignore
                    textwrap.fill(
                        "Some tests were skipped because: %s"
                        % ", ".join(sorted(skip_reasons))
                    )
                )
                self.stream.write("\n")  # type: ignore
            return result


class CountingStderr(io.IOBase):
    def __init__(self, real):
        self.real = real
        self.byte_count = 0

    def write(self, data):
        self.byte_count += len(data)
        return self.real.write(data)

    def flush(self):
        return self.real.flush()

def main():
    import tornado.testing

    kwargs = {}
    orig_stderr = sys.stderr
    # Certain errors (especially "unclosed resource" errors raised in
    # destructors) go directly to stderr instead of logging. Count
    # anything written by anything but the test runner as an error.
    counting_stderr = CountingStderr(orig_stderr)
    sys.stderr = counting_stderr  # type: ignore
    kwargs["warnings"] = False
    kwargs["testRunner"] = test_runner_factory(orig_stderr)
    tornado.testing.main(**kwargs)



if __name__ == "__main__":
    main()