#!/usr/bin/env python
__author__    = "Phil Hendren"
__copyright__ = "Copyright 2014, Mind Candy"
__credits__   = ["Phil Hendren"]
__license__   = "MIT"
__version__   = "1.0"

from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
