# rfckit

Thing for generating fancy sequence diagrams from annotated RFCs / standards doc.

It's a:
- file format for sequence diagrams annotated with standards info
- html generator for sequence diagrams

The goal is to be able to read an RFC in the context of a sequence diagram.

The reach goal is to develop markup formats that can exist *within* RFCs so these diagrams are generated automatically from written specs.

## Example

There is a sample spec in this codebase for the oauth 2.0 authorization code grant (in samples/). Nobody has reviewed it and it may or may not be right. You can view the generated output for the [oauth 2.0 authorization flow](https://abe-winter.github.io/2022/01/23/oauth.html) (based on the [oauth sample spec](./samples/oauth.yml) in this repo).

## Who should use this

If you want to generate highly annotated sequence diagrams for your own projects, or if you're publishing or writing about an RFC, this may be for you.

## Docs

There are none -- file an issue if you want to use this and need help. But you can get started looking at oauth.yml and spec.py in this codebase.

To run the program, do something like:

```sh
direnv allow
pip install -r requirements.txt
# main.py defaults to samples/oauth.yml
./main.py > oauth.htm
xdg-open oauth.htm # (or `open` on a mac)
```
