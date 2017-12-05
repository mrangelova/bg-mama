from helpers import make_request
import database
import settings


if __name__ == "__main__":
    with open(settings.start_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            page = make_request(line)
            database.save(page)
            print("End")
