use std::{fs::File, io::Read};
use clap::Parser;
use whitesmiths_linter_rs::lexer::Lexer;

#[derive(Parser, Debug)]
struct Args {
    #[clap(value_name = "FILE")]
    file: String,
}

fn main() {

    let args = Args::parse();

    println!("File: {}", args.file);

    let mut fobj = match File::open(args.file) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    };

    let mut buffer = String::new();
    fobj.read_to_string(&mut buffer).unwrap();

    let lxr = Lexer::new(buffer.as_str());

    for i in lxr {
        println!("{}", i);
    }

}

