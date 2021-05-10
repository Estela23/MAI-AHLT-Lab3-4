def extract_features(tree, entities, e1, e2):
    """
    Task: Given an analyzed sentence and two target entities, compute a
    feature vector for this classification example.
    Input: tree: a DependencyGraph object with all sentence information.
           entities: A list of all entities in the sentence(id and offsets).
           e1, e2: ids of the two entities to be checked for an interaction
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
     , ’path=dobj/combine\nmod\compound’, ’entity_in_between ’]
     """
    features = []

    # Check if there is a verb in the middle and its type with respect to the lists of verbs
    rule_v_m = rule_verb_middle(tree, entities, e1, e2)
    if rule_v_m:
        features.append(rule_v_m)

    """# TODO: WTF?
    paths = path_verbs(tree, entities, e1, e2)
    if paths is not None:
        features.append("path1=" + paths)"""

    # Checks whether an entity is above the other and returns the path between them
    """paths = path_entities(tree, entities, e1, e2)
    if paths:
        features.append("path_above=" + paths)"""

    # Extracts the part of speech and 'rel' parameter of each entity
    pos_and_rels = pos_and_rel_entities(tree, entities, e1, e2)
    labels = ["pos_e1=", "pos_e2=", "rel_e1=", "rel_e2="]
    for i in range(len(pos_and_rels)):
        if pos_and_rels[i] != "":
            features.append(labels[i] + pos_and_rels[i])

    """# Part of Speech of each entity
    pos_entities = part_of_speech_entities(tree, entities, e1, e2)
    features.append("pos_e1=" + pos_entities[0])
    features.append("pos_e2=" + pos_entities[1])
    
    # Extracts the 'rel' parameter from the entities, their role inside the sentence
    rel_entities = obtain_rel_entities(tree, entities, e1, e2)
    if rel_entities is not None:
        if rel_entities[0] != "":
            features.append("RelE1=" + rel_entities[0])
        if rel_entities[1] != "":
            features.append("RelE2=" + rel_entities[1])"""

    # Some information about the Least Common Subsumer of the entities
    LCS_results = LCS(tree, entities, e1, e2)
    if LCS_results:
        features.append("LCSpostag=" + LCS_results[0])
        features.append("LCSword=" + LCS_results[1])
        features.append("LCSlemma=" + LCS_results[2])
        features.append("path_e1_LCS=" + LCS_results[3])
        features.append("path_e2_LCS=" + LCS_results[4])
        features.append("path_e1_LCS_e2=" + LCS_results[5])
        if len(LCS_results) > 6:
            features.append("LCS_type=" + LCS_results[6])

    return features


######################################################################################################
#####                          Auxiliary functions to extract  features                          #####
######################################################################################################


# TODO: meter feature de entities: distancia entre ambas y si hay otras entities o no entre ellas


def rule_verb_middle(analysis, entities, e1, e2):
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])

    for i in range(1, len(analysis.nodes) + 1):
        if "start" in analysis.nodes[i]:
            if analysis.nodes[i]["tag"] in ["VB", "VBD", "MD"] and analysis.nodes[i]["start"] > start_e1 and \
                    analysis.nodes[i]["end"] < start_e2:
                if analysis.nodes[i]['lemma'] in effect:
                    return 'verb_effect_middle'
                elif analysis.nodes[i]['lemma'] in mechanism:
                    return 'verb_mechanism_middle'
                elif analysis.nodes[i]['lemma'] in inter:
                    return 'verb_int_middle'
                elif analysis.nodes[i]['lemma'] in advice:
                    return "verb_advise_middle"
    return None


# TODO: meter palabras de antes, medio y después

"""def path_verbs(analysis, entities, e1, e2):
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
                if "tag" in analysis.nodes[i] and "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                    if analysis.nodes[i]["tag"] in ["VB", "VBD", "MD"]:
                        aux1 = analysis.nodes[analysis.nodes[i]["head"]]    # TODO: qué querías hacer aquí? porque estos aux1 y aux2 son iguales..
                        aux2 = analysis.nodes[analysis.nodes[i]["head"]]
                        path = str(aux1["rel"])
                        path2 = str(aux2["rel"])
                        while aux1['head'] is not None and "start" in aux1 and "end" in aux1 and aux1[
                            "start"] != start_e1 and aux1["end"] != end_e1:
                            aux1 = analysis.nodes[aux1["head"]]
                            path = path + "/" + str(aux1["rel"])

                        while aux2['head'] is not None and "start" in aux2 and "end" in aux2 and aux2[
                            "start"] != start_e2 and aux2["end"] != end_e2:
                            aux2 = analysis.nodes[aux2["head"]]
                            path2 = path2 + "/" + str(aux2["rel"])
                        if "start" in aux1 and "end" in aux1 and "start" in aux2 and "end" in aux2:
                            if aux1["start"] == start_e1 and aux1["end"] == end_e1:
                                flag_1 = True
                            if aux2["start"] == start_e2 and aux2["end"] == end_e2:
                                flag_2 = True
                            lemma = "<" + analysis.nodes[i][
                                'lemma'] + ">"  # TODO: REVISAR EL CODIGO PUEDE QUE ESTE MAL OJO
                            # paths.append(["<"+analysis.nodes[i]['lemma']+">"])
                            return path + lemma + path2     # TODO: esto no tiene pinta de estar nada bien xD
    return None"""


""" REDUNDANT
    def path_entities(analysis, entities, e1, e2):
    # TODO: esto creo que es redundante con el LCS, porque si una esta encima de otra sera el LCS la de arriba ya, no?
    ""
    :returns: checks whether an entity is above the other and returns the corresponding path
    ""
    first_entity = ""
    second_entity = ""
    lengths = {key: len(value) for key, value in entities.items()}

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])
    flag_1 = False
    flag_2 = False
    if lengths[e1] == 2 and lengths[e2] == 2:
        end_e1 = int(entities[e1][1])
        end_e2 = int(entities[e2][1])
        for i in range(1, len(analysis.nodes) + 1):
            if first_entity == "" or second_entity == "":
                if "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                    if analysis.nodes[i]["start"] == start_e1 and analysis.nodes[i]["end"] == end_e1:
                        first_entity = analysis.nodes[i]
                    elif analysis.nodes[i]["start"] == start_e2 and analysis.nodes[i]["end"] == end_e2:
                        second_entity = analysis.nodes[i]

        if first_entity != "" and second_entity != "":
            aux1 = first_entity
            path_e1_above = ""
            while aux1["head"] is not None and "start" in aux1 and aux1["start"] != start_e2 and aux1["end"] != end_e2:
                aux1 = analysis.nodes[aux1["head"]]
                path_e1_above = path_e1_above + "/" + str(aux1["rel"])

            aux2 = second_entity
            path_e2_above = ""
            while aux2['head'] is not None and "start" in aux2 and aux2["start"] != start_e1 and aux2["end"] != end_e1:
                aux2 = analysis.nodes[aux2["head"]]
                path_e2_above = path_e2_above + "/" + str(aux2["rel"])

            if "start" in aux1:
                if aux1["start"] == start_e2 and aux1["end"] == end_e2:
                    flag_1 = True
            if "start" in aux2:
                if aux2["start"] == start_e1 and aux2["end"] == end_e1:
                    flag_2 = True

            if flag_1:
                return path_e1_above
            elif flag_2:
                return path_e2_above

    return None"""


def pos_and_rel_entities(analysis, entities, e1, e2):
    # TODO: meter word, lemma de la propia entity
    """
    :return: part of speech tag of the two entities
    """
    pos_first_entity = ""
    pos_second_entity = ""
    first_entity_rel = ""
    second_entity_rel = ""

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])
    for i in range(1, len(analysis.nodes) + 1):
        if pos_first_entity == "" or pos_second_entity == "":
            if "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                if analysis.nodes[i]["start"] == start_e1 and analysis.nodes[i]["tag"] is not None and \
                        analysis.nodes[i]["rel"] is not None:
                    pos_first_entity = analysis.nodes[i]["tag"]
                    first_entity_rel = analysis.nodes[i]["rel"]
                elif analysis.nodes[i]["start"] == start_e2 and analysis.nodes[i]["tag"] is not None and \
                        analysis.nodes[i]["rel"] is not None:
                    pos_second_entity = analysis.nodes[i]["tag"]
                    second_entity_rel = analysis.nodes[i]["rel"]
    return pos_first_entity, pos_second_entity, first_entity_rel, second_entity_rel


def LCS(tree, entities, e1, e2):
    """
    :returns: a list with the tag, word, lemma of the LCS of the entities and
             3 paths: from e1 to LCS, from e2 to LCS and from e1 to e2 going through LCS
    """
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']

    first_entity_tree = ""
    second_entity_tree = ""

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])
    for i in range(1, len(tree.nodes) + 1):
        if first_entity_tree == "" or second_entity_tree == "":
            if "start" in tree.nodes[i] and "end" in tree.nodes[i]:
                if tree.nodes[i]["start"] == start_e1:
                    first_entity_tree = tree.nodes[i]
                elif tree.nodes[i]["start"] == start_e2:
                    second_entity_tree = tree.nodes[i]

    # Save in the lists all the tokens above (in the dependency tree) each entity
    if first_entity_tree != "" and second_entity_tree != "":
        list_first_entity = []
        list_second_entity = []
        while first_entity_tree['head'] != 0:
            list_first_entity.append(first_entity_tree)
            first_entity_tree = tree.nodes[first_entity_tree["head"]]
        list_first_entity.append(first_entity_tree)

        while second_entity_tree['head'] != 0:
            list_second_entity.append(second_entity_tree)
            second_entity_tree = tree.nodes[second_entity_tree["head"]]
        list_second_entity.append(second_entity_tree)

        all_common_subsumers = [elem for elem in list_first_entity if elem in list_second_entity]
        least_common_subsumer = all_common_subsumers[0]

        results = [least_common_subsumer["tag"], least_common_subsumer["word"], least_common_subsumer["lemma"]]

        # Paths between e1, LCS and e2
        # We remove from the list the common subsumers that are not the LCS to create the paths e1->LCS->e2 ...
        number_common_subsumers = len(all_common_subsumers) - 1
        rels_e1 = [elem['rel'] for elem in list_first_entity]
        rels_e2 = [elem['rel'] for elem in list_second_entity]

        if number_common_subsumers > 0:
            rels_e1_LCS = rels_e1[:-number_common_subsumers]
            rels_e2_LCS = list(reversed(rels_e2[:-number_common_subsumers]))
        else:
            rels_e1_LCS = rels_e1
            rels_e2_LCS = list(reversed(rels_e2))

        path_e1_LCS = "->".join(rels_e1_LCS)
        results.append(path_e1_LCS)

        path_e2_LCS = "<-".join(rels_e2_LCS)
        results.append(path_e2_LCS)

        path_e1_LCS_e2 = "=".join([path_e1_LCS, path_e2_LCS])
        results.append(path_e1_LCS_e2)

        # Check the type of verb of the LCS if it is a verb
        if least_common_subsumer["tag"] in ["VB", "VBD", "MD"]:
            if least_common_subsumer['lemma'] in effect:
                results.append("effect")
            elif least_common_subsumer['lemma'] in mechanism:
                results.append("mechanism")
            elif least_common_subsumer['lemma'] in inter:
                results.append("int")
            elif least_common_subsumer['lemma'] in advice:
                results.append("advise")

        return results
    return None
