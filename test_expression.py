"""Test class expression
"""
import unittest
import numpy as np
import expression as ep
import group as grp


class TestExpression(unittest.TestCase):
    """Test Expression.
    """

    def test_init(self):
        """ Test instance and print.
        """
        expr = ep.Expr("zero+one+x0+x1x2")
        self.assertTrue(isinstance(expr, ep.Expr))
        self.assertEqual(expr.__repr__(), "one+zero+x0+x1x2")

    def test_expression(self):
        """Test single expression.
        """
        expr = ep.Expr("zero")
        out = expr.get_all_out()
        self.assertEqual(np.bitwise_or.reduce(out), False)
        self.assertFalse(expr.test_balance())
        self.assertEqual(expr.get_pair_expr().__repr__(), "zero")

        expr = ep.Expr("one")
        out = expr.get_all_out()
        self.assertEqual(np.bitwise_or.reduce(out), True)
        self.assertFalse(expr.test_balance())
        self.assertEqual(expr.get_pair_expr().__repr__(), "one")

        expr = ep.Expr("x0")
        out = expr.get_all_out()
        self.assertTrue(
            (out == np.array([0]*128 + [1]*128, dtype=np.bool)).all())
        self.assertTrue(expr.test_balance())
        self.assertEqual(expr.get_pair_expr().__repr__(), "x7")

        expr = ep.Expr("x7")
        out = expr.get_all_out()
        self.assertTrue((out == np.array([0, 1]*128, dtype=np.bool)).all())
        self.assertTrue(expr.test_balance())
        self.assertEqual(expr.get_pair_expr().__repr__(), "x0")

        expr = ep.Expr("x1x2")
        out = expr.get_all_out()
        self.assertTrue((out == np.array(
            [0]*(2**5)*3 + [1]*(2**5) + [0]*(2**5)*3 + [1]*(2**5), dtype=np.bool)).all())
        self.assertFalse(expr.test_balance())
        self.assertEqual(expr.get_pair_expr().__repr__(), "x5x6")

        expr = ep.Expr("x1+x2")
        out = expr.get_all_out()
        self.assertTrue((out == np.array(
            [0]*(2**5) + [1]*(2**5)*2 + [0]*(2**5)*2 +
            [1]*(2**5)*2 + [0]*(2**5), dtype=np.bool)).all())
        self.assertTrue(expr.test_balance())
        self.assertEqual(expr.get_pair_expr().__repr__(), "x5+x6")

        expr1 = ep.Expr("x0+x1x2")
        expr2 = ep.Expr("x1+x2x3")
        expr_prod = expr1 * expr2
        print(expr_prod)
        self.assertEqual(str(expr_prod), "x0x1+x1x2+x0x2x3+x1x2x3")

    def test_expr_batch(self):
        """Test batch expressions.
        """
        list_exprs = [
            "x0+x1",
            "x1x2+x3",
            "x3x4+x5",
            "x0x1x2x3x4x5x6+x7"
        ]
        res_expr = []
        for expr in list_exprs:
            expr = ep.Expr(expr)
            res_expr.append(expr.get_all_out())
        res_expr = np.array(res_expr)

        expr_batch = ep.RegBatch(list_exprs)
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
        for expr in list_exprs:
            expr = ep.Expr(expr)
            res_expr.append(expr.get_all_out())
        res_expr = np.array(res_expr)

        expr_batch = ep.ExprBatch(list_exprs)
        res_expr_batch = expr_batch.run().numpy()
        print(res_expr == res_expr_batch)
        self.assertTrue((res_expr == res_expr_batch).all())

    def test_group(self):
        """Test group"""
        list_exprs = [
            "x4+x5x6+x5x7",
            "x5+x4x6+x4x7",
            "x6+x4x7+x5x7",
            "x7+x4x6+x5x6",
            "x0+x4+x1x2+x1x3",
            "x1+x5+x0x2+x0x3",
            "x2+x6+x0x3+x1x3",
            "x3+x7+x0x2+x1x2",
        ]
        group = grp.Group(list_exprs)
        self.assertFalse(group.test_permutation())

        list_exprs = [
            "x4+x4x5x6+x5x6x7",
            "x5+x5x6x7+x6x7x4",
            "x6+x6x7x4+x7x4x5",
            "x7+x7x4x5+x4x5x6",
            "x0+x4+x0x2x3+x1x2x3",
            "x1+x5+x0x1x3+x0x2x3",
            "x2+x6+x0x1x2+x0x1x3",
            "x3+x7+x0x1x2+x1x2x3",
        ]
        group = grp.Group(list_exprs)
        self.assertTrue(group.test_permutation())

    def test_group_batch(self):
        """Test batch group"""
        list_grps = [
            [
                "x4+x5x6+x5x7",
                "x5+x4x6+x4x7",
                "x6+x4x7+x5x7",
                "x7+x4x6+x5x6",
                "x0+x4+x1x2+x1x3",
                "x1+x5+x0x2+x0x3",
                "x2+x6+x0x3+x1x3",
                "x3+x7+x0x2+x1x2",
            ], [
                "x4+x4x5x6+x5x6x7",
                "x5+x5x6x7+x6x7x4",
                "x6+x6x7x4+x7x4x5",
                "x7+x7x4x5+x4x5x6",
                "x0+x4+x0x2x3+x1x2x3",
                "x1+x5+x0x1x3+x0x2x3",
                "x2+x6+x0x1x2+x0x1x3",
                "x3+x7+x0x1x2+x1x2x3",
            ]
        ]
        grp_batch = grp.GroupBatch(list_grps)
        res = (grp_batch.test_permutation())
        self.assertFalse(res[0])
        self.assertTrue(res[1])
