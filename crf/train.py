# 
import argparse

from model.crf import LinearChainCRF
from utils.read_conll import read_conll_corpus

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", help="data file for training input")
    parser.add_argument("modelfile", help="the model file name. (output)")

    args = parser.parse_args()

    training_data = read_conll_corpus(args.datafile)

    crf = LinearChainCRF()
    crf.train(training_data, args.modelfile)

