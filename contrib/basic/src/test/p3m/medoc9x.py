
##
import unittest
import logging

## 
logging.basicConfig(level=logging.DEBUG)


class FooTestCase(unittest.TestCase):
    def test_ten(self):
        logging.info('Testing ten (10)...')
    def test_eleven(self):
        logging.debug('Testing eleven (11)...')

class BarTestCase(unittest.TestCase):
    def test_twelve(self):
        logging.info('Testing twelve (12)...')
    def test_nine(self):
        logging.debug('Testing nine (09)...')

##
def suite():
    suite = unittest.TestSuite()
    suite.addTest(BarTestCase('test_nine'))
    suite.addTest(FooTestCase('test_ten'))
    suite.addTest(FooTestCase('test_eleven'))
    suite.addTest(BarTestCase('test_twelve'))
    return suite

## 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())