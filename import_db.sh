#!/bin/sh
docker run -i --network wealth_backend_default --rm wealth_backend-web python3 import_db.py
