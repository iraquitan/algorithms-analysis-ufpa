# -*- coding: utf-8 -*-


def bmh(text, pattern, debug=False):
    # preprocess pattern
    text = "".join(text.split(" "))
    keys = {}
    m = len(pattern)
    for j in range(0, len(pattern) - 1):
        s = pattern[j]
        v = keys.get(s, None)
        if v:
            keys[s] = min(m - j - 1, v)
        else:
            keys[s] = min(m - j - 1, m)
    if debug:
        print(keys)
    step = 0
    while len(text) - step >= len(pattern):
        i = len(pattern) - 1
        if debug:
            print(f"step={step}\ti={i}")
        while text[step + 1] == pattern[i]:
            if i == 0:
                return step
            i -= 1
        step += keys.get(text[step + len(pattern) - 1], m)
    return False


if __name__ == '__main__':
    txt = "h badeca edcade"
    ptn = "cade"
    print(bmh(txt, ptn, debug=True))
