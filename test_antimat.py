#import library for tests
import pytest

#Import antimat function
from antimat import is_mat

def test_mat_lower_t():
    assert is_mat("сука, Ты тупой") == True

def test_mat_lower_f():
    assert is_mat("привет, Ты тупой") == False

def test_mat_high_t():
    assert is_mat("сУка, Ты тупой") == True

def test_mat_high_t1():
    assert is_mat("FucK, Ты тупой") == True

def test_mat_high_t2():
    assert is_mat("fuck, Ты тупой") == True

def test_mat_high_t3():
    assert is_mat("Тебе жопа, Ты тупой") == True