from unittest import TestCase
import types_checker as tc


class TestNode(TestCase):
    def test_check(self):
        n = tc.Node(str)
        self.assertTrue(n == "", "str")
        self.assertFalse(n == 1, "int")
        n = tc.Node(tc.Node(str))
        self.assertTrue(n == "", "node str")
        self.assertFalse(n == 1, "node int")

    def test__check(self):
        self.assertTrue(tc.Node._check("", str), "str")
        self.assertFalse(tc.Node._check("", int), "int")
        self.assertTrue(tc.Node._check("", tc.Node(str)), "node str")
        self.assertFalse(tc.Node._check("", tc.Node(int)), "node int")


class TestObjectTypeNode(TestCase):
    def test__check(self):
        self.assertTrue(tc.ObjectTypeNode._check("", ""), "str")
        self.assertFalse(tc.ObjectTypeNode._check("", 1), "int")
        self.assertTrue(tc.ObjectTypeNode._check("", tc.ObjectTypeNode("")), "obj node str")
        self.assertFalse(tc.ObjectTypeNode._check("", tc.ObjectTypeNode(1)), "obj node int")

    def test_check(self):
        n = tc.ObjectTypeNode("")
        self.assertTrue(n == "", "str")
        self.assertFalse(n == 1, "int")
        n = tc.ObjectTypeNode(tc.ObjectTypeNode(""))
        self.assertTrue(n == "", "node str")
        self.assertFalse(n == 1, "node int")


class TestSubClassNode(TestCase):
    def test__check(self):
        self.fail()

    def test_check(self):
        self.fail()
