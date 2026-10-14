
def assembler(parser, code, dist):
    dist = open(dist, 'w')
    while parser.has_more_lignes():
        current_instruction_type = parser.instruction_type
        if current_instruction_type == "A_INSTRUCTION":
            dist.write(format(int(parser.symbol()), "016b"))
            dist.write("\n")
        elif current_instruction_type == "C_INSTRUCTION":
            contain_a = "M" in parser.comp()
            dist.write(
                    "111"+ str(contain_a * 1) + code.comp(
                        parser.comp()
                        ) + code.dest(
                            parser.dest()
                            ) + code.jump(
                                parser.jump()
                            )
                )
            dist.write("\n")
        parser.advance()

if __name__ == "__main__":

    from code_ import code
    from parser import Parser
    import argparse 

    parser = argparse.ArgumentParser()
    parser.add_argument("source_path")
    parser.add_argument("dest_path")
    args = parser.parse_args()
    source_path = args.source_path
    dist_path = args.dest_path
    parser = Parser(source_path)
    code = code()
    assembler(parser, code, dist_path)
