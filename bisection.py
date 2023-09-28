class bisection:
    def __init__(self, fx: str = "x", x0: float = 0.0, x1: float = 0.0, e: float = 0.0001):
        """ 
            Initializes the Bisection Class

            :param fx: the string of the function f(x) = 0
            :param x0: first guess
            :param x1: second guess
            :param e: 
        """
        self.x0 = x0
        self.x1 = x1
        self.e = e
        self.fx = fx
        self.steps = {"x2": [], "f(x2)": []}

    def set_fx(self, fx: str):
        self.fx = fx

    def set_x0(self, x0: float):
        self.x0 = x0

    def set_x1(self, x1: float):
        self.x1 = x1

    def set_e(self, e: float):
        self.e = e

    # Defining Function
    def __str__(self):
        return "fx: {}\nguess1: {}\n guess2: {}\ne: {}\n".format(self.fx, self.x0, self.x1, self.e)

    def f(self, x):
        return eval(self.fx, {"x": x})

    # Check is Initial Guess is Valid
    def is_valid(self):
        try:
            if (self.f(self.x0) * self.f(self.x1)) > 0.0:
                return False
            return True
        except:
            return False

    # Implementing Bisection Method
    def solve(self):
        condition = True
        x_0 = self.x0
        x_1 = self.x1
        while condition:
            x2 = (x_0 + x_1)/2
            self.steps["x2"].append(x2)
            self.steps["f(x2)"].append(self.f(x2))
            if self.f(x_0) * self.f(x2) < 0:
                x_1 = x2
            else:
                x_0 = x2
            condition = abs(self.f(x2)) > self.e
        return x2
