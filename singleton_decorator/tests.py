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
