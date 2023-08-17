import os

from dotenv import load_dotenv

import app

load_dotenv()

if __name__ == "__main__":
    app.run(port=os.getenv("PORT", default=5000),
            host=os.getenv("HOST", default="localhost"),
            debug=True)