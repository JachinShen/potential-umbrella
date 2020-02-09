"""
Test class expression
"""
import unittest
import numpy as np
import expression as expr
import group as grp


class TestExpression(unittest.TestCase):
    """
    Test Expression
    """

    def test_init(self):
        """
        Test instance and print
        """
        e = expr.Expr("zero+one+x0+x1x2")
        self.assertTrue(isinstance(e, expr.Expr))
        self.assertEqual(e.__repr__(), "one + zero + x0 + x1 x2")

    def test_expression(self):
        """Test"""
        e = expr.Expr("zero")
        out = e.get_all_out()
        self.assertEqual(np.bitwise_or.reduce(out), False)
        self.assertFalse(e.test_balance())
        self.assertEqual(e.get_pair_expr().__repr__(), "zero")

        e = expr.Expr("one")
        out = e.get_all_out()
        self.assertEqual(np.bitwise_or.reduce(out), True)
        self.assertFalse(e.test_balance())
        self.assertEqual(e.get_pair_expr().__repr__(), "one")

        e = expr.Expr("x0")
        out = e.get_all_out()
        self.assertTrue(
            (out == np.array([0]*128 + [1]*128, dtype=np.bool)).all())
        self.assertTrue(e.test_balance())
        self.assertEqual(e.get_pair_expr().__repr__(), "x7")

        e = expr.Expr("x7")
        out = e.get_all_out()
        self.assertTrue((out == np.array([0, 1]*128, dtype=np.bool)).all())
        self.assertTrue(e.test_balance())
        self.assertEqual(e.get_pair_expr().__repr__(), "x0")

        e = expr.Expr("x1x2")
        out = e.get_all_out()
        self.assertTrue((out == np.array(
            [0]*(2**5)*3 + [1]*(2**5) + [0]*(2**5)*3 + [1]*(2**5), dtype=np.bool)).all())
        self.assertFalse(e.test_balance())
        self.assertEqual(e.get_pair_expr().__repr__(), "x5 x6")

        e = expr.Expr("x1+x2")
        out = e.get_all_out()
        self.assertTrue((out == np.array(
            [0]*(2**5) + [1]*(2**5)*2 + [0]*(2**5)*2 +
            [1]*(2**5)*2 + [0]*(2**5), dtype=np.bool)).all())
        self.assertTrue(e.test_balance())
        self.assertEqual(e.get_pair_expr().__repr__(), "x5 + x6")

    def test_expr_batch(self):
        """
        Test cases
        """
        list_exprs = [
            "x0+x1",
            "x1x2+x3",
            "x3x4+x5",
            "x0x1x2x3x4x5x6+x7"
        ]
        res_expr = []
        for e in list_exprs:
            e = expr.Expr(e)
            res_expr.append(e.get_all_out())
        res_expr = np.array(res_expr)

        expr_batch = expr.RegBatch(list_exprs)
        res_expr_batch = expr_batch.run().numpy()
        self.assertTrue((res_expr == res_expr_batch).all())

        list_exprs = [
            "x1",
            "x0+x2",
            "x1x2+x3x4+x5x6",
            "x5",
            "x1x2+x3",
            "x0+x1x2+x3x4x5"
        ]
        res_expr = []
        for e in list_exprs:
            e = expr.Expr(e)
            res_expr.append(e.get_all_out())
        res_expr = np.array(res_expr)

        expr_batch = expr.ExprBatch(list_exprs)
        res_expr_batch = expr_batch.run().numpy()
        print(res_expr == res_expr_batch)
        self.assertTrue((res_expr == res_expr_batch).all())

    def test_group(self):
        """Test"""
        list_exprs = [
            "x4+x5x6+x5x7",
            "x5+x4x6+x4x7",
            "x6+x4x7+x5x7",
            "x7+x4x6+x5x6"
        ]
        g = grp.Group(list_exprs)
        self.assertFalse(g.test_permutation())

        list_exprs = [
            "x4+x4x5x6+x5x6x7",
            "x5+x5x6x7+x6x7x4",
            "x6+x6x7x4+x7x4x5",
            "x7+x7x4x5+x4x5x6"
        ]
        g = grp.Group(list_exprs)
        self.assertTrue(g.test_permutation())

    def test_group_batch(self):
        """Test"""
        list_grps = [
            [
                "x4+x5x6+x5x7",
                "x5+x4x6+x4x7",
                "x6+x4x7+x5x7",
                "x7+x4x6+x5x6",
            ], [
                "x4+x4x5x6+x5x6x7",
                "x5+x5x6x7+x6x7x4",
                "x6+x6x7x4+x7x4x5",
                "x7+x7x4x5+x4x5x6"
            ]
        ]
        grp_batch = grp.GroupBatch(list_grps)
        res = (grp_batch.test_permutation())
        self.assertFalse(res[0])
        self.assertTrue(res[1])
