import typing
from collections import Counter
from math import log


def clean(s: str):
    for x in ",.!?;#$%^*-=":
        s = s.replace(x, "")
    for x in '/()"+':
        s = s.replace(x, " ")
    return s


class NaiveBayesClassifier:
    """
    NaiveBayesClassifier
    """

    def __init__(self, alpha: float = 1e-200):
        self.alpha = alpha
        self.counters: typing.Dict[int, typing.Counter[str]] = dict()
        self.global_counter: typing.Counter[str] = Counter()
        self.class_counter: typing.Counter[int] = Counter()
        self.words_count = 0

    def fit(self, x: typing.List[str], y: typing.List[typing.Any]):
        """ Fit Naive Bayes classifier according to x, y. """
        self.counters = dict()
        self.global_counter = Counter()
        self.class_counter = Counter()
        self.words_count = 0
        for ind, text in enumerate(x):
            text_cleaned = clean(text)
            if y[ind] not in self.counters:
                self.counters.update({y[ind]: Counter()})
                self.class_counter[y[ind]] = 0
            self.class_counter[y[ind]] += 1
            for word in map(lambda it: it.lower(), text_cleaned.split(" ")):
                if word == "":
                    continue
                if word not in self.counters[y[ind]]:
                    self.counters[y[ind]][word] = 0
                if word not in self.global_counter:
                    self.global_counter[word] = 0
                self.counters[y[ind]][word] += 1
                self.global_counter[word] += 1
                self.words_count += 1

    def predict(self, x: typing.List[str]):
        """ Perform classification on an array of test vectors x. """
        predicted_values: typing.List[typing.List[typing.Tuple[int, float]]] = []
        count_of_articles = sum(map(lambda it: self.class_counter[it], self.class_counter))
        for string in x:
            string_cleaned = clean(string)
            predicted_values.append([])
            for i in self.counters:
                predicted_values[-1].append(
                    (
                        i,
                        log(self.class_counter[i] / count_of_articles)
                        + sum(
                            map(
                                lambda it: log(
                                    (
                                        (self.counters[i][it] if it in self.counters[i] else 0)
                                        + self.alpha
                                    )
                                    / (
                                        (
                                            self.global_counter[it]
                                            if it in self.global_counter
                                            else 0
                                        )
                                        + self.alpha * len(self.global_counter.keys())
                                    )
                                )
                                if it != ""
                                else 0,
                                map(lambda it: it.lower(), string_cleaned.split(" ")),
                            )
                        ),
                    )
                )
        return [max(a, key=lambda it: it[1])[0] for a in predicted_values]

    def score(self, x_test: typing.List[str], y_test: typing.List[typing.Any]) -> float:
        """ Returns the mean accuracy on the given test data and labels. """
        results = self.predict(x_test)
        return sum(y_test[it] == results[it] for it in range(len(y_test))) / len(y_test)
