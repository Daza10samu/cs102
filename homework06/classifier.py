import typing
from collections import Counter, defaultdict
from math import log


def clean(s: str) -> str:
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
        self.counters: typing.DefaultDict[
            typing.Union[int, str], typing.DefaultDict[str, int]
        ] = defaultdict(lambda: defaultdict(int))
        self.global_counter: typing.DefaultDict[str, int] = defaultdict(int)
        self.class_counter: typing.DefaultDict[typing.Union[int, str], int] = defaultdict(int)
        self.words_count = 0

    def fit(self, x: typing.List[str], y: typing.List[typing.Union[int, str]]):
        """ Fit Naive Bayes classifier according to x, y. """
        self.counters = defaultdict(lambda: defaultdict(int))
        self.global_counter = defaultdict(int)
        self.class_counter = defaultdict(int)
        self.words_count = 0
        for xi, yi in zip(x, y):
            self.class_counter[yi] += 1
            for word in xi.split():
                self.counters[yi][word] += 1
                self.global_counter[word] += 1
                self.words_count += 1

    def predict(self, x: typing.List[str]):
        """ Perform classification on an array of test vectors x. """
        predicted_values: typing.List[typing.List[typing.Tuple[typing.Union[int, str], float]]] = []
        count_of_articles = sum(map(lambda it: self.class_counter[it], self.class_counter))
        for string in x:
            predicted_values.append([])
            for class_ind in self.counters:
                curr_value = log(self.class_counter[class_ind] / count_of_articles)
                for word in string.split():
                    curr_value += log(
                        (self.counters[class_ind][word] + self.alpha)
                        / (self.global_counter[word] + self.alpha * len(self.global_counter.keys()))
                    )
                predicted_values[-1].append((class_ind, curr_value))
        return [max(a, key=lambda it: it[1])[0] for a in predicted_values]

    def score(self, x_test: typing.List[str], y_test: typing.List[typing.Union[int, str]]) -> float:
        """ Returns the mean accuracy on the given test data and labels. """
        results = self.predict(x_test)
        return sum(y_test[it] == results[it] for it in range(len(y_test))) / len(y_test)
