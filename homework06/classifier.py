import typing
from collections import Counter
from math import log


def clean(s: str):
    for x in "-=,.!?":
        s = s.replace(x, "")
    return s


class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class NaiveBayesClassifier:
    """
    NaiveBayesClassifier
    """

    def __init__(self, alpha: float = 1e-10):
        self.alpha = alpha
        self.counters: typing.Dict[int, Counter[str]] = dict()
        self.global_counter: Counter[str] = Counter()
        self.class_counter: Counter[int] = Counter()
        self.words_count = 0

    def fit(self, x: typing.List[str], y: typing.List[int]):
        """ Fit Naive Bayes classifier according to x, y. """
        for ind, text in enumerate(x):
            text_cleaned = clean(text)
            if y[ind] not in self.counters:
                self.counters.update({y[ind]: Counter()})
                self.class_counter[y[ind]] = 0
            self.class_counter[y[ind]] += 1
            for word in text_cleaned.split():
                if word not in self.counters[y[ind]]:
                    self.counters[y[ind]][word] = 0
                if word not in self.global_counter:
                    self.global_counter[word] = 0
                self.counters[y[ind]][word] += 1
                self.global_counter[word] += 1
                self.words_count += 1

    def predict(self, x: typing.List[str]):
        """ Perform classification on an array of test vectors x. """
        predicted_values: typing.List[typing.List[Pair[int, float]]] = []
        count_of_articles = sum(map(lambda it: self.class_counter[it], self.class_counter))
        for string in x:
            predicted_values.append([])
            for i in self.counters:
                predicted_values[-1].append(
                    Pair(
                        i,
                        log(self.class_counter[i] / count_of_articles)
                        + sum(
                            map(
                                lambda it: log(
                                    (self.counters[i][it] if it in self.counters[i] else 0)
                                    + self.alpha
                                    / (
                                        (
                                            self.global_counter[it]
                                            if it in self.global_counter
                                            else 0
                                        )
                                        + self.alpha * self.words_count
                                    )
                                ),
                                string.split(),
                            )
                        ),
                    )
                )
        return [max(a, key=lambda it: it.y).x for a in predicted_values]

    def score(self, x_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass
