import os
import ast
import numpy
from sys import argv

script, first, second = argv


class FirstTransform(ast.NodeTransformer):

    def visit_ClassDef(self, node):
        node.name = "class_name"
        return node


class SecondTransform(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        node.name = 'func_name'
        return node


class ThirdTransform(ast.NodeTransformer):
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            return None
        return node

    def visit_Name(self, node):
        return ast.Str('name')

    def visit_arg(self, node):
        if hasattr(node, 'annotation'):
            node.annotation = None
        return node

    def visit_AnnAssign(self, node):
        if hasattr(node, 'annotation'):
            node.annotation = None
        return node


def levenshtein(text1, text2):
    distances = numpy.zeros((len(text1) + 1, len(text2) + 1))

    for t1 in range(len(text1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(text2) + 1):
        distances[0][t2] = t2

    for t1 in range(1, len(text1) + 1):
        for t2 in range(1, len(text2) + 1):
            if text1[t1 - 1] == text2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(text1)][len(text2)]


def comparison(a, b):
    with open(a, "r") as a, open(b, "r") as b:
        first_tree = ast.parse(a.read())

        second_tree = ast.parse(b.read())
        t1 = FirstTransform()
        t2 = SecondTransform()
        t3 = ThirdTransform()

        t1.visit(first_tree)
        t2.visit(first_tree)
        t3.visit(first_tree)

        t1.visit(second_tree)
        t2.visit(second_tree)
        t3.visit(second_tree)
        return levenshtein(ast.unparse(first_tree), ast.unparse(second_tree)) / len(
            ast.unparse(first_tree))


with open(first, "r") as f1, open(second, "a") as f2:
    for line in f1.readlines():
        start, end = line.split()
        d = os.getcwd()
        f2.write(str(comparison(d + "\\" + start, d + "\\" + end)))
        f2.write("\n")
