import random

def first(x: str) -> str:
    return f'first {x}'

def second(y: int) -> str:
    return f'second {y}'

if __name__ == '__main__':
    x = first if random.random() > 0.5 else second
    print(x('hi'))
