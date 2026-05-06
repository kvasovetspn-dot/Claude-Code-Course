"""
Advanced unit tests for oop_tasks.py.
Run:  python -m pytest test_oop_tasks.py -v
  or: python -m unittest test_oop_tasks -v
"""

import math
import unittest
import inspect
from io import StringIO
from abc import ABC
from unittest.mock import patch

from oop_tasks import (
    Shape, Circle, Rectangle, Triangle,
    BankAccount, SavingsAccount, CheckingAccount,
    Animal, Dog, Cat, Bird, make_all_speak,
    Book, Library,
    Stack,
)


# =============================================================================
# Task 1 — Shape Hierarchy
# =============================================================================

class TestShapeAbstraction(unittest.TestCase):
    def test_shape_is_abstract(self):
        self.assertTrue(inspect.isabstract(Shape))

    def test_shape_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Shape()  # type: ignore

    def test_shape_has_abstract_area(self):
        self.assertIn("area", Shape.__abstractmethods__)

    def test_shape_has_abstract_perimeter(self):
        self.assertIn("perimeter", Shape.__abstractmethods__)

    def test_all_shapes_are_subclasses(self):
        for cls in (Circle, Rectangle, Triangle):
            with self.subTest(cls=cls):
                self.assertTrue(issubclass(cls, Shape))


class TestCircle(unittest.TestCase):
    def setUp(self):
        self.c = Circle(5)

    def test_area(self):
        self.assertAlmostEqual(self.c.area(), math.pi * 25, places=9)

    def test_perimeter(self):
        self.assertAlmostEqual(self.c.perimeter(), 10 * math.pi, places=9)

    def test_unit_circle(self):
        c = Circle(1)
        self.assertAlmostEqual(c.area(), math.pi)
        self.assertAlmostEqual(c.perimeter(), 2 * math.pi)

    def test_str_contains_class_name(self):
        self.assertIn("Circle", str(self.c))

    def test_str_contains_area_and_perimeter(self):
        s = str(self.c)
        self.assertIn("area=", s)
        self.assertIn("perimeter=", s)

    def test_isinstance_shape(self):
        self.assertIsInstance(self.c, Shape)


class TestRectangle(unittest.TestCase):
    def setUp(self):
        self.r = Rectangle(4, 6)

    def test_area(self):
        self.assertEqual(self.r.area(), 24.0)

    def test_perimeter(self):
        self.assertEqual(self.r.perimeter(), 20.0)

    def test_square(self):
        sq = Rectangle(3, 3)
        self.assertEqual(sq.area(), 9.0)
        self.assertEqual(sq.perimeter(), 12.0)

    def test_str_contains_class_name(self):
        self.assertIn("Rectangle", str(self.r))

    def test_isinstance_shape(self):
        self.assertIsInstance(self.r, Shape)


class TestTriangle(unittest.TestCase):
    def setUp(self):
        self.t = Triangle(3, 4, 5)  # right triangle

    def test_area_right_triangle(self):
        self.assertAlmostEqual(self.t.area(), 6.0, places=9)

    def test_perimeter(self):
        self.assertEqual(self.t.perimeter(), 12.0)

    def test_equilateral(self):
        t = Triangle(2, 2, 2)
        expected_area = math.sqrt(3)
        self.assertAlmostEqual(t.area(), expected_area, places=9)

    def test_invalid_triangle_raises(self):
        with self.assertRaises(ValueError):
            Triangle(1, 2, 10)

    def test_degenerate_triangle_raises(self):
        with self.assertRaises(ValueError):
            Triangle(1, 2, 3)  # a+b == c, not strictly greater

    def test_str_contains_class_name(self):
        self.assertIn("Triangle", str(self.t))

    def test_isinstance_shape(self):
        self.assertIsInstance(self.t, Shape)


# =============================================================================
# Task 2 — Bank Account
# =============================================================================

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Alice", 500.0)

    def test_initial_balance(self):
        self.assertEqual(self.acc.balance, 500.0)

    def test_default_initial_balance_is_zero(self):
        acc = BankAccount("Bob")
        self.assertEqual(acc.balance, 0.0)

    def test_deposit_increases_balance(self):
        self.acc.deposit(200)
        self.assertAlmostEqual(self.acc.balance, 700.0)

    def test_withdraw_decreases_balance(self):
        self.acc.withdraw(100)
        self.assertAlmostEqual(self.acc.balance, 400.0)

    def test_withdraw_exact_balance(self):
        self.acc.withdraw(500)
        self.assertEqual(self.acc.balance, 0.0)

    def test_deposit_zero_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(0)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(-50)

    def test_withdraw_zero_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(0)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(-10)

    def test_overdraft_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(600)

    def test_balance_is_private(self):
        # Direct attribute access must go through name mangling
        self.assertFalse(hasattr(self.acc, "balance") and isinstance(
            type(self.acc).__dict__.get("balance"), float
        ))
        self.assertIn("_BankAccount__balance", self.acc.__dict__)

    def test_balance_is_read_only_property(self):
        with self.assertRaises(AttributeError):
            self.acc.balance = 9999  # type: ignore

    def test_str_contains_owner(self):
        self.assertIn("Alice", str(self.acc))


class TestSavingsAccount(unittest.TestCase):
    def setUp(self):
        self.acc = SavingsAccount("Alice", 1000.0, interest_rate=0.10)

    def test_is_subclass_of_bank_account(self):
        self.assertIsInstance(self.acc, BankAccount)

    def test_default_interest_rate(self):
        acc = SavingsAccount("Bob", 100)
        self.assertEqual(acc.interest_rate, 0.05)

    def test_apply_interest_increases_balance(self):
        self.acc.apply_interest()
        self.assertAlmostEqual(self.acc.balance, 1100.0)

    def test_apply_interest_twice(self):
        self.acc.apply_interest()
        self.acc.apply_interest()
        self.assertAlmostEqual(self.acc.balance, 1210.0)

    def test_inherits_deposit_and_withdraw(self):
        self.acc.deposit(500)
        self.acc.withdraw(200)
        self.assertAlmostEqual(self.acc.balance, 1300.0)


class TestCheckingAccount(unittest.TestCase):
    def setUp(self):
        self.acc = CheckingAccount("Bob", 50.0, overdraft_limit=100.0)

    def test_is_subclass_of_bank_account(self):
        self.assertIsInstance(self.acc, BankAccount)

    def test_withdraw_within_balance(self):
        self.acc.withdraw(30)
        self.assertAlmostEqual(self.acc.balance, 20.0)

    def test_withdraw_into_overdraft(self):
        self.acc.withdraw(120)
        self.assertAlmostEqual(self.acc.balance, -70.0)

    def test_withdraw_exactly_to_overdraft_limit(self):
        self.acc.withdraw(150)
        self.assertAlmostEqual(self.acc.balance, -100.0)

    def test_withdraw_beyond_overdraft_limit_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(151)

    def test_withdraw_negative_still_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(-5)

    def test_default_overdraft_limit(self):
        acc = CheckingAccount("Carol", 0)
        self.assertEqual(acc.overdraft_limit, 100.0)


# =============================================================================
# Task 3 — Animal Hierarchy
# =============================================================================

class TestAnimalAbstraction(unittest.TestCase):
    def test_animal_is_abstract(self):
        self.assertTrue(inspect.isabstract(Animal))

    def test_animal_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Animal("x", 1)  # type: ignore

    def test_animal_is_abc(self):
        self.assertTrue(issubclass(Animal, ABC))

    def test_speak_is_abstract(self):
        self.assertIn("speak", Animal.__abstractmethods__)

    def test_all_animals_are_subclasses(self):
        for cls in (Dog, Cat, Bird):
            with self.subTest(cls=cls):
                self.assertTrue(issubclass(cls, Animal))


class TestDog(unittest.TestCase):
    def setUp(self):
        self.dog = Dog("Rex", 3)

    def test_speak_contains_name(self):
        self.assertIn("Rex", self.dog.speak())

    def test_speak_contains_woof(self):
        self.assertIn("Woof", self.dog.speak())

    def test_str_contains_class_name(self):
        self.assertIn("Dog", str(self.dog))

    def test_str_contains_name_and_age(self):
        s = str(self.dog)
        self.assertIn("Rex", s)
        self.assertIn("3", s)

    def test_repr_equals_str(self):
        self.assertEqual(str(self.dog), repr(self.dog))


class TestCat(unittest.TestCase):
    def setUp(self):
        self.cat = Cat("Whiskers", 5)

    def test_speak_contains_name(self):
        self.assertIn("Whiskers", self.cat.speak())

    def test_speak_contains_meow(self):
        self.assertIn("Meow", self.cat.speak())


class TestBird(unittest.TestCase):
    def setUp(self):
        self.bird = Bird("Tweety", 2)

    def test_speak_contains_name(self):
        self.assertIn("Tweety", self.bird.speak())

    def test_speak_contains_tweet(self):
        self.assertIn("Tweet", self.bird.speak())


class TestMakeAllSpeak(unittest.TestCase):
    def test_all_animals_speak(self):
        animals = [Dog("D", 1), Cat("C", 2), Bird("B", 3)]
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            make_all_speak(animals)
            output = mock_out.getvalue()
        self.assertIn("Woof", output)
        self.assertIn("Meow", output)
        self.assertIn("Tweet", output)

    def test_empty_list_no_output(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            make_all_speak([])
            self.assertEqual(mock_out.getvalue(), "")

    def test_correct_number_of_lines(self):
        animals = [Dog("A", 1), Dog("B", 2), Cat("C", 3)]
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            make_all_speak(animals)
            lines = mock_out.getvalue().strip().splitlines()
        self.assertEqual(len(lines), 3)


# =============================================================================
# Task 4 — Library System
# =============================================================================

class TestBook(unittest.TestCase):
    def setUp(self):
        self.b1 = Book("1984", "George Orwell", 1949)
        self.b2 = Book("Brave New World", "Aldous Huxley", 1932)
        self.b3 = Book("Animal Farm", "George Orwell", 1945)

    def test_str_contains_title_author_year(self):
        s = str(self.b1)
        self.assertIn("1984", s)
        self.assertIn("George Orwell", s)
        self.assertIn("1949", s)

    def test_repr_contains_title(self):
        self.assertIn("1984", repr(self.b1))

    def test_eq_same_title_and_author(self):
        duplicate = Book("1984", "George Orwell", 2000)
        self.assertEqual(self.b1, duplicate)

    def test_eq_different_title(self):
        self.assertNotEqual(self.b1, self.b3)

    def test_eq_different_author(self):
        other = Book("1984", "Someone Else", 1949)
        self.assertNotEqual(self.b1, other)

    def test_eq_with_non_book_returns_not_implemented(self):
        result = self.b1.__eq__("not a book")
        self.assertEqual(result, NotImplemented)

    def test_lt_by_year(self):
        self.assertLess(self.b2, self.b3)  # 1932 < 1945
        self.assertLess(self.b3, self.b1)  # 1945 < 1949

    def test_sort_by_year(self):
        books = [self.b1, self.b2, self.b3]
        sorted_books = sorted(books)
        self.assertEqual(sorted_books, [self.b2, self.b3, self.b1])


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.lib = Library("Test Library")
        self.b1 = Book("1984", "George Orwell", 1949)
        self.b2 = Book("Brave New World", "Aldous Huxley", 1932)
        self.b3 = Book("Animal Farm", "George Orwell", 1945)

    def test_empty_library_len(self):
        self.assertEqual(len(self.lib), 0)

    def test_add_book_increases_len(self):
        self.lib.add_book(self.b1)
        self.assertEqual(len(self.lib), 1)

    def test_add_multiple_books(self):
        for b in (self.b1, self.b2, self.b3):
            self.lib.add_book(b)
        self.assertEqual(len(self.lib), 3)

    def test_remove_book_decreases_len(self):
        self.lib.add_book(self.b1)
        self.lib.remove_book(self.b1)
        self.assertEqual(len(self.lib), 0)

    def test_remove_nonexistent_raises(self):
        with self.assertRaises(ValueError):
            self.lib.remove_book(self.b1)

    def test_contains_added_book(self):
        self.lib.add_book(self.b1)
        self.assertIn(self.b1, self.lib)

    def test_not_contains_removed_book(self):
        self.lib.add_book(self.b1)
        self.lib.remove_book(self.b1)
        self.assertNotIn(self.b1, self.lib)

    def test_find_by_author_returns_correct_books(self):
        for b in (self.b1, self.b2, self.b3):
            self.lib.add_book(b)
        results = self.lib.find_by_author("George Orwell")
        self.assertIn(self.b1, results)
        self.assertIn(self.b3, results)
        self.assertNotIn(self.b2, results)

    def test_find_by_author_case_insensitive(self):
        self.lib.add_book(self.b1)
        self.assertEqual(self.lib.find_by_author("george orwell"), [self.b1])
        self.assertEqual(self.lib.find_by_author("GEORGE ORWELL"), [self.b1])

    def test_find_by_author_no_match_returns_empty(self):
        self.lib.add_book(self.b1)
        self.assertEqual(self.lib.find_by_author("Unknown Author"), [])

    def test_str_contains_library_name(self):
        self.assertIn("Test Library", str(self.lib))


# =============================================================================
# Task 5 — Stack
# =============================================================================

class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())

    def test_push_makes_non_empty(self):
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())

    def test_len_empty(self):
        self.assertEqual(len(self.stack), 0)

    def test_len_after_pushes(self):
        self.stack.push("a")
        self.stack.push("b")
        self.assertEqual(len(self.stack), 2)

    def test_peek_returns_top(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.peek(), 20)

    def test_peek_does_not_remove(self):
        self.stack.push(42)
        self.stack.peek()
        self.assertEqual(len(self.stack), 1)

    def test_pop_returns_top(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.pop(), 20)

    def test_pop_removes_element(self):
        self.stack.push(1)
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    def test_lifo_order(self):
        for v in [1, 2, 3]:
            self.stack.push(v)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)

    def test_pop_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_iter_top_to_bottom(self):
        for v in [1, 2, 3]:
            self.stack.push(v)
        self.assertEqual(list(self.stack), [3, 2, 1])

    def test_iter_empty(self):
        self.assertEqual(list(self.stack), [])

    def test_push_mixed_types(self):
        self.stack.push(1)
        self.stack.push("hello")
        self.stack.push([1, 2, 3])
        self.assertEqual(len(self.stack), 3)
        self.assertEqual(self.stack.pop(), [1, 2, 3])

    def test_str_contains_stack(self):
        self.assertIn("Stack", str(self.stack))

    def test_data_is_encapsulated(self):
        # Internal list must not be directly accessible as a public attribute
        self.assertFalse(hasattr(self.stack, "data"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
