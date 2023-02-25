from typing import List

from nltk.util import ngrams

def map_ngrams(inp_data, n: int) -> List[dict[str, int]]:
    """
    Turns the input string into a dict of ngrams with count 1.
    Includes repeats since these are handled by the reduction function.
    """
    inp_list = inp_data.split()

    input_ngrams = ngrams(inp_list, n, pad_left=False, pad_right=False)
    return [{" ".join(ngram): 1} for ngram in input_ngrams]

def reduce_ngrams(inp_data: List[dict[str, int]]) -> dict[str, int]:
    """
    Reduces the list of ngram count dicts into a single dict of counts.
    """
    out_dict = {}
    for data_dict in inp_data:
        for word_key, word_count in data_dict.items():
            if out_dict.get(word_key):
                out_dict[word_key] += word_count
            else:
                out_dict.update({word_key: word_count})
    return out_dict