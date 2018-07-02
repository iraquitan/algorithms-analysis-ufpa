# -*- coding: utf-8 -*-


def preprocess_pattern_bmh(pattern, k=1):
    keys = {}
    m = len(pattern)
    for j in range(0, len(pattern) - k):
        s = pattern[j]
        v = keys.get(s, None)
        if v:
            keys[s] = min(m - j - k, v)
        else:
            keys[s] = min(m - j - k, m)
    return keys


def bmh(text, pattern, blanks=True, debug=False):
    if not blanks:
        text = "".join(text.split(" "))
    # preprocess pattern
    keys = preprocess_pattern_bmh(pattern, k=1)
    m = len(pattern)
    if debug:
        print(keys)

    matches = []
    step = 0
    while (len(text) - step) >= m:
        i = m - 1
        # if debug:
            # print(f"len(text)-step={len(text)-step}"
            #       f"\tm={m}"
            #       f"\tstep={step}\ti={i}"
            #       f"\ttext[step+i]={text[step+i]}"
            #       f"\tpattern[i]={pattern[i]}")
        while text[step+i] == pattern[i]:
            if i == 0:
                matches.append(step)
                break
            i -= 1
        if debug:
            print(f"shift for key = {text[step+m-1]}")
        step += keys.get(text[step + m - 1], m)
    return matches


def bmhs(text, pattern, blanks=True, debug=False):
    if not blanks:
        text = "".join(text.split(" "))
    # preprocess pattern
    keys = preprocess_pattern_bmh(pattern, k=0)
    m = len(pattern)
    if debug:
        print(keys)

    matches = []
    step = 0
    while (len(text) - step) >= m:
        i = m - 1
            #
            # print(f"|{'texto':_^7}|{'(r>>1)|10^(m-1)':_^{max(m, 15)+2}}|{'r':_^{m+2}}|")
            # print(f"len(text)-step={len(text)-step}"
            #       f"\tm={m}"
            #       f"\tstep={step}\ti={i}"
            #       f"\ttext[step+i]={text[step+i]}"
            #       f"\tpattern[i]={pattern[i]}")
        while text[step+i] == pattern[i]:
            if i == 0:
                matches.append(step)
                break
            i -= 1
        if step + m >= len(text):
            break
        if debug:
            print(f"shift for key = {text[step+m]}")
        step += keys.get(text[step + m], m)
    return matches


def to_bin(n, width=32):
    "Pad a binary number to WIDTH bits wide"
    s = bin(n).replace("0b", "")
    return f"{int(s):0{width}d}"


def preprocess_pattern_shift_and(pattern):
    keys = {}
    for s in set(pattern):
        init_mask = [0] * len(pattern)
        for i, p in enumerate(pattern):
            if s == p:
                init_mask[i] = 1
        keys[s] = "".join([str(v) for v in init_mask])
    return keys


def shift_and(text, pattern, blanks=True, debug=False):
    if not blanks:
        text = "".join(text.split(" "))
    keys = preprocess_pattern_shift_and(pattern)
    if debug:
        print(keys)
    n = len(text)
    m = len(pattern)
    matches = []
    r = 0
    ones = int("1"+"0"*(m-1), 2)
    if debug:
        print(f"|{'texto':_^7}|{'(r>>1)|10^(m-1)':_^{max(m, 15)+2}}|{'r':_^{m+2}}|")
    for i in range(n):
        # expr = r >> 1 | 10**(m-1)
        expr = (r >> 1) | ones
        r = expr & int(keys.get(text[i], '0'), 2)
        if debug:
            print(f"|{text[i]:^7}|{to_bin(expr, m):^{max(m, 15)+2}}|{to_bin(r, m):^{m+2}}|")
        if r & (ones >> (m - 1)):
            match = i - m + 1
            matches.append(match)
    return matches


def shift_and2(text, pattern, trace=False):
    m = len(pattern)
    n = len(text)
    matches = []
    B = {}  # char -> bitmask table
    for i in range(m):
        B[pattern[i]] = (B.get(pattern[i], 0) | (1 << i))
    if trace:
        print(B)
    # search
    D = 0
    for i in range(n):
        D = ((D << 1) | 1) & (B.get(text[i], 0))
        if trace:
            print("%s & B[%c] : %s" % (
            to_bin(D, m), text[i], to_bin(B.get(text[i], 0), m)))
        if D & (1 << (m - 1)):
            match = i - m + 1
            if trace:
                print("Found at %d" % (i - m + 1))
            matches.append(match)
    return matches


if __name__ == '__main__':
    txt = "h badeca edcade"
    ptn = "cade"
    matches_1 = bmh(txt, ptn, blanks=False, debug=True)
    print(matches_1)
    matches_2 = bmhs(txt, ptn, blanks=False, debug=True)
    print(matches_2)
    matches_3 = shift_and(txt, ptn, blanks=False, debug=True)
    print(matches_3)

