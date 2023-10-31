pub struct Lexer {
    content: Vec<String>,
    line: u32,
    indent: u32,
    total_lines: u32,
}

impl Lexer {

    pub fn new(content: &str) -> Self {
        let newline_braces = content.replace("{", "\n{\n").replace("}", "\n}\n");
        let newlines: Vec<String> = newline_braces.to_owned().split("\n").map(|s| s.to_owned()).collect();
        let total_lines = newlines.clone().len() as u32;
        Lexer {
            content: newlines.clone(),
            line: 0,
            indent: 0,
            total_lines,
        }
    }

}

impl Iterator for Lexer {
    type Item = String;

    fn next(&mut self) -> Option<Self::Item> {
        if self.line >= self.total_lines {
            return None;
        }

        let line = &self.content[self.line as usize];
        self.line += 1;
        Some(line.to_string())
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.total_lines - self.line;
        (remaining as usize, Some(remaining as usize))
    }
}

