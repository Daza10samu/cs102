from classifier import NaiveBayesClassifier, clean
import pathlib


def test_NaiveBayesClassifier():
    with (pathlib.Path(__file__).parent / "SMSSpamCollection").open() as f:
        (*data,) = filter(lambda it: it != "", f.read().split("\n"))
    (*x,) = map(lambda it: it.split("\t")[1], data)
    (*y,) = map(lambda it: it.split("\t")[0], data)
    x_train, y_train, x_test, y_test = x[:3900], y[:3900], x[3900:], y[3900:]
    model = NaiveBayesClassifier()
    model.fit(map(lambda it: clean(it).lower(), x_train), y_train)
    assert model.score(list(map(lambda it: clean(it).lower(), x_test)), y_test) >= 0.97
