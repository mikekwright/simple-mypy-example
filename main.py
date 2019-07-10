import random

from typing import Callable, List


def first(x: str) -> str:
    return f'first {x}'

def second(y: int) -> str:
    return f'second {y}'

if __name__ == '__main__':
    funcs = [first, second]  # type: List[Callable[..., str]]
    x = funcs[0] if random.random() > 0.5 else funcs[1] # type: Callable[[str], str]
    print(x('hi'))
