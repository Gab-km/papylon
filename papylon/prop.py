"""Classes and functions to represent properties"""

from collections import OrderedDict


class PropResult:
    """A result for the execution of a property."""

    FINISHED = 0
    STOPPED = 1

    def __init__(self, status):
        self.status = status
        self.result = None

    @staticmethod
    def finish(func_name, inputs, is_valid, shrunk_number):
        """
        Create a PropResult instance as a property is finished.

        :param func_name: str
            The name of property.
        :param inputs: list
            The list of arguments in the last execution.
        :param is_valid: bool
            Whether the property is valid or not.
        :param shrunk_number: int
            The number of times in which the arguments are shrunk.

        :return: PropResult
            The result of a executed property which is finished.
        """

        result = PropResult(PropResult.FINISHED)
        result.result = (func_name, inputs, is_valid, shrunk_number)
        return result

    @staticmethod
    def stop(func_name, inputs, error):
        """
        Create a PropResult instance as a property is stopped.

        :param func_name: str
            The name of property.
        :param inputs: list
            The list of arguments in the last execution.
        :param error: Exception
            The Exception instance occurred in the execution.

        :return: PropResult
            The result of a executed property which is stopped.
        """

        result = PropResult(PropResult.STOPPED)
        result.result = (func_name, inputs, error)
        return result

    def has_finished(self):
        """
        Get a value indicating whether the PropResult is finished.

        :return: bool
            True if the execution is finished; otherwise, False.
        """

        return self.status == PropResult.FINISHED

    def has_stopped(self):
        """
        Get a value indicating whether the PropResult is stopped.

        :return: bool
            True if the execution is stopped; otherwise, False.
        """

        return self.status == PropResult.STOPPED

    def get(self):
        """
        Get a value of result.

        :return: tuple
            A tuple value of result.
        """

        return self.result


class PropExecutor:
    """A class which executes a property."""

    def __init__(self, arbs, func, max_shrinks):
        self.arbs = arbs
        self.func = func
        self.max_shrinks = max_shrinks

    def execute(self):
        """
        Execute the property.

        Execute the property given in initialization, and return
        the result if the execution is succeeded; otherwise, return
        the result of another execution with shrinking.

        :return: PropResult
            The result for the execution of a property.
        """

        inputs = None
        try:
            inputs = []
            for arb in self.arbs:
                inputs.append(arb.arbitrary())
            is_valid = self.func(*inputs)

            if is_valid:
                return PropResult.finish(self.func.__name__, inputs, is_valid, 0)
            else:
                return self.execute_shrinker(inputs)

        except Exception as error:
            return PropResult.stop(self.func.__name__, inputs, error)

    def execute_shrinker(self, inputs):
        """
        Execute the property with shrinking.

        This method needs to be implemented; otherwise, raise
        NotImplementedError.

        :param inputs: list
            The list of arguments in the last execution.

        :return: PropResult
            The result for the execution of a property.
        """

        raise NotImplementedError("PropExecutor#execute_shrinker")


class PropExecutorWithShrink(PropExecutor):
    """
    A class which executes a property, and executes it with shrinking
    if fails.
    """

    def __init__(self, arbs, func, max_shrinks):
        super().__init__(arbs, func, max_shrinks)

    def execute_shrinker(self, inputs):
        """
        Execute the property with shrinking.

        Execute the property repeatedly with shrinking arguments, and
        return the result.

        :param inputs: list
            The list of arguments in the last execution.

        :return: PropResult
            The result for the execution of a property.
        """

        shrunk_number = 0
        last_inputs = inputs.copy()
        new_inputs = []
        try:
            shrinkings = []
            for _ in range(self.max_shrinks):
                zipped = zip(self.arbs, last_inputs)
                shrinkings.clear()
                for arb, v in zipped:
                    shrinkings.append(arb.shrink(v))
                stop_shrinking = False
                while True:
                    new_inputs.clear()
                    try:
                        for shrinking in shrinkings:
                            new_inputs.append(next(shrinking))
                    except TypeError:
                        break
                    except StopIteration:
                        break

                    if len(new_inputs) != len(self.arbs):
                        break

                    if new_inputs == last_inputs:
                        stop_shrinking = True
                        break

                    is_valid = self.func(*new_inputs)
                    if not is_valid:
                        last_inputs = new_inputs.copy()
                        shrunk_number += 1
                        break

                if stop_shrinking:
                    break
            return PropResult.finish(self.func.__name__, last_inputs, False, shrunk_number)
        except Exception as error:
            return PropResult.stop(self.func.__name__, new_inputs, error)


class PropExecutorWithoutShrink(PropExecutor):
    """
    A class which executes a property, and immediately returns a failed
    result if fails.
    """

    def __init__(self, arbs, func, max_shrinks):
        super().__init__(arbs, func, max_shrinks)

    def execute_shrinker(self, inputs):
        """
        Return a result of the execution as failed.

        :param inputs: list
            The list of arguments in the last execution.

        :return: PropResult
            The result for the execution of a property.
        """

        return PropResult.finish(self.func.__name__, inputs, False, 0)


class Prop:
    """A class representing a property."""

    def __init__(self, arbs, func, executor_type):
        self.executor = executor_type(arbs, func, 100)

    def execute(self):
        """
        Execute the property.

        :return: PropResult
            The result for the execution of a property.
        """

        return self.executor.execute()


def for_all_shrink(arbs, func):
    """
    Create a property which shrinks arguments if fails.

    :param arbs: list
        The Arbitrary list for arguments.
    :param func: function
        The function representing a property.

    :return: Prop
        The Prop instance whose executor_type is
        PropExecutorWithShrink.
    """

    return Prop(arbs, func, executor_type=PropExecutorWithShrink)


def for_all_no_shrink(arbs, func):
    """
    Create a property which doesn't shrink argument.

    :param arbs: list
        The Arbitrary list for arguments.
    :param func: function
        The function representing a property.

    :return: Prop
        The Prop instance whose executor_type is
        PropExecutorWithoutShrink.
    """

    return Prop(arbs, func, executor_type=PropExecutorWithoutShrink)


def for_all(arbs, func):
    """
    Create a property.

    :param arbs: list
        The Arbitrary list for arguments.
    :param func: function
        The function representing a property.

    :return: Prop
        The Prop instance which is created by for_all_shrink.
    """

    return for_all_shrink(arbs, func)


class Properties:
    """A class treating with a number of properties."""

    def __init__(self, group_name):
        self.group_name = group_name
        self.__properties = OrderedDict()

    def add(self, prop_name, prop):
        """
        Add a property into the Properties instance.

        :param prop_name: str
            The property name.
        :param prop: Prop
            The Prop instance.
        """

        self.__properties[prop_name] = prop

    def properties(self):
        """
        Return items of the Properties.

        :return: odict_items
            The items view of the Properties instance.
        """

        return self.__properties.items()
