#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test mocks

Execute "sys.exit('some error message')" on errors
"""
import argparse
import os
from pdb import set_trace as debug
import sys

from unittest.mock import patch, MagicMock as MM

class Foo():
    def method(self):
        return "bar"

def some_func():
    instance = Foo()
    return instance.method()

def main():
    """Main function"""
    with patch('__main__.Foo') as mock:
        debug()
        instance = mock.return_value
        instance.method.return_value = 'baz'
        result = some_func()
        assert result == 'baz'

if __name__ == "__main__":
    sys.exit(main())
