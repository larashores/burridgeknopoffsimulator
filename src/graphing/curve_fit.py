class CurveFit:
    def __init__(self, func=None, display_string=None, limits=None, returns=None, guesses=None):
        self.func = func
        self.limits = limits
        self.string = display_string
        self.returns = returns
        self.values = None
        self.dvalues = None
        self.guesses = guesses