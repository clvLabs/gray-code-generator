#!/usr/bin/pytnon3
import argparse
from src.absoluteencoder import AbsoluteEncoder

DEFAULT_GAP = 0
DEFAULT_INNER_DIAMETER = 100
DEFAULT_OUTER_DIAMETER = 1000

parser = argparse.ArgumentParser()
parser.add_argument('bits',                       help='number of bits', type=int)
parser.add_argument('outfile',                    help='name of the generated SVG')
parser.add_argument('-id', '--inner-diameter',    help='diameter of the inner circle', type=int, default=DEFAULT_INNER_DIAMETER)
parser.add_argument('-od', '--outer-diameter',    help='diameter of the outer circle', type=int, default=DEFAULT_OUTER_DIAMETER)
parser.add_argument('-g', '--gap',                help='gap between bits', type=float, default=DEFAULT_GAP)
parser.add_argument('-d', '--debug',              help='debug mode (adds extra figures to output)', action='store_true')
parser.add_argument('-q', '--quiet',              help='suppress console output', action='store_true')
args = parser.parse_args()

encoder = AbsoluteEncoder(args)
encoder.save()
