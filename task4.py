import random
import time

class MockAPI:
    def __init__(self):
        self.pages = {
            1: {"items": [1, 2, 3], "next_page": 2},
            2: {"items": [4, 5], "next_page": None}
        }

    def get_status_page(self, page):
        if random.random() < 0.3:
            return {"error": True, "temporary": True, "data": None}
        if page not in self.pages:
            return {"error": True, "temporary": False, "data": None}
        return {"error": False, "temporary": False, "data": self.pages[page]}


class AutomationClient:
    def __init__(self, api):
        self.api = api
        self.log = []
        self.results = []
        self.max_retries = 3
        self.initial_delay = 0.1

    def log_step(self, message):
        self.log.append(message)

    def poll_page_with_retries(self, page):
        attempts = 0
        delay = self.initial_delay

        while attempts < self.max_retries:
            self.log_step(f"Requesting page {page}, attempt {attempts+1}")
            response = self.api.get_status_page(page)

            if not response["error"]:
                self.log_step(f"Page {page} succeeded.")
                return response["data"]

            if not response["temporary"]:
                self.log_step(f"Page {page} permanent failure. Aborting.")
                return None

            attempts += 1
            self.log_step(f"Temporary failure on page {page}; backoff {delay}s.")
            delay *= 2

        self.log_step(f"Page {page} failed after {self.max_retries} retries.")
        return None

    def run(self):
        page = 1
        while page:
            data = self.poll_page_with_retries(page)
            if data is None:
                self.log_step(f"Stopping pagination at page {page} due to failure.")
                break

            self.results.extend(data["items"])
            self.log_step(f"Collected items from page {page}: {data['items']}")

            page = data.get("next_page")

        self.log_step(f"Run finished. Total items collected: {len(self.results)}.")
        return self.results


if __name__ == "__main__":
    api = MockAPI()
    client = AutomationClient(api)
    all_items = client.run()

    print("RESULTS:", all_items)
    print("LOG:")
    for entry in client.log:
        print(entry)
