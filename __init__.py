"""Hash Flagging System - Detect duplicate password hashes across employee records"""

from .core import HashFlagger
from .loaders import FileLoader
from .reporters import ReportGenerator

__version__ = "1.0.0"
__author__ = "Peter Hash Byte"

__all__ = ["HashFlagger", "FileLoader", "ReportGenerator"]
