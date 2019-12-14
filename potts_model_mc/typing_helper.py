from typing import Callable, List

# Python type hinting; the code works in principle without this
Interaction = Callable[[int, int], float]
States = List[int]
