from classifier import NaiveBayesClassifier


def test_NaiveBayesClassifier():
    (*data,) = filter(lambda it: it != "", open("tests/SMSSpamCollection").read().split("\n"))
    (*x,) = map(lambda it: it.split("\t")[1], data)
    (*y,) = map(lambda it: it.split("\t")[0], data)
    x_train, y_train, x_test, y_test = x[:3900], y[:3900], x[3900:], y[3900:]
    model = NaiveBayesClassifier()
    model.fit(x_train, y_train)
    assert model.score(x_test, y_test) >= 0.97
