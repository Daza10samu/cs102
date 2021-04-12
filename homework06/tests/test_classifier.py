import pathlib
import typing

from classifier import NaiveBayesClassifier
from textutils import clean


def test_NaiveBayesClassifier() -> None:
    with (pathlib.Path(__file__).parent / "SMSSpamCollection").open() as f:
        data = list(filter(lambda it: it != "", f.read().split("\n")))
    x = list(map(lambda it: it.split("\t")[1], data))
    y = list(map(lambda it: it.split("\t")[0], data))
    x_train, y_train, x_test, y_test = x[:3900], y[:3900], x[3900:], y[3900:]
    model = NaiveBayesClassifier()
    model.fit(list(map(lambda it: clean(it).lower(), x_train)), y_train)
    assert model.score(list(map(lambda it: clean(it).lower(), x_test)), y_test) >= 0.9826
