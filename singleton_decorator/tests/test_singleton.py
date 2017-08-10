from unittest import TestCase, mock

from .. import decorator

class TestSingletonWrapper(TestCase):
    """Tests for the _SingletonWrapper class"""

    def setUp(self):
        """
        Creates a mock object for passing into methods
        as the self argument
        """
        self.wrapper = mock.MagicMock()

    def test_init(self):
        """
        Checks whether the constructor holds wrapped class
        and initialise the _instance attribute with None
        """
        # create a mock object for wrapped class
        cls = mock.MagicMock()
        # call the method
        decorator._SingletonWrapper.__init__(self.wrapper, cls)
        # check whether the object holds wrapped class
        self.assertEqual(self.wrapper.__wrapped__, cls)

    def test_call_has_not_instance(self):
        """
        Checks whether the __call__ method creates a new instance
        of wrapped class and returns it if an instance has not been
        created before
        """
        # set init value of _instance to None
        self.wrapper._instance = None
        # create a wrapped mock object
        self.wrapper.__wrapped__ = mock.MagicMock()
        # call the method
        result = decorator._SingletonWrapper.__call__(self.wrapper)
        # check whether the method returns a result of a call
        # of the wrapped class
        self.assertEqual(result, self.wrapper.__wrapped__.return_value)
        # check whether the wrapped class has been called once
        self.wrapper.__wrapped__.assert_called_once_with()
        # check whether the created object has been held
        self.assertEqual(result, self.wrapper._instance)

    def test_call_has_instance(self):
        """
        Checks whether the __call__ method returns the instance created
        before if it already exists and does not create a new one
        """
        # create a wrapped mock object
        self.wrapper.__wrapped__ = mock.MagicMock()
        # call the method
        result = decorator._SingletonWrapper.__call__(self.wrapper)
        # check whether the method returns a held instance
        self.assertEqual(result, self.wrapper._instance)
        # check whether the wrapped class has not been called
        self.assertEqual(self.wrapper.__wrapped__.call_count, 0)


class TestSingleton(TestCase):
    """Tests for the singleton decorator"""

    # patch the wrapper class
    @mock.patch.object(decorator, '_SingletonWrapper')
    def test_singleton(self, wrapper):
        """
        Checks whether the singleton decorator returns a wrapper object
        created by calling a wrapper class with a decorated object
        """
        # create a mock object for decorated class
        cls = mock.MagicMock()
        # call a decorator function
        result = decorator.singleton(cls)
        # check whether the function returns a result of wrapper class call
        self.assertEqual(result, wrapper.return_value)
        # check whether the wrapper class has been created
        # with decorated class
        wrapper.assert_called_once_with(cls)


# create two test classes decorated with the singleton

@decorator.singleton
class Foo:
    """A test class decorated with singleton"""


@decorator.singleton
class Bar:
    """A test class decorated with singleton"""

    def __init__(self, arg, kwarg):
        self.arg = arg
        self.kwarg = kwarg


class TestSingletonIntegration(TestCase):
    """Tests the singleton decorator in work"""

    def test_create_two_objects_from_same_class(self):
        """
        Checks whether an instantiation of decorated class
        returns the same object each time
        """
        self.assertEqual(Foo(), Foo())

    def test_create_two_objects_from_same_class_diff_args(self):
        """
        Checks whether an instantiation of decorated class
        returns the same object each time and its attributes
        does not change
        """
        # create an object
        bar1 = Bar(1, kwarg="foo")
        # check whether the object has attributes arg=1 kwarg=foo
        self.assertEqual(bar1.arg, 1)
        self.assertEqual(bar1.kwarg, "foo")
        # create another object
        bar2 = Bar(2, kwarg="bar")
        # check whether it's the same object
        self.assertEqual(bar1, bar2)
        # check whether its attributes are the same
        self.assertEqual(bar2.arg, 1)
        self.assertEqual(bar2.kwarg, "foo")

    def test_two_objects_from_different_classes(self):
        """
        Checks whether an instantiations of different decorated classes
        return different objects
        """
        # create two objects from different decorated classes
        foo = Foo()
        bar = Bar(1, kwarg="bar")
        # check whether the objects are different
        self.assertNotEqual(foo, bar)

    def test_wrapped_attribute(self):
        """
        Checks whether the __wrapped__ attribute contains a decorated class
        """
        # create an object from decorated class
        foo = Foo()
        # check whether the __wrapped__ attribute contains
        # a class of the foo object
        self.assertEqual(Foo.__wrapped__, foo.__class__)
