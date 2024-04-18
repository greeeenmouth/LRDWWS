#!/usr/bin/env python3

# Copyright 2018-2020  Yiming Wang
#           2018-2020  Daniel Povey
#           2021       Binbin Zhang
# Apache 2.0
""" This script prepares the Mobvoi data into kaldi format.
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="""Prepare data.""")
    parser.add_argument('wav_dir',
                        type=str,
                        help='dir containing all the wav files')
    parser.add_argument('text', type=str, help='path to the json file')
    parser.add_argument('scp', type=str, help='out_file')
    args = parser.parse_args()
    print(args.wav_dir, args.text, args.scp)

    fout = open(args.scp, 'w')
    abs_dir = os.path.abspath(args.wav_dir).strip()
    with open(args.text, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            num = line.split(' ')[0].strip('﻿')  # DF0001_0001
            id = num.split('_')[0].strip('﻿')  # DF001
            fout.write(num+' '+abs_dir + '/' + id + '/' + num + '.wav'+'\n')


if __name__ == "__main__":
    main()
