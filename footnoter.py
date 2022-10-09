import collections
import enum
FOOTNOTE_SYMBOLS = '*†‡§¶#♠♥♦♣'
FOOTNOTE_SYMBOLS_LEN = len(FOOTNOTE_SYMBOLS)


def get_pairs(txt):
    def bad_char(c):
        return c not in ':;'

    pairs = []
    pair_stack = collections.deque()
    for i, x in enumerate(txt):
        if x == '(':
            pair_stack.append(i)
        elif x == ')':
            pairs.append((
                pair_stack.pop(),
                i + 1  # inclusive of the )
            ))
    return pairs


def generate_text(txt, pairs):
    def get_foot_symbol(i):
        multiple = i // FOOTNOTE_SYMBOLS_LEN + 1
        return FOOTNOTE_SYMBOLS[i % FOOTNOTE_SYMBOLS_LEN] * multiple

    footnotes = []
    offset = 0
    for i, pair in enumerate(reversed(pairs)):  # need to reverse so earlier ones don't impact later ones
        footnotes.append(txt[(pair[0] + 1):(pair[1] - 1)])
        txt = txt[:pair[0]].strip() + get_foot_symbol(i) + txt[pair[1]:]  # stripping just for visual appeal
    txt += '\n\n' + '\n'.join(
        get_foot_symbol(i) + ' ' + x
        for i, x in enumerate(reversed(footnotes))  # need a secondary reverse to undo the first one
    )
    print(txt)


def main():
    tst = open('examples/a.txt').read()
    pairs = get_pairs(tst)
    generate_text(tst, pairs)


if __name__ == '__main__':
    main()