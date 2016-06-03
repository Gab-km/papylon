Papylon
=======

Papylon is a Python library for random testing of program properties.

.. image:: https://travis-ci.org/Gab-km/papylon.svg
    :target: https://travis-ci.org/Gab-km/papylon

.. image:: https://badge.fury.io/py/papylon.svg
    :target: https://badge.fury.io/py/papylon

Example
-------

We can write a simple property with Python code:

.. code-block:: python

  from papylon.prop import for_all
  from papylon.arbitrary import arb_list, arb_int
  from papylon.checker import check

  # reversed and reversed list is the same of the original list
  p1 = for_all([arb_list(arb_int(), max_length=20)],
               lambda x: list(reversed(list(reversed(x)))) == x)
  check(p1)

When we run the script above, we can see the result as following:

.. code-block:: text

  OK, passed 100 tests.

If a property failed, Papylon reports which arbitrary(s) made it failed:

.. code-block:: python

  import math

  p2 = for_all([arb_int()], lambda n: math.sqrt(n*n) == n)
  check(p2)

.. code-block:: text

  Falsified after 2 tests (31 shrinks):
  > [-1]
