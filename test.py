import unittest
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover("tests")
    testRunner = unittest.runner.TextTestRunner()
    runner = testRunner.run(tests)
    if runner.errors:
        raise Exception("error in tests")
