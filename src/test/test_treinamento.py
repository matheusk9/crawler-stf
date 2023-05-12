from src.modules.testes import soma_iteravel
import unittest
from fractions import Fraction


class TestTreinamento(unittest.TestCase):
    """Doc."""

    def test_soma(self):
        """Doc."""

        lista = [1, 4]
        a = 5
        total = soma_iteravel(lista)
        self.assertEqual(a, total)

    def test_fracao(self):
        """Doc"""
        
        lista = [Fraction(1,4), Fraction(1,4), Fraction(2,5)]
        total = soma_iteravel(lista)
        self.assertEqual(total, 1)