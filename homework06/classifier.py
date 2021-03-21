import typing
from collections import Counter, defaultdict
from math import log

T = typing.TypeVar("T", str, int)


def clean(s: str) -> str:
    for x in ",.!?;#$%^*-=":
        s = s.replace(x, "")
    for x in '/()"+':
        s = s.replace(x, " ")
    return s


class NaiveBayesClassifier(typing.Generic[T]):
    """
    NaiveBayesClassifier
    """

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.counters: typing.DefaultDict[T, typing.DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.words_set: typing.Set[str] = set()
        self.class_counter: typing.DefaultDict[T, int] = defaultdict(int)
        self.words_count = 0

    def fit(self, x: typing.List[str], y: typing.List[T]) -> None:
        """ Fit Naive Bayes classifier according to x, y. """
        self.counters = defaultdict(lambda: defaultdict(int))
        self.words_set = set()
        self.class_counter = defaultdict(int)
        self.words_count = 0
        for xi, yi in zip(x, y):
            self.class_counter[yi] += 1
            for word in xi.split():
                self.counters[yi][word] += 1
                self.words_set.add(word)
                self.words_count += 1

    def predict(self, x: typing.Sequence[str]) -> typing.List[T]:
        """ Perform classification on an array of test vectors x. """
        predicted_values: typing.List[typing.List[typing.Tuple[T, float]]] = []
        count_of_articles = sum(map(lambda it: self.class_counter[it], self.class_counter))
        for string in x:
            predicted_values.append([])
            for class_ind in self.counters:
                curr_value = log(self.class_counter[class_ind] / count_of_articles)
                for word in string.split():
                    curr_value += log(
                        (self.counters[class_ind][word] + self.alpha)
                        / (
                            sum(self.counters[class_ind].values())
                            + self.alpha * len(self.words_set)
                        )
                    )
                predicted_values[-1].append((class_ind, curr_value))
        return [max(a, key=lambda it: it[1])[0] for a in predicted_values]

    def score(self, x_test: typing.List[str], y_test: typing.List[T]) -> float:
        """ Returns the mean accuracy on the given test data and labels. """
        results = self.predict(x_test)
        return sum(y_test[it] == results[it] for it in range(len(y_test))) / len(y_test)
