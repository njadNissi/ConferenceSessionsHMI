#!/usr/bin/env python3
import os
from website import create_app


DEBUG = bool(os.getenv("CONF_DEBUG", False))
app = create_app()

if __name__ == '__main__':
    print(DEBUG)
    app.run(debug=DEBUG, host='0.0.0.0')
