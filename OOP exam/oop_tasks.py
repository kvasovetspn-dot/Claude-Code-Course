"""
Classical OOP Tasks — Python Exam Solutions
Covers: abstraction, encapsulation, inheritance, polymorphism, magic methods.
"""

from abc import ABC, abstractmethod
import math


# =============================================================================
# Task 1 — Shape Hierarchy (Abstraction + Polymorphism)
# =============================================================================

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def __str__(self) -> str:
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides.")
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# =============================================================================
# Task 2 — Bank Account (Encapsulation + Inheritance)
# =============================================================================

class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0):
        self.owner = owner
        self.__balance = initial_balance

    @property
    def balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= amount

    def __str__(self) -> str:
        return f"{type(self).__name__}[{self.owner}]: ${self.__balance:.2f}"


class SavingsAccount(BankAccount):
    def __init__(self, owner: str, initial_balance: float = 0.0, interest_rate: float = 0.05):
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate

    def apply_interest(self) -> None:
        self.deposit(self.balance * self.interest_rate)


class CheckingAccount(BankAccount):
    def __init__(self, owner: str, initial_balance: float = 0.0, overdraft_limit: float = 100.0):
        super().__init__(owner, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Exceeds overdraft limit.")
        # bypass parent's check to allow overdraft
        self._BankAccount__balance -= amount


# =============================================================================
# Task 3 — Animal Hierarchy (Polymorphism + __str__)
# =============================================================================

class Animal(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @abstractmethod
    def speak(self) -> str: ...

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, age={self.age})"

    def __repr__(self) -> str:
        return self.__str__()


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Meow!"


class Bird(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Tweet!"


def make_all_speak(animals: list[Animal]) -> None:
    for animal in animals:
        print(animal.speak())


# =============================================================================
# Task 4 — Library System (Composition + Magic Methods)
# =============================================================================

class Book:
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self) -> str:
        return f'"{self.title}" by {self.author} ({self.year})'

    def __repr__(self) -> str:
        return f"Book({self.title!r}, {self.author!r}, {self.year})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title and self.author == other.author

    def __lt__(self, other: "Book") -> bool:
        return self.year < other.year


class Library:
    def __init__(self, name: str):
        self.name = name
        self._books: list[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def remove_book(self, book: Book) -> None:
        self._books.remove(book)

    def find_by_author(self, author: str) -> list[Book]:
        return [b for b in self._books if b.author.lower() == author.lower()]

    def __len__(self) -> int:
        return len(self._books)

    def __contains__(self, book: Book) -> bool:
        return book in self._books

    def __str__(self) -> str:
        return f"Library({self.name!r}, {len(self)} books)"


# =============================================================================
# Task 5 — Generic Stack (Iteration Protocol + Encapsulation)
# =============================================================================

class Stack:
    def __init__(self):
        self._data: list = []

    def push(self, item) -> None:
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack.")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty stack.")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return reversed(self._data)

    def __str__(self) -> str:
        return f"Stack(top -> {list(reversed(self._data))})"


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Task 1 — Shapes")
    print("=" * 50)
    shapes: list[Shape] = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
    for s in shapes:
        print(s)

    print("\n" + "=" * 50)
    print("Task 2 — Bank Accounts")
    print("=" * 50)
    savings = SavingsAccount("Alice", 1000, interest_rate=0.1)
    savings.apply_interest()
    print(savings)

    checking = CheckingAccount("Bob", 50, overdraft_limit=100)
    checking.withdraw(120)
    print(checking)

    print("\n" + "=" * 50)
    print("Task 3 — Animals")
    print("=" * 50)
    animals: list[Animal] = [Dog("Rex", 3), Cat("Whiskers", 5), Bird("Tweety", 2)]
    make_all_speak(animals)

    print("\n" + "=" * 50)
    print("Task 4 — Library")
    print("=" * 50)
    lib = Library("City Library")
    b1 = Book("1984", "George Orwell", 1949)
    b2 = Book("Brave New World", "Aldous Huxley", 1932)
    b3 = Book("Animal Farm", "George Orwell", 1945)
    for book in (b1, b2, b3):
        lib.add_book(book)
    print(lib)
    print("Orwell books:", lib.find_by_author("George Orwell"))
    print("1984 in library:", b1 in lib)
    print("Sorted by year:", sorted([b1, b2, b3]))

    print("\n" + "=" * 50)
    print("Task 5 — Stack")
    print("=" * 50)
    stack: Stack = Stack()
    for val in [10, 20, 30]:
        stack.push(val)
    print(stack)
    print("Peek:", stack.peek())
    print("Pop:", stack.pop())
    print("Iterate (top to bottom):", list(stack))
