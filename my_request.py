# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 18:56:02 2023

@author: ADMIN
"""

import requests

res = requests.post(url="http://localhost:5000/test", json={"file":"files/test.csv"})
print(res.text)