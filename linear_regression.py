import matrix


class linear_regression:

    def __init__(self):
        self.parm = matrix

    def lse_fit(self, X, y):
        self.parm = (X.transpose() * X).inverse() * X.transpose() * y

    def predict(self, X):
        return (X * self.parm)[0, 0]
