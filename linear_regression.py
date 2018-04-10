import matrix


class linear_regression:

    def __init__(self):
        self.parm = matrix

    def lse_fit(self, X, y):
        self.parm = (X.transpose() * X).inverse() * X.transpose() * y

    def ridge_fit(self, X, y, lambda_):
        lambda_I = matrix.identity(X.cols_)
        self.parm = (X.transpose() * X + lambda_I).inverse() * X.transpose() * y

    def predict(self, X):
        return (X * self.parm)[0, 0]
