from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password: str


@dataclass
class Income:
    user_id: int
    income: str
    title: str
    created_at: str


@dataclass
class Expense:
    user_id: int
    expense: str
    title: str
    created_at: str


@dataclass
class Goal:
    user_id: int
    title: str
    money_count: str
    savings: str
