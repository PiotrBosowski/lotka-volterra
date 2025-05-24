class LotkaVoltera:
    def __init__(self, r: float, a: float, b: float, m: float):
        self.r = r
        self.a = a
        self.b = b
        self.m = m

    def __call__(self, _, current_point):
        V, P = current_point
        dVdt = self.r * V - self.a * V * P
        dPdt = - self.m * P + self.b * V * P 
        return [dVdt, dPdt]
    

class LotkaVolteraLimitedEnviron:
    def __init__(self, r: float, a: float, b: float, m: float, k: float):
        self.r = r
        self.a = a
        self.b = b
        self.m = m
        self.k = k

    def __call__(self, _, current_point):
        V, P = current_point
        dVdt = self.r * V * (1 - V / self.k) - self.a * V * P
        dPdt = - self.m * P + self.b * V * P 
        return [dVdt, dPdt]
    

class LotkaVolteraPreyShelters:
    def __init__(self, r: float, a: float, b: float, m: float, s: float):
        self.r = r
        self.a = a
        self.b = b
        self.m = m
        self.s = s

    def __call__(self, _, current_point):
        V, P = current_point
        dVdt = self.r * V - self.a * (V - self.s) * P
        dPdt = - self.m * P + self.b * (V - self.s) * P 
        return [dVdt, dPdt]
    