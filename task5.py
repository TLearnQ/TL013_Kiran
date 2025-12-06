import requests
import logging


logging.basicConfig(
    filename="app2.log",
    level=logging.INFO,
  
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_calls(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Function called: {func.__name__} | Args: {args} | Kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper


@log_calls
def fetch_api(url):
    try:
        response = requests.get(url, timeout=5)
        return response.json()
    except Exception:
        return None    # keeps it simple


for label, url in [
    ("GOOD", "https://jsonplaceholder.typicode.com/todos/1"),
    ("BAD", "https://invalid-example-123.com")
]:
    print(f"\nTesting {label} URL:")
    print(fetch_api(url))
