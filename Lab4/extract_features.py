def extract_features(tree , entities , e1, e2):
    '''Task: Given an analyzed sentence and two target entities, compute a
    featurevector for this  classification  example.
    Input:tree: a DependencyGraph object with  all  sentence  information.
    entities: A list of all entities in the sentence(id and offsets).
    e1, e2: ids of the two entities to be checked for an  interaction
    Output:
    A vector of binary features.
    Features are binary and vectors are in sparse representation(i.e. only active
    features are listed)
    Example: >>> extract_features(tree, {’DDI - DrugBank.d370.s1.e0 ’:[’43’, ’52’],
     ’DDI - DrugBank.d370.s1.e1 ’:[’57’, ’70’],
     ’DDI - DrugBank.d370.s1.e2 ’:[’77’, ’88’]},
     ’DDI - DrugBank.d370.s1.e0’, ’DDI - DrugBank.d370.s1.e2 ’)
     [’lb1 = Caution ’, ’lb1 = be’, ’lb1 = exercise ’, ’lb1 = combine ’, ’lib = or ’, ’lib
     = salicylic ’, ’lib = acid ’, ’lib = with ’, ’LCSpos=VBG ’, ’LCSlema=combine’
     , ’path=dobj / combine\nmod\compound ’ ’entity_in_between ’]'''
    if rule_verb_middle(tree, entities, e1, e2) is not None:
        if rule_verb_middle(tree, entities, e1, e2)=='verb_effect_middle':
            return ['1']
        elif rule_verb_middle(tree, entities, e1, e2)=='verb_mechanism_middle':
            return ['2']
        else:
            return ['3']
    else:
        return ['0']

def rule_verb_middle(analysis, entities, e1, e2):
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']
    lengths = {key: len(value) for key, value in entities.items()}

    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])

        if lengths[e1] == 2 and lengths[e2] == 2:
            for i in range(1, len(analysis.nodes) + 1):
                if "tag" in analysis.nodes[i] and "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                    if analysis.nodes[i]["tag"] == "VB" and analysis.nodes[i]["start"] > start_e1 and analysis.nodes[i][
                        "end"] < start_e2:
                        if analysis.nodes[i]['lemma'] in effect:
                            return 'verb_effect_middle'
                        elif analysis.nodes[i]['lemma'] in mechanism:
                            return 'verb_mechanism_middle'
                        elif analysis.nodes[i]['lemma'] in inter:
                            return 'verb_int_middle'
                        elif analysis.nodes[i]['lemma'] in advice:
                            return "verb_advise_middle"
    return None