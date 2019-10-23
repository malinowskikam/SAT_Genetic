def parse(input_filename,output_filename='generated.py'):
    input_file = open(input_filename, "r")

    problem_defined=False
    arg_count = 0
    clause_count = 0
    lambdas = []
    line_n = 0
    for line in input_file:
        words = line[:-1].split(' ')

        if words[0].lower() == 'c':
            line_n += 1
            continue

        elif words[0].lower() == 'p':
            if words[1].lower() == 'cnf':
                arg_count = int(words[2])
                clause_count = int(words[3])
                problem_defined = True
            else:
                raise ValueError("Unsupported input type: " + words[1])

        else:
            if words[-1] != '0':
                raise ValueError('Line not ended with "0" (' + str(line_n) + ',' + words[-1] + ')')
            else:
                lambda_string = "lambda x:"
                variable_number = int(words[0])
                if variable_number < 0:
                    lambda_string += ' not x[' + str(-variable_number-1) + ']'
                elif variable_number > 0:
                    lambda_string += ' x[' + str(variable_number-1) + ']'
                else:
                    raise ValueError('"0" within a clause')

                for word in words[1:-2]:
                    if word != '':
                        variable_number = int(word)
                        if variable_number < 0:
                            lambda_string += ' or not x[' + str(-variable_number-1) + ']'
                        elif variable_number > 0:
                            lambda_string += ' or x[' + str(variable_number-1) + ']'
                        else:
                            raise ValueError('"0" within a clause')

                lambda_string += ','
                lambdas.append(lambda_string)
        line_n += 1

    input_file.close()
    output_file = open(output_filename, "w")

    output_file.write("# generated with cnf input file parser\n")

    output_file.write("variable_count = " + str(arg_count) + "\n")
    output_file.write("\n")
    output_file.write("clauses = [\n")

    for lambda_string in lambdas:
        output_file.write("    " + lambda_string + '\n')

    output_file.write("]\n")
    output_file.write("\n")
    output_file.write("clause_count = len(clauses)\n")

    output_file.close()


parse("example2.cnf")
