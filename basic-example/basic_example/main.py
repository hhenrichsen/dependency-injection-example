from typing import Callable


class Logger:
    """
    Deals with printing in a consistent format.
    """

    def info(self, message: any) -> None:
        print("[INFO ]\t" + str(message))


_logger = Logger()
_COUNTER_COUNT = 100


class Counter:
    """
    Takes a list of filters and runs them through `_COUNTER_COUNT` numbers. If the
    filter passes, it prints its message. 

    Filters is a list of tuples. The first tuple is used to parse the current
    number into a message to be printed. The second is used to determine if the
    first's message should print.
    
    Filters are mutually exclusive.
    """

    def __init__(
        self, filters: list[tuple[Callable[[int], any], Callable[[int], bool]]]
    ):
        """
        :param filters: The list of filters to run.
        """
        self.__filters = filters

    def run(self) -> None:
        """
        Runs the loop of `_COUNTER_COUNT` numbers, printing based on the filters
        given in the `__init__` function.
        """
        for num in range(1, _COUNTER_COUNT):
            for message, filter in self.__filters:
                if filter(num):
                    _logger.info(message(num))
                    break


if __name__ == "__main__":
    counter = Counter(
        [
            (lambda _: "FIZZBUZZ", lambda num: num % 3 == 0 and num % 5 == 0),
            (lambda _: "BUZZ", lambda num: num % 5 == 0),
            (lambda _: "FIZZ", lambda num: num % 3 == 0),
            (lambda num: f"{num}", lambda _: True),
        ]
    )
    counter.run()
