#!/bin/sh
docker run -i --network wealth_default --rm wealth-web python3 import_db.py
