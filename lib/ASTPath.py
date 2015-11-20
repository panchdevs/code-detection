#!/usr/bin/python

import ast

class ASTPath:

  def __init__(self, file_path):
    self.file_path = file_path

    with open(file_path) as code_file:
      code_lines = code_file.readlines()

    code = "".join(code_lines)

    self.paths = self.get_paths(code)

  @staticmethod
  def get_paths(code):
    code_ast = ast.parse(code)
    
    paths = []
    ASTPath.build_paths(code_ast, paths, "")

    return paths

  @staticmethod
  def build_paths(node, paths, path_so_far):
    for field in ast.iter_fields(node):
      if(field[0] != 'body'):
        path_so_far += Mapping(field[0])
        path_so_far += Mapping(type(field[1]).__name__)

    for child_node in ast.iter_child_nodes(node):
      ASTPath.build_paths(child_node, paths, path_so_far)

    if path_so_far:
      paths.append(path_so_far)


def Mapping(word):
  d = {'Module': 'a', 'Interactive': 'b', 'Expression': 'c', 'Suite': 'd',
  'FuntionDef': 'e', 'AsyncFunctionDef': 'f', 'ClassDef': 'g', 'Return': 'h',
  'Delete': 'i', 'Assign': 'j', 'AugAssign': 'k', 'For': 'l', 'AsyncFor': 'm',
  'While': 'n', 'If': 'o', 'With': 'p', 'AsyncWith': 'q', 'Raise': 'r',
  'Try': 's', 'Assert': 't', 'Import': 'u', 'ImportFrom': 'v', 'Global': 'w',
  'Nonlocal': 'x', 'Expr': 'y', 'Pass': 'z', 'Break': 'a1', 'Continue': 'b1',
  'BoolOp': 'c1', 'BinOp': 'd1', 'UnaryOp': 'e1', 'Lambda': 'f1', 'IfExp': 'g1',
  'Dict': 'h1', 'Set': 'i1', 'ListComp': 'j1', 'SetComp': 'k1', 'DictComp': 'l1',
  'GeneratorExp': 'm1', 'Await': 'n1', 'Yield': 'o1', 'YieldFrom': 'p1', 'Compare': 'q1',
  'Call': 'r1', 'Num': 's1', 'Str': 't1', 'Bytes': 'u1', 'NameConstant': 'v1',
  'Ellipses': 'w1', 'Attribute': 'x1', 'Subscript': 'y1', 'Starred': 'z1', 'Name': 'a2',
  'List': 'b2', 'Tuple': 'c2', 'Load': 'd2', 'Store': 'e2', 'Del': 'f2', 
  'AugLoad': 'g2', 'AugStore': 'h2', 'Param': 'i2', 'Slice': 'j2', 'ExtSlice': 'k2',
  'Index': 'l2', 'And': 'm2', 'Add': 'n2', 'Sub': 'o2', 'Mult': 'p2', 'MatMult': 'q2',
  'Div': 'r2', 'Mod': 's2', 'Pow': 't2', 'LShift': 'u2', 'RShift': 'v2', 'BitOr': 'w2',
  'BitXor': 'x2', 'BitAnd': 'y2', 'FloorDiv': 'z2', 'Invert': 'a3', 'Not': 'b3',
  'UAdd': 'c3', 'USub': 'd3', 'Or': 'e3', 'Eq': 'f3', 'NotEq': 'g3', 'Lt': 'h3',
  'LtE': 'i3', 'Gt': 'j3', 'GtE': 'k3', 'Is': 'l3', 'IsNot': 'm3', 'In': 'n3',
  'NotIn': 'o3', 'ExceptHandler': 'p3', 'body': 'q3', 'name': 'r3', 'args': 's3',
  'decorator_list': 't3', 'returns': 'u3', 'bases': 'v3', 'keywords': 'w3', 'value': 'x3',
  'targets': 'y3', 'op': 'z3', 'iter': 'a4', 'orelse': 'b4', 'test': 'c4', 'items': 'd4',
  'exc': 'e4', 'cause': 'f4', 'handlers': 'g4', 'finalbody': 'h4', 'msg': 'i4', 'names': 'j4',
  'module': 'k4', 'level': 'l4', 'lineno': 'm4', 'col_offset': 'n4', 'values': 'o4',
  'left': 'p4', 'right': 'q4', 'operand': 'r4', 'keys': 's4', 'elts': 't4', 'generators': 'u4',
  'elt': 'v4', 'comparators': 'w4', 'func': 'x4', 'n' : 'y4', 's': 'z4', 'attr': 'a5', 
  'ctx': 'b5', 'slice': 'c5', 'id': 'd5', 'lower': 'e5', 'upper': 'f5', 'step': 'g5',
  'dims': 'h5', 'target': 'i5', 'ifs': 'j5', 'vararg': 'k5', 'kwonlyargs': 'l5',
  'kw_defaults': 'm5', 'kwarg': 'n5', 'defaults': 'o5', 'arg': 'p5', 'annotation': 'q5',
  'asname': 'r5', 'context_expr': 's5', 'optional_vars': 't5','asname': 'r5',
  'context_expr': 's5', 'optional_vars': 't5', 'list': 'u5', 'str': 'v5', 'NoneType': 'w5',
  'starargs': 'x5', 'kwargs': 'y5', 'arguments': 'z5', 'varargannotation': 'a6', 
  'kwargannotation': 'b6', 'ops': 'c6', 'int': 'd6', 'float': 'e6', 'type': 'f6', 'key': 'g6',
  'complex': 'h6'}

  return d[word]