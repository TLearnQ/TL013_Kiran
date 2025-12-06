items = []

def run_request(req):
    method, path = req.split()
    if method == "GET" and path == "/items":
        return items
    if method == "POST" and path == "/items":
        item = {"id": len(items) + 1}
        items.append(item)
        return item
    return "error"