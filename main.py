from sys import argv
from re import search, sub
en, keywords = [chr(i) for i in list(range(65, 91)) + list(range(97, 123))], eval(open('lang.json').read())  # Do not support latin languages, it has all the built-in keywords except Inheritances of Exception and swapcase
def rep(line: str) -> tuple:
    gr = []
    while s := search(r"\".*?(?<!\\)\"", line):  # Only support " not '
        line = sub(s.group(), "%s", line, 1)
        gr.append(s.group())
    return tuple(gr), line
def exact(partials: list) -> float:
    n = len(partials) - 1
    hi = partials[n]
    n -= 1
    diff = 0
    while n:
        x = hi
        y = partials[n]
        n -= 1
        hi = x + y
        yr = hi - x
        diff = y - yr
        if diff != 0: break
    if n * diff * partials[n - 1] > 0:
        y = diff * 2
        x = hi + y
        yr = x - hi
        if y == yr: return x
    return hi
def _sum(iterable: list) -> float:  # Why? try print(_sum([0.1]*100)) and print(sum([0.1]*100))
    partials = []
    for x in iterable:
        i = 0
        for y in partials:
            if abs(x) < abs(y): x, y = y, x
            hi = x + y
            lo = y - (hi - x)
            if lo:
                partials[i] = lo
                i += 1
            x = hi
        partials[i:] = [x]
    return exact(partials) if partials else 0
def _exec(line: str) -> None:
    gr, line = rep(line)
    flag = True
    for i in range(len(line)):
        if line[i] in en and line[i - 1: i + 1] != "%s" and "#" not in line[:i] and flag:
            print(f"You need to use only {keywords['lang']} keywords")
            flag = False
    if flag:
        for i in keywords: line = line.replace(i, keywords[i])
        line, e = line.replace("exec", "_exec").replace("sum", "_sum") % gr, None
        try: e = eval(line)
        except:
            try: exec(line, globals())
            except BaseException as e: print(e)
        else:
            if e is not None: print(e)
while len(argv) == 1: _exec(input(">>> "))
if len(argv) != 1:
    try: text, newline = open(' '.join(argv[1:])).read(), "\n"
    except: _exec(' '.join(argv[1:]))
    else:
        groups, text = rep(text)
        for i in range(len(text)):
            if text[i] in en and text[i - 1: i + 1] != "%s" and "#" not in text[text[:i].rfind("\n"): i]: raise SyntaxError(f"In line {text[: i].count(newline)} you need to use only {keywords['lang']} keywords")
        for i in keywords: text = text.replace(i, keywords[i])
        exec(text.replace("exec", "_exec").replace("sum", "_sum") % groups)
# lang.json is written to be compatible with Hebrew, but it can be done in every non-latin language
