singleton-decorator
===================

.. image:: https://travis-ci.org/Kemaweyan/singleton-decorator.svg?branch=master
    :target: https://travis-ci.org/Kemaweyan/singleton-decorator

.. image:: https://coveralls.io/repos/github/Kemaweyan/singleton-decorator/badge.svg?branch=master
    :target: https://coveralls.io/github/Kemaweyan/singleton-decorator?branch=master


A testable singleton decorator allows easily create a singleton objects
just adding a decorator to class definition but also allows easily write
unit tests for those classes.

A problem
=========

If you use a simple singleton pattern based on a decorator function that
wraps a class with inner wrapper function like this:

.. code-block::

    def singleton(cls):
        instances = {}
        def wrapper(*args, **kwargs):
            if cls not in instances:
              instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return wrapper

it works fine with your classes, but it makes impossible a direct access
to the class object within the wrapper function. So you cannot call methods
using a class name in unit tests:

.. code-block::

    @singleton
    class YourClass:
        def method(self):
            ...
    YourClass.method(...)

this code would not work because ``YouClass`` actually contains a wrapper function
but not your class object. Also this approach causes another problem if your
tests require separate instances of the objects, so a singleton pattern could
break an isolation of different tests.

Solution
========

The **singleton-decorator** offers a simple solution to avoid both of these
problems. It uses a separate wrapper object for each decorated class and holds
a class within ``__wrapped__`` attribute so you can access the decorated class
directly in your unit tests.

Installation
============

To install the **singleton-decorator** just type in the command line:

.. code-block::

    $ pip install singleton-decorator

Usage
=====

At first import the singleton decorator:

.. code-block::

    from singleton_decorator import singleton

Then decorate you classes with this decorator:

.. code-block::

    @singleton
    class YourClass:
        ...

That's all. Now you could create or get existing instance of your class by
calling it as a simple class object:

.. code-block::

    obj = YourClass()  # creates a new instance
    obj2 = YourClass()  # returns the same instance
    obj3 = YourClass()  # returns the same instance
    ...

You also could pass args and kwargs into constructor of your class:

.. code-block::

    obj = YourClass(1, "foo", bar="baz")

.. NOTE::

    Since the singleton pattern allows to create only one instance from
    the class, an ``__init__`` method would be called once with args and
    kwargs passed at the first call. Arguments of all future calls would
    be completely ignored and would not impact the existing instance at all.

Unit testing
============

In your unit tests to run the methods of decorated classes in isolation
without instantiation the object (to avoid running a constructor code),
use the ``__wrapped__`` attribute of the wrapper object:

.. code-block::

    # your_module.py
    @singleton
    class YourClass:
        def your_method(self):
            ...

.. code-block::

    # tests.py
    class TestYourClass(TestCase):
        def test_your_method(self):
            obj = mock.MagicMock()
            YourClass.__wrapped__.your_method(obj)
            ...

This test runs a code of the ``your_method`` only using a mock object
as the ``self`` argument, so the test would be run in complete isolation
and would not depend on another pieces of your code including a constructor
method.
