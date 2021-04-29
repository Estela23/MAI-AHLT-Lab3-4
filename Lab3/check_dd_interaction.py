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

    rule_subj_obj = rule_subject_object_improved(analysis, entities, e1, e2)
    if rule_subj_obj is not None:
        return rule_subj_obj
    else:

        rule_v_m = rule_verb_middle(analysis, entities, e1, e2)
        if rule_v_m is not None:
            return rule_v_m
        else:

            advise = rule_advise(analysis, entities, e1, e2)
            if advise is not None:
                return advise
            else:
                return None


def rule_subject_object_improved(analysis, entities, e1, e2):
    """
    This rule checks whether one of the entities is the subject and the other is the object of the same verb
    in the dependency tree. In that case the lemma of that verb decides the type of interaction the entities have
    """
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']

    nsubj = []
    dobj = []
    for key, value in analysis.nodes.items():
        if key != 0:
            if analysis.nodes[key]['rel'] == 'nsubj':
                nsubj.append(analysis.nodes[key]['word'])
            elif analysis.nodes[key]['rel'] == 'obj':
                dobj.append(analysis.nodes[key]['word'])
            elif analysis.nodes[key]['head'] is not None:
                k = analysis.nodes[key]['head']
                while analysis.nodes[k]['rel'] != 'nsubj' and analysis.nodes[k]['rel'] != 'obj'\
                        and analysis.nodes[k]['head'] != 0 and analysis.nodes[k]['head'] is not None:
                    k = analysis.nodes[k]['head']
                if analysis.nodes[k]['rel'] == 'nsubj':
                    nsubj.append(analysis.nodes[key]['word'])
                elif analysis.nodes[k]['rel'] == 'obj':
                    dobj.append(analysis.nodes[key]['word'])
    verb_1 = ""
    verb_obj_1 = ""
    verb_2 = ""
    verb_obj_2 = ""
    if len(nsubj) > 0 and len(dobj) > 0:
        lengths = {key: len(value) for key, value in entities.items()}
        if lengths[e1] == 2 and lengths[e2] == 2:
            for key, value in analysis.nodes.items():
                if 'start' in analysis.nodes[key] and 'end' in analysis.nodes[key]:
                    if analysis.nodes[key]['start'] == int(entities[e1][0]) and analysis.nodes[key]['end'] == int(
                            entities[e1][1]) and analysis.nodes[key]['word'] in nsubj:
                        if analysis.nodes[key]['rel'] == 'nsubj':
                            verb_1 = analysis.nodes[analysis.nodes[key]['head']]['lemma']
                        else:
                            auxiliar = analysis.nodes[analysis.nodes[key]['head']]
                            if auxiliar['rel'] == 'nsubj':
                                verb_1 = analysis.nodes[auxiliar['head']]['lemma']
                    elif analysis.nodes[key]['start'] == int(entities[e1][0]) and analysis.nodes[key]['end'] == int(
                            entities[e1][1]) and analysis.nodes[key]['word'] in dobj:
                        if analysis.nodes[key]['rel'] == 'obj':
                            verb_obj_1 = analysis.nodes[analysis.nodes[key]['head']]['lemma']
                        else:
                            auxiliar = analysis.nodes[analysis.nodes[key]['head']]
                            if auxiliar['rel'] == 'obj':
                                verb_obj_1 = analysis.nodes[auxiliar['head']]['lemma']
                    elif analysis.nodes[key]['start'] == int(entities[e2][0]) and analysis.nodes[key]['end'] == int(
                            entities[e2][1]) and analysis.nodes[key]['word'] in nsubj:
                        if analysis.nodes[key]['rel'] == 'nsubj':
                            verb_2 = analysis.nodes[analysis.nodes[key]['head']]['lemma']
                        else:
                            auxiliar = analysis.nodes[analysis.nodes[key]['head']]
                            if auxiliar['rel'] == 'nsubj':
                                verb_2 = analysis.nodes[auxiliar['head']]['lemma']
                    elif analysis.nodes[key]['start'] == int(entities[e2][0]) and analysis.nodes[key]['end'] == int(
                            entities[e2][1]) and analysis.nodes[key]['word'] in dobj:
                        if analysis.nodes[key]['rel'] == 'obj':
                            verb_obj_2 = analysis.nodes[analysis.nodes[key]['head']]['lemma']
                        else:
                            auxiliar = analysis.nodes[analysis.nodes[key]['head']]
                            if auxiliar['rel'] == 'obj':
                                verb_obj_2 = analysis.nodes[auxiliar['head']]['lemma']
    if verb_1 != "" and verb_obj_2 != "" and verb_1 == verb_obj_2:
        if verb_1 in effect:
            return 'effect'
        elif verb_1 in mechanism:
            return 'mechanism'
        elif verb_1 in inter:
            return 'int'
        elif verb_1 in advice:
            return 'advise'
    if verb_2 != "" and verb_obj_1 != "" and verb_2 == verb_obj_1:
        if verb_2 in effect:
            return 'effect'
        elif verb_2 in mechanism:
            return 'mechanism'
        elif verb_2 in inter:
            return 'int'
        elif verb_2 in advice:
            return 'advise'
    return None


def rule_subject_object(analysis, entities, e1, e2):
    """
    This rule checks whether the entities we are analyzing have the same head in the dependency tree. In that case
    if their head is a verb from any of the fourth lists, we detect a drug interaction of that type
    """
    rel_e1 = ""
    rel_e2 = ""

    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']

    lengths = {key: len(value) for key, value in entities.items()}
    if lengths[e1] == 2 and lengths[e2] == 2:
        for key, value in analysis.nodes.items():
            if 'start' in analysis.nodes[key] and 'end' in analysis.nodes[key]:
                if analysis.nodes[key]['start'] == int(entities[e1][0]) and analysis.nodes[key]['end'] == int(
                        entities[e1][1]):
                    rel_e1 = analysis.nodes[key]['rel']
                    head_e1 = analysis.nodes[key]['head']
                elif analysis.nodes[key]['start'] == int(entities[e2][0]) and analysis.nodes[key]['end'] == int(
                        entities[e2][1]):
                    rel_e2 = analysis.nodes[key]['rel']
                    head_e2 = analysis.nodes[key]['head']
        if rel_e1 == 'nsubj' and rel_e2 == 'obl' and head_e1 == head_e2:
            if analysis.nodes[head_e1]['lemma'] in effect:
                return 'effect'
            elif analysis.nodes[head_e1]['lemma'] in mechanism:
                return 'mechanism'
            elif analysis.nodes[head_e1]['lemma'] in inter:
                return 'int'
            elif analysis.nodes[head_e1]['lemma'] in advice:
                return 'advise'
    return None


def rule_advise(analysis, entities, e1, e2):
    """
    This rule checks whether any word from the list "rule_advised" is in between our entities of interest
    """
    rule_advised = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']
    lengths = {key: len(value) for key, value in entities.items()}
    if lengths[e1] == 2 and lengths[e2] == 2:
        for i in range(1, len(analysis.nodes) + 1):
            if analysis.nodes[i]['lemma'] in rule_advised:
                return "advise"
    return None


def rule_verb_middle(analysis, entities, e1, e2):
    """
    This rule checks whether there is a verb in the middle of the two entities. If so, the first verb that appears
    after the first entity determines the type of interaction between them.
    """
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']

    lengths = {key: len(value) for key, value in entities.items()}

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])

    if lengths[e1] == 2 and lengths[e2] == 2:
        for i in range(1, len(analysis.nodes) + 1):
            if "tag" in analysis.nodes[i] and "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                if analysis.nodes[i]["tag"] == "VB" and analysis.nodes[i]["start"] > start_e1 and \
                        analysis.nodes[i]["end"] < start_e2:
                    if analysis.nodes[i]['lemma'] in effect:
                        return 'effect'
                    elif analysis.nodes[i]['lemma'] in mechanism:
                        return 'mechanism'
                    elif analysis.nodes[i]['lemma'] in inter:
                        return 'int'
                    elif analysis.nodes[i]['lemma'] in advice:
                        return "advise"
    return None


def rule_head(analysis, entities, e1, e2):
    """
    This rule checks whether or not two entities have the same head. If so, the lemma of the head determines the
    type of interaction between them if it is in one of the four lists
    """
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']

    head_e1 = None
    head_e2 = None

    lengths = {key: len(value) for key, value in entities.items()}
    if lengths[e1] == 2 and lengths[e2] == 2:
        for key, value in analysis.nodes.items():
            if 'start' in analysis.nodes[key] and 'end' in analysis.nodes[key]:
                if analysis.nodes[key]['start'] == int(entities[e1][0]) and analysis.nodes[key]['end'] == int(
                        entities[e1][1]):
                    head_e1 = analysis.nodes[key]['head']
                elif analysis.nodes[key]['start'] == int(entities[e2][0]) and analysis.nodes[key]['end'] == int(
                        entities[e2][1]):
                    head_e2 = analysis.nodes[key]['head']
        if head_e1 is not None and head_e2 is not None:
            if head_e1 == head_e2:
                if analysis.nodes[head_e1]['lemma'] in effect:
                    return 'effect'
                elif analysis.nodes[head_e1]['lemma'] in mechanism:
                    return 'mechanism'
                elif analysis.nodes[head_e1]['lemma'] in inter:
                    return 'int'
                elif analysis.nodes[head_e1]['lemma'] in advice:
                    return 'advise'

    return None
