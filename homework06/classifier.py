import typing as tp
from collections import Counter, defaultdict
from math import log

T = tp.TypeVar("T", str, int)


class NaiveBayesClassifier(tp.Generic[T]):
    """
    NaiveBayesClassifier
    """

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.counters: tp.DefaultDict[T, tp.DefaultDict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.words_set: tp.Set[str] = set()
        self.class_counter: tp.DefaultDict[T, int] = defaultdict(int)
        self.words_count = 0

    def clear_fitted(self) -> None:
        """ clear fitted data to fit classifier again """
        self.counters = defaultdict(lambda: defaultdict(int))
        self.words_set = set()
        self.class_counter = defaultdict(int)
        self.words_count = 0

    def fit(self, x: tp.List[str], y: tp.List[T]) -> None:
        """ Fit Naive Bayes classifier according to x, y. """
        for xi, yi in zip(x, y):
            self.class_counter[yi] += 1
            for word in xi.split():
                self.counters[yi][word] += 1
                self.words_set.add(word)
                self.words_count += 1

    def _predict_class(self, string: str) -> T:
        """ classify current str to class """
        class_ind: tp.Optional[T] = None
        count_of_elements = sum(self.class_counter.values())
        best_val = float("-inf")
        for class_i in self.counters:
            curr_value = log(self.class_counter[class_i] / count_of_elements)
            for word in string.split():
                count_of_curr_word_in_class = self.counters[class_i][word]
                count_of_words_in_curr_class = sum(self.counters[class_i].values())
                curr_value += log(
                    (count_of_curr_word_in_class + self.alpha)
                    / (count_of_words_in_curr_class + self.alpha * len(self.words_set))
                )
            if best_val < curr_value:
                class_ind = class_i
                best_val = curr_value
        if class_ind is None:
            raise Exception("Classifier is not fitted")
        return class_ind

    def predict(self, x: tp.Sequence[str]) -> tp.List[T]:
        """ Perform classification on an array of test vectors x. """
        predicted: tp.List[T] = []
        for string in x:
            predicted.append(self._predict_class(string))
        return predicted

    def score(self, x_test: tp.List[str], y_test: tp.List[T]) -> float:
        """ Returns the mean accuracy on the given test data and labels. """
        results = self.predict(x_test)
        return sum(y_test[it] == results[it] for it in range(len(y_test))) / len(y_test)
