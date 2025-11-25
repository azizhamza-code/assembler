class Parser:
    def __init__(self, file_stream:str):
        self.text = _open_file_to_be_parsed(file_stream)
        self.buffer = _get_buffer_version(self.text)
        self.current_instructions=''

    
    def has_more_lignes(self.text):
        return self.buffer_reader.peek() != b''

    def advance(self):
        current_line:str = read_line()
        its_comment = current_line.startwith("//")
        its_space = current_line.contain(" ")
        self.current_instructions = next(buffer)

    @staticmethod
    def _get_buffer_version(text:io.TextIOBase)->io.BufferedReader:
        return io.BufferedReader(io.BytesIO(file.getvalue().encode("utf-8")))

    @staticmethod
    def _open_file_to_be_parsed(file_stream:str)-> :
            with open(file_stream, "r",  encoding="utf-8") as f:
                read_data = f.read()
            return read_data




