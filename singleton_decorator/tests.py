from unittest import TestCase, mock

from . import decorator

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
