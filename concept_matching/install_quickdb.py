from __future__ import unicode_literals, division, print_function

# built in modules
import os
import sys
import time
import codecs
import shutil
import argparse
from six.moves import input

from quickumls.toolbox import countlines, CuiSemTypesDB, SimstringDBWriter, mkdir
from quickumls.constants import LANGUAGES
from quickumls.install import (
    extract_from_mrconso,
    parse_and_encode_ngrams
)

try:
    from unidecode import unidecode
except ImportError:
    pass


HEADERS_MRCONSO = [
    'cui',
    'str',
    'lat',
    'ispref',
]
HEADERS_MRSTY = [
    'cui',
    'sty',
    'tui',
]

class InstallConfig:
    destination_path = "./concept_matching/quickUCSLS"
    normalize_unicode = False
    lowercase = True
    umls_installation_path = "./concept_matching/definition_files"
    language = "ENG"

opts = InstallConfig()

if not os.path.exists(opts.destination_path):
    msg = ('Directory "{}" does not exists; should I create it? [y/N] '
               ''.format(opts.destination_path))
    create = True#input(msg).lower().strip() == 'y'

    if create:
        os.makedirs(opts.destination_path)
    else:
        print('Aborting.')
        exit(1)

if len(os.listdir(opts.destination_path)) > 0:
    msg = ('Directory "{}" is not empty; should I empty it? [y/N] '
            ''.format(opts.destination_path))
    empty = True #input(msg).lower().strip() == 'y'
    if empty:
        shutil.rmtree(opts.destination_path)
        os.mkdir(opts.destination_path)
    else:
        print('Aborting.')
        exit(1)

if opts.normalize_unicode:
    try:
        unidecode
    except NameError:
        err = ('`unidecode` is needed for unicode normalization'
                'please install it via the `[sudo] pip install '
                'unidecode` command.')
        print(err, file=sys.stderr)
        exit(1)

    flag_fp = os.path.join(opts.destination_path, 'normalize-unicode.flag')
    open(flag_fp, 'w').close()

if opts.lowercase:
    flag_fp = os.path.join(opts.destination_path, 'lowercase.flag')
    open(flag_fp, 'w').close()


flag_fp = os.path.join(opts.destination_path, 'language.flag')
with open(flag_fp, 'w') as f:
    f.write(opts.language)

mrconso_path = os.path.join(opts.umls_installation_path, 'MRCONSO.RRF')
mrsty_path = os.path.join(opts.umls_installation_path, 'MRSTY.RRF')

mrconso_iterator = extract_from_mrconso(mrconso_path, mrsty_path, opts, mrconso_header=HEADERS_MRCONSO, mrsty_header=HEADERS_MRSTY)

simstring_dir = os.path.join(opts.destination_path, 'umls-simstring.db')
cuisty_dir = os.path.join(opts.destination_path, 'cui-semtypes.db')

parse_and_encode_ngrams(mrconso_iterator, simstring_dir, cuisty_dir, "leveldb")
