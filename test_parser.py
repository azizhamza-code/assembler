from parser import Parser
from unittest.mock import mock_open, patch
from io import StringIO
from pathlib import Path

TEST_ASM = Path(__file__).parent / "test.asm"


def test_parser_init(path_file):

    m = mock_open(read_data="hello")

    with patch("builtins.open", m):

        parser = Parser("dummy.txt")

        parser.f = StringIO("a=d\n@A")

        assert parser.instruction_type== "C_INSTRUCTION"

        assert parser.dest() == "a"
        
        assert parser.comp() == "d"

        assert parser.has_more is True

        print(parser._current())

        parser.advance()

        print(parser._current())

        assert parser.instruction_type== "A_INSTRUCTION"

        assert parser.has_more is True

        assert parser.symbol() == 'A'

        parser.advance()

        assert parser.has_more is False


def test_parser_asm():
    parser = Parser(str(TEST_ASM))

    assert parser.instruction_type == "A_INSTRUCTION"
    assert parser.symbol() == "1"
    parser.advance()

    assert parser.instruction_type == "C_INSTRUCTION"
    assert parser.dest() == "D"
    assert parser.comp() == "A"
    parser.advance()

    assert parser.instruction_type == "A_INSTRUCTION"
    assert parser.symbol() == "0"
    parser.advance()

    assert parser.instruction_type == "C_INSTRUCTION"
    assert parser.dest() == "M"
    assert parser.comp() == "D"
    parser.advance()

    assert parser.instruction_type == "A_INSTRUCTION"
    assert parser.symbol() == "6"
    parser.advance()

    assert parser.instruction_type == "C_INSTRUCTION"
    assert parser.dest() is None
    assert parser.comp() == "0"
    print(parser.jump())
    assert parser.jump() == "JMP"
    parser.advance()

    assert parser.has_more is False


def test_parser_asm_print():
    parser = Parser(str(TEST_ASM))

    print(parser._current())

        
if __name__ == '__main__':
    test_parser_asm()