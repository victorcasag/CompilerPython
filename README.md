# Python Compiler

## Overview
This project is a compiler developed in Python for the UNESC compiler course, based on a specific grammar for processing and translating code written in a defined programming language. The goal is to create a tool capable of reading, interpreting, and compiling source code written according to the provided grammar, producing an appropriate output.

## Project Structure

### Grammar
The grammar used to define the syntax of the supported language is as follows:

- PROGRAMA ::= program ident ; DECLARACOES BLOCO .
- DECLARACOES ::= CONSTANTES VARIAVEIS PROCEDIMENTOS
- CONSTANTES ::= const ident = nint ; CONSTANTES
- VARIAVEIS ::= var LISTAVARIAVEIS : TIPO ; LDVAR
- PROCEDIMENTOS ::= procedure ident PARAMETROS ; BLOCO ; PROCEDIMENTOS
- BLOCO ::= begin COMANDOS end
- COMANDOS ::= COMANDO ; COMANDOS


The grammar specifies the structure of the code, including declarations of constants, variables, and procedures, as well as control flow commands such as `if`, `for`, `while`, and `repeat`.

### Data Types
The language supports the following data types:

- `integer`: integer numbers
- `real`: real numbers
- `string`: character strings

### Commands and Structures
The main commands and control structures include:

- **Input Data**: `read(ident)`
- **Output Data**: `print { ITEMSAIDA }`
- **Conditional Structures**: `if EXPRELACIONAL then BLOCO ELSEOPC`
- **Loops**: 
  - `while EXPRELACIONAL do BLOCO`
  - `for ident := EXPRESSAO to EXPRESSAO do BLOCO`
  - `repeat COMANDOS until EXPRELACIONAL`

### Usage Examples

#### Example 1: Simple Program

```text
program sum;
var a, b: integer;
begin
  a := 5;
  b := 10;
  print { a + b }
end.
```
### Requirements

To run the compiler, you need:

- Python 3.x

## Contribution

Feel free to contribute improvements and fixes. To report issues or suggest new features, please open an [issue](link-to-issues) or submit a pull request.

## License

This project is licensed under the [MIT License](link-to-license).
