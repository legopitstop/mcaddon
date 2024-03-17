import py2js
import math

# pip install py2js
# pip install jsbeautifier
# pip install strinpy


@py2js.convert
def main():
    def test(a):
        return a == 5


print(main)
