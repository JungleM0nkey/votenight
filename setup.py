#!/usr/bin/env python3 

import os
from os import path

if path.exists('sample.db'):
    os.rename('sample.db','app.db')