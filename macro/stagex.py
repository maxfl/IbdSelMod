#!/usr/bin/env python

"""Simple python macro to run stage1_main.cc"""

from load import ROOT as R
from dayabay_filename import *
import os
from os import path

def process_file(filename, args):
    filedata = parse_dayabay_filename(filename)

    period, site = getattr(R, 'k'+filedata.daq_period), getattr(R, filedata.site)

    if args.verbose:
        print(filedata)

    ofile1, ofile2 = output_filename(filename, args.common_root, args.output_folder, ('stage1', 'stage2'))

    if args.stage==1:
        ifile = filename
        ofile = ofile1
        if args.verbose:
            print('Read {}, write {}'.format(ifile, ofile))
        R.stage1_main(ifile, ofile, period, site)
    else:
        ifile = ofile1
        ofile = ofile2
        if args.verbose:
            print('Read {}, write {}'.format(ifile, ofile))

        stagename = 'stage2_main'
        R.stage2_main(args.cfg, ifile, ofile, period, 0, site)

    print('Done processing file', ifile)
    print('Write output file', ofile)

def main(args):
    args.common_root = find_common_root(args.input)

    for fname in args.input:
        process_file(fname, args)

def output_filename(input_filename, common_root, output_root, suffixes=()):
    if not input_filename.startswith(common_root):
        raise Exception('Invalid input_filename or invalid file root')

    input_path, basename= path.split(input_filename)

    ret = ()
    for suffix in suffixes:
        dirname = os.path.join(output_root, suffix)

        try:
            os.makedirs(dirname)
        except OSError:
            pass
        else:
            print('Create output folder:', dirname)

        ret += os.path.join(dirname, basename),

    return ret

def output_filename_wcommon(input_filename, common_root, output_root, suffixes=()):
    if not input_filename.startswith(common_root):
        raise Exception('Invalid input_filename or invalid file root')

    base = input_filename[len(common_root):]
    if base[0]=='/':
        base = base[1:]

    subdirname, basename = os.path.split(base)

    ret = ()
    for suffix in suffixes:
        dirname = os.path.join(output_root, suffix, subdirname)

        try:
            os.makedirs(dirname)
        except OSError:
            pass
        else:
            print('Create output folder:', dirname)

        ret += os.path.join(dirname, basename),

    return ret

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input', nargs='+', help='input files')
    parser.add_argument('--stage', type=int, choices=[1, 2], required=True, help='Analysis stage')
    # parser.add_argument('-o', '--output', type=checkoutput, required=True, help='output file name for stage ')
    parser.add_argument('-o', '--output-folder', required=True, help='output file name for stage ')
    parser.add_argument('--cfg', required=True, help='configuration file')
    parser.add_argument('-v', '--verbose', action='count', help='verbosity level')

    main(parser.parse_args())

