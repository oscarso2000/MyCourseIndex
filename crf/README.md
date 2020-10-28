# Conditional Random Fields (CRF)
A pure python implementation of the Conditional Random Fields

## Usage

You can test this code with [CoNLL 2000 Chunking Data](https://www.clips.uantwerpen.be/conll2000/chunking/).

### Training

```sh
# format
python3 crf_train.py <train_file> <model_file>

# example
python3 crf_train.py data/chunking_small/small_train.data small_model.json
```

### Test

```sh
# format
python3 crf_test.py <test_file> <trained_model_file>

# example
python3 crf_test.py data/chunking_small/small_test.data small_model.json
```

**Accuracy**

|    Dataset     | crf |
|--------------- | -------- |
| chunking_full  | 0.960128 |
| chunking_small | 0.899072 |

## Reference
TODO
