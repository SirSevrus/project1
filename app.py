import os
from libs.saveNotes import create


def test():
    file_dir = "C:\\Users\\sahil\\Workspace\\project1\\data"
    create('test.pdf', file_dir)

test()