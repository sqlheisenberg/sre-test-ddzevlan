import os
import unittest
import pycodestyle


class TestPep8(unittest.TestCase):
    """Run PEP8 on all project files."""

    def test_pep8(self):
        print("Code Style Test")
        style = pycodestyle.StyleGuide(quiet=False, config_file='./setup.cfg')
        for root, dirs, files in os.walk('./'):
            python_files = [
                os.path.join(root, f) for f in files if f.endswith('.py')]
            style.check_files(python_files)
        n = style.check_files().total_errors
        print(n)
        self.assertEqual(n, 0, 'PEP8 style errors: %d' % n)


def main():
    runTests = TestPep8()
    runTests.test_pep8()


if __name__ == "__main__":
    main()
