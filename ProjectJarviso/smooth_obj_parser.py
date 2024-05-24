from pywavefront import Wavefront, ObjParser


class SmoothObjParser(ObjParser):
    def __init__(self, wavefront, file_name, *args, **kwargs):
        super().__init__(wavefront, file_name, *args, **kwargs)

    def parse(self):
        while True:
            try:
                self.next_line()
            except StopIteration:
                break

            if self.line.startswith('s '):
                # Skip smooth shading statement
                continue

            self._parse_line(self.line)

    def _parse_line(self, line):
        self.line = line.strip()
        self.values = self.line.split()
        if not self.values:
            return
        if self.values[0] in self.dispatcher:
            self.dispatcher[self.values[0]]()
        else:
            self.parse_fallback()


class CustomWavefront(Wavefront):
    def __init__(self, file_name, *args, **kwargs):
        self.parser_cls = SmoothObjParser
        super().__init__(file_name, *args, **kwargs)
