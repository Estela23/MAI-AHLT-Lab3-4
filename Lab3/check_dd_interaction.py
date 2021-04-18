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
    rule_subject2 = rule_subject(analysis, entities, e1, e2)
    if rule_subject2 is not None:
        return rule_subject2
    else:
        rule_v_m = rule_verb_middle(analysis, entities, e1, e2)
        if rule_v_m is not None:
            return rule_v_m
        else:
            rule_h = rule_head(analysis, entities, e1, e2)
            if rule_h is not None:
                return rule_h
            else:
                return None
    '''rule_subject2 = rule_subject(analysis, entities, e1, e2)
    if rule_subject2 is not None:
        return rule_subject2
    else:
        rule_v_m = rule_verb_middle(analysis, entities, e1, e2)
        if rule_v_m is not None:
            return rule_v_m
        else:
            rule_h = rule_head(analysis, entities, e1, e2)
            if rule_h is not None:
                return rule_h
            else:
                advise = rule_advise(analysis, entities, e1, e2)
                if advise is not None:
                    return advise
                else:
                    return None'''
    return None


def rule_subject(analysis, entities, e1, e2):
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']
    nsubj = [item['word'] for key,item in analysis.nodes.items() if item['rel']== 'nsubj' or (item['head'] in analysis.nodes and analysis.nodes[item['head']]['rel']=='nsubj')]
    dobj=[item['word'] for key,item in analysis.nodes.items() if item['rel']== 'obj' or (item['head'] in analysis.nodes and analysis.nodes[item['head']]['rel']=='obj')]
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
    rel_e1 = ""
    rel_e2 = ""
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'inhibit', 'antagonize', 'augment', 'block']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance']
    inter = ['interact', 'interaction']
    advice = ['consider']
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
        if rel_e1 == 'nsubj' and rel_e2 == 'dobj' and head_e1 == head_e2:
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
    rule_advised = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']
    lengths = {key: len(value) for key, value in entities.items()}
    if lengths[e1] == 2 and lengths[e2] == 2:
        for i in range(1, len(analysis.nodes) + 1):
            if analysis.nodes[i]['lemma'] in rule_advised:
                return "advise"
    return None


def rule_verb_middle(analysis, entities, e1, e2):
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
                if analysis.nodes[i]["tag"] == "VB" and analysis.nodes[i]["start"] > start_e1 and analysis.nodes[i][
                    "end"] < start_e2:
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
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'inhibit', 'antagonize', 'augment', 'block']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance']
    inter = ['interact', 'interaction']
    advice = ['consider']

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
