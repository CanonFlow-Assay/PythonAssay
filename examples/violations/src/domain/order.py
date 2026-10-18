def load_order() -> str:
    content = open("order.txt", encoding="utf-8").read()
    print("loaded")
    raise RuntimeError(content)
