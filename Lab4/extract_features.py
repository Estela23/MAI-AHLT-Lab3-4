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
    features=[]
    rule_v_m = rule_verb_middle(tree, entities, e1, e2)
    if rule_v_m is not None:
        features.append(rule_v_m)
    paths = path_verbs(tree, entities, e1, e2)
    if paths is not None:
        features.append("path1="+paths)
    paths = path_entities(tree, entities, e1, e2)
    if paths is not None:
        features.append("path2="+paths)
    return features
def path_entities(analysis, entities, e1, e2):
    first_entity=""
    second_entity=""
    lengths = {key: len(value) for key, value in entities.items()}
    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])
        flag_1 = False
        flag_2 = False
        if lengths[e1] == 2 and lengths[e2] == 2:
            end_e1 = int(entities[e1][1])
            end_e2 = int(entities[e2][1])
            for i in range(1, len(analysis.nodes) + 1):
                if "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                    if analysis.nodes[i]["start"] == start_e1 and analysis.nodes[i]["end"] ==end_e1:
                        first_entity=analysis.nodes[i]
                    elif analysis.nodes[i]["start"] == start_e2 and analysis.nodes[i]["end"] ==end_e2:
                        second_entity=analysis.nodes[i]
            if first_entity!="" and second_entity!="":
                aux1=first_entity
                path = ""
                while aux1['head'] is not None and aux1["start"] != start_e2 and aux1["end"] != end_e2:
                    aux1 = analysis.nodes[aux1["head"]]
                    path = path + "/" + str(aux1["rel"])
                aux2=second_entity
                path2 = ""
                while aux2['head'] is not None and aux2["start"] != start_e1 and aux2["end"] != end_e1:
                    aux2 = analysis.nodes[aux2["head"]]
                    path2 = path2 + "/" + str(aux2["rel"])
                if "start" in aux1 and "end" in aux1:
                    if aux1["start"] == start_e2 and aux1["end"] == end_e2:
                        flag_1 = True
                if "start" in aux2 and "end" in aux2:
                    if aux2["start"] == start_e1 and aux2["end"] == end_e1:
                        flag_2 = True
                if flag_1:
                    return path
                elif flag_2:
                    return path2

    return None
def path_verbs(analysis, entities, e1, e2):
    lengths = {key: len(value) for key, value in entities.items()}
    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])
        flag_1=False
        flag_2=False
        if lengths[e1] == 2 and lengths[e2] == 2:
            end_e1 = int(entities[e1][1])
            end_e2 = int(entities[e2][1])
            for i in range(1, len(analysis.nodes) + 1):
                if "tag" in analysis.nodes[i] and "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                    if analysis.nodes[i]["tag"] == "VB" or analysis.nodes[i]["tag"] == "VBD":
                        aux1=analysis.nodes[analysis.nodes[i]["head"]]
                        aux2 = analysis.nodes[analysis.nodes[i]["head"]]
                        path = str(aux1["rel"])
                        path2=str(aux2["rel"])
                        while aux1['head'] is not None and aux1["start"] != start_e1 and aux1["end"] != end_e1:
                            aux1=analysis.nodes[aux1["head"]]
                            path=path+"/"+str(aux1["rel"])

                        while aux2['head'] is not None and aux2["start"] != start_e2 and aux2["end"] != end_e2:
                            aux2=analysis.nodes[aux2["head"]]
                            path2=path2+"/"+str(aux2["rel"])
                        if "start" in aux1 and "end" in aux1 and "start" in aux2 and "end" in aux2:
                            if aux1["start"] == start_e1 and aux1["end"] == end_e1:
                                flag_1=True
                            if aux2["start"] == start_e2 and aux2["end"] == end_e2:
                                flag_2=True
                            lemma="<"+analysis.nodes[i]['lemma']+">"#TODO: REVISAR EL CODIGO PUEDE QUE ESTE MAL OJO
                            #paths.append(["<"+analysis.nodes[i]['lemma']+">"])
                            return path+lemma+path2
    return None
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