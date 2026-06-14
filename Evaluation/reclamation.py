from regions import Cown, Region


class A:
    pass


def build_cycle():
    a = A()
    a.b = A()
    a.b.a = a
    return a


def add_cycles(region):
    """Create many unreachable cycles in the region."""
    for _ in range(1000):
        region.cycle = build_cycle()
        region.cycle = None


cown = Cown(Region())
while True:
    add_cycles(cown.value)
    # Releasing the cown allows the region GC to run.
    cown.release()
    cown.acquire()
