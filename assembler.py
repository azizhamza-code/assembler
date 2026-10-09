def assembler(parser, code, dist):
    while parser.has_morelines():
        current_line = parser.current_instruction
        code_bin = code.decode(current_line)
        dist.write(code_bin)
        parser.advance()

if __name__ == "__main__":
    //parse args
    source_path = args.source_path
    dist_path = args.dist_path

    
    parser = Parser(source_path)
    code = code()
    assembler(parser, code, dist)

