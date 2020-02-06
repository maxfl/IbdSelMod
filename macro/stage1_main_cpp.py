#!/usr/bin/env python

"""Simple python macro to run stage1_main.cc"""

from load import ROOT as R

def main(args):
    stage, site = getattr(R, 'k'+args.stage), getattr(R, args.site)
    R.stage1_main(args.input, args.output, stage, site)

    print('Done processing file', args.input)
    print('Write output file', args.output)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input', help='input files')
    parser.add_argument('--site',  choices=('EH1', 'EH2', 'EH3'), required=True, help='site to process')
    parser.add_argument('--stage', choices=('6AD', '8AD', '7AD'), required=True, help='DAQ stage')
    parser.add_argument('-o', '--output', required=True, help='output file name')

    main(parser.parse_args())
