#!/usr/bin/env python
#-*- coding: utf-8 -*-

# standardize: stdvietnamese
#
# Copyright (C) 20012-2014 coclib
# Authors: Tran Huu Cuong <tranhuucuong91@gmail.com>
# URL:     http://tranhuucuong91.wordpress.com/
# License: BSD

"""
    Cac ham chuan hoa tieng Viet
        - tohop2utf8
        - new_diacritic
        - remove_diacritic
        - y2i
"""

import re


def tohop2utf8(utf8_str):
    """
        INPUT:  utf8 string, tieng Viet to hop
        OUTPUT: utf8 string, tieng Viet unicode dung san
    """
    DAU = [u'\u0301',  # sac
           u'\u0300',  # huyen
           u'\u0309',  # hoi
           u'\u0303',  # nga
           u'\u0323'   # nang
           ]

    # dấu ấ           \u0302
    # dấu á           \u0306
    # dấu ơ           \u031B

    OUTTAB = u'áàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ'
    OUTTAB = OUTTAB + OUTTAB.upper()

    INTAB = []
    replaces_dict = {}
    index = 0
    for chu in [u'a', u'â', u'ă', u'e', u'ê', u'i', u'o', u'ô', u'ơ', u'u',
                u'ư', u'y', u'A', u'Â', u'Ă', u'E', u'Ê', u'I', u'O', u'Ô',
                u'Ơ', u'U', u'Ư', u'Y']:
        for dau in DAU:
            INTAB.append(chu + dau)
            replaces_dict[chu + dau] = OUTTAB[index]
            index += 1

    # Đ co 2 ma khac nhau: u'\xd0'     u'\u0110' <- day moi da Đ tieng Viet
    # Ð:    ð
    # Đ:    đ
    INTAB.append(u'\xd0')
    replaces_dict[u'\xd0'] = u'\u0110'

    r = re.compile('|'.join(INTAB))

    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def new_diacritic(utf8_str):
    """
        INPUT:  tieng Viet co dau da chuan hoa tohop2utf8()
        OUTPUT: tieng Viet co dau, dat dau kieu moi
    """

    INTAB = [u'òa', u'óa', u'ỏa', u'õa', u'ọa', u'òe', u'óe', u'ỏe', u'õe',
             u'ọe', u'ùy', u'úy', u'ủy', u'ũy', u'ụy']
    OUTTAB = [u'oà', u'oá', u'oả', u'oã', u'oạ', u'oè', u'oé', u'oẻ', u'oẽ',
              u'oẹ', u'uỳ', u'uý', u'uỷ', u'uỹ', u'uỵ']

    replaces_dict = dict(zip(INTAB, OUTTAB))

    r = re.compile('|'.join(INTAB))

    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def remove_diacritic(utf8_str):
    """
        INPUT:  tieng Viet co dau da chuan hoa tohop2utf8()
        OUTTAB: tieng Viet khong dau
    """

    INTAB = u'aáàảãạâấầẩẫậăắằẳẵặeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵđ'
    OUTTAB = u'a' * 18 + u'e' * 12 + u'i' * 6 + u'o' * 18 + u'u' * 12 + \
             u'y' * 6 + u'd'

    INTAB = INTAB + INTAB.upper()
    OUTTAB = OUTTAB + OUTTAB.upper()

    replaces_dict = dict(zip(INTAB, OUTTAB))

    r = re.compile('|'.join(INTAB))

    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def y2i(utf8_str):
    """
        INPUT:  tieng Viet co dau da chuan hoa tohop2utf8()
        OUTTAB: tieng Viet quy ve chuan i ngan
        Co the khong dung voi thuc te nhung chuan hoa de de xu ly.
    """

    CONSONANT = [u'b', u'c', u'd', u'đ', u'g', u'h', u'k', u'l', u'm', u'n',
                 u'p', u'q', u'r', u's', u't', u'v', u'x']

    Y = u"yýỳỷỹỵ"
    I = u"iíìỉĩị"

    INTAB = []
    OUTTAB = []

    for c in CONSONANT:
        for index in range(len(Y)):
            INTAB.append('%s%s' % (c, Y[index]))
            OUTTAB.append('%s%s' % (c, I[index]))

    replaces_dict = dict(zip(INTAB, OUTTAB))

    r = re.compile("|".join(INTAB))

    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='standardize vietnamese')
    parser.add_argument('input', type=str)
    parser.add_argument('output', type=str)

    args = parser.parse_args()

    with open(args.input) as f:
        old_data = f.read()
        new_data = new_diacritic(tohop2utf8(old_data))

    with open(args.output, 'w') as f:
        f.write(new_data)

if __name__ == '__main__':
    main()
