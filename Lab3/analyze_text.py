# import nltk CoreNLP module (just once)
from nltk.parse.corenlp import CoreNLPDependencyParser
# connect to your CoreNLP server (just once)
my_parser = CoreNLPDependencyParser(url="http://localhost:9000")


def analyze(my_text):
    """
    Task:
    Given one sentence, sends it to CoreNLP to obtain the tokens, tags, and dependency tree.
    It also adds the start / end offsets to each token.
    Input:
        s: string containing the text for one sentence
    Output:
        Returns the nltk DependencyGraph object produced by CoreNLP, enriched with token offsets.
    Example:
    >> analyze("Caution should be exercised when combining resorcinol or salicylic acid with DIFFERIN Gel")
    {0:{’head’: None, ’lemma’: None, ’rel’: None, ’tag’: ’TOP’, ’word’: None},
     1: {’word’: ’Caution’, ’head’:4, ’lemma’: ’caution’, ’rel’: ’nsubjpass’, ’tag’: ’NN’, ’start’:0, ’end’:6},
     2: {’word’: ’should’, ’head’:4, ’lemma’: ’should’, ’rel’: ’aux’, ’tag’: ’MD’, ’start’:8, ’end’:13},
     3: {’word’: ’be’, ’head’:4, ’lemma’: ’be’, ’rel’: ’auxpass’, ’tag’: ’VB’, ’start’:15, ’end’:16},
     4: {’word’: ’exercised’, ’head’:0, ’lemma’: ’exercise’, ’rel’: ’ROOT’, ’tag’: ’VBN’, ’start’:18, ’end’:26},
     5: {’word’: ’when’, ’head’:6, ’lemma’: ’when’, ’rel’: ’advmod’, ’tag’: ’WRB’, ’start’:28, ’end’:31},
     6: {’word’: ’combining’, ’head’:4, ’lemma’: ’combine’, ’rel’: ’advcl’, ’tag’: ’VBG’, ’start’:33, ’end’:41},
    ...
    """

    # parse text (as many times as needed). Watch the comma!
    my_tree, = my_parser.raw_parse(my_text)

    # TODO: Add offset to the tree
    analyzed_text = my_tree

    return analyzed_text


