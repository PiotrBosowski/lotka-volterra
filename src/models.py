from typing import List


class LotkaVoltera:
    def __init__(self, r: float, a: float, b: float, m: float):
        self.r = r
        self.a = a
        self.b = b
        self.m = m

    def __call__(self, _, current_point):
        V, P = current_point
        dVdt = self.r * V - self.a * V * P
        dPdt = - self.m * P + self.a * self.b * V * P 
        return [dVdt, dPdt]
    
    def stability_points(self) -> List:
        return [(0, 0, 'origin'), (self.m / (self.a * self.b), self.r / self.a, 'equilibrium')]


class LotkaVolteraLimitedEnviron(LotkaVoltera):
    def __init__(self, r: float, a: float, b: float, m: float, k: float):
        super().__init__(r, a, b, m)
        self.k = k

    def __call__(self, _, current_point):
        V, P = current_point
        dVdt = self.r * V * (1 - V / self.k) - self.a * V * P
        dPdt = - self.m * P + self.a * self.b * V * P 
        return [dVdt, dPdt]
    
    def stability_points(self) -> List:
        return [(0, 0, 'origin'), (self.k, 0, 'full environment'), (self.m / (self.a * self.b), (self.r / self.a) * (1 - self.m / (self.a * self.b * self.k)), 'equilibrium')]

class LotkaVolteraPreyShelters(LotkaVoltera):
    def __init__(self, r: float, a: float, b: float, m: float, s: float):
        super().__init__(r, a, b, m)
        self.s = s

    def __call__(self, _, current_point):
        V, P = current_point
        dVdt = self.r * V - self.a * (V - self.s) * P
        dPdt = - self.m * P + self. a * self.b * (V - self.s) * P
        return [dVdt, dPdt]

    def stability_points(self) -> List:
        return [(0, 0, 'origin'), (self.s + self.m / (self.a * self.b), self.r * (1 / self.a + self.b * self.s / self.m), 'equilibrium')]


models = {
    "Base model": LotkaVoltera,
    "Limited environment": LotkaVolteraLimitedEnviron,
    "Prey shelters": LotkaVolteraPreyShelters,
}