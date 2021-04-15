def check_interaction(analysis, entities, e1, e2):
    """
    Task:
        Decide whether a sentence is expressing a DDI between two drugs.
    Input:
        analysis: a DependencyGraph object with all sentence information
        entites: A list of all entities in the sentence(id and offsets)
        e1, e2: ids of the two entities to be checked.
    Output:
        Returns the type of interaction (’effect’, ’mechanism’, ’advice’, ’int’) between e1 and e2 expressed by
        the sentence, or ’None’ if no interaction is described.
    """

    rule_s_o = rule_subject_object(analysis, entities, e1, e2)
    if rule_s_o != None:
        return rule_s_o
    return None


def rule_subject_object(analysis, entities, e1, e2):
    rel_e1=""
    rel_e2=""
    effect=['administer', 'potentiate', 'prevent']
    mechanism=['reduce', 'increase', 'decrease']
    inter=['interact', 'interaction']
    advice=[]
    lengths = {key: len(value) for key, value in entities.items()}
    if lengths[e1]==2 and lengths[e2]==2:
        for key, value in analysis.nodes.items():
            if 'start' in analysis.nodes[key] and 'end' in analysis.nodes[key] :
                if analysis.nodes[key]['start'] == int(entities[e1][0]) and analysis.nodes[key]['end'] == int(entities[e1][1]):
                    rel_e1 = analysis.nodes[key]['rel']
                    head_e1 = analysis.nodes[key]['head']
                elif analysis.nodes[key]['start'] == int(entities[e2][0]) and analysis.nodes[key]['end'] == int(
                        entities[e2][1]):
                    rel_e2 = analysis.nodes[key]['rel']
                    head_e2 = analysis.nodes[key]['head']
        if rel_e1 == 'nsubj' and rel_e2 == 'dobj' and head_e1==head_e2:
            if analysis.nodes[head_e1]['lemma'] in effect:
                return 'effect'
            elif analysis.nodes[head_e1]['lemma'] in mechanism:
                return 'mechanism'
            elif analysis.nodes[head_e1]['lemma'] in inter:
                return 'int'
            elif analysis.nodes[head_e1]['lemma'] in advice:
                return 'advice'

    return None
