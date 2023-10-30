pub struct Lexer<'a> {
    content: Vec<&'a str>,
    line: u32,
    indent: u32,
    total_lines: u32,
}

impl<'a> Lexer<'a> {

    pub fn new(content: &'a str) -> Self {
        let newlines: Vec<&str> = content.split("\n").collect::<Vec<&str>>().clone();
        Lexer {
            content: newlines.clone(),
            line: 0,
            indent: 0,
            total_lines: newlines.len() as u32,
        }
    }

}

impl<'a> Iterator for Lexer<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        if self.line >= self.total_lines {
            return None;
        }

        let line = self.content[self.line as usize];
        self.line += 1;
        Some(line)
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.total_lines - self.line;
        (remaining as usize, Some(remaining as usize))
    }
}

