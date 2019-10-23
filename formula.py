#simple example
variable_count = 4

clauses = [
    lambda x1, x2, x3, x4: not x1 or x2 or x4,
    lambda x1, x2, x3, x4: not x2 or x3 or x4,
    lambda x1, x2, x3, x4: x1 or not x3 or x4,
    lambda x1, x2, x3, x4: x1 or not x2 or not x4,
    lambda x1, x2, x3, x4: x2 or not x3 or not x4,
    lambda x1, x2, x3, x4: not x1 or x3 or not x4,
    lambda x1, x2, x3, x4: x1 or x2 or x3,
]

clauses_count = len(clauses)

