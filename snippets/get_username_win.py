"""
Get Win Username
"""
import sys
py_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(py_path)
import os

OUT = os.environ.get('USERNAME')
