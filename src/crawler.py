from datetime import datetime

from helpers import make_request
from amazonModel import amazonModel
import database
import settings

if __name__ == "__main__":
    with open(settings.start_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            page = make_request(line)
            database.saveAsJson(page)
            print("End")
