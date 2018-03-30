import time


class SwitchSign(Exception):
    pass

class BreakOut(Exception):
    pass

def inner():
    coef = 1
    total = 0
    while True:
        try:
            input_val = yield total
            total +=coef*input_val
        except SwitchSign:
            coef = -coef
        except BreakOut:
            return total


def outer2():
    print('Before inner(),I do this.')
    yield from inner()
    print('After inner(),I do that')

gen = outer2()
while True:
    next_str= next(gen)
    if not next_str:
        break
    print(next_str)