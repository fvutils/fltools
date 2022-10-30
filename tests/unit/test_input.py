
import unittest
from unittest.case import TestCase
import io
import fltools
from .test_base import TestBase

class TestInput(TestBase):
    
    def test_comments(self):
        fp = io.BytesIO(
b'''/**
 * This is a comment
 */
tok1
tok2
'''
            )

        input = fltools.FilelistParser.Input(None, "myfile", fp)

        tok = next(input)
        self.assertEqual(tok.get_img(), "tok1")
        self.assertEqual(tok.lineno, 4)
        print("filename: %s line: %d" % (tok.filename, tok.lineno))
        tok = next(input)
        self.assertEqual(tok.get_img(), "tok2")
        self.assertEqual(tok.lineno, 5)
        print("filename: %s line: %d" % (tok.filename, tok.lineno))

        try:
            next(input)
            self.fail("extraneous token")
        except StopIteration:
            pass
            
        