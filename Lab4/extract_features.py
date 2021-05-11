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

    # If there is a verb in the middle of the entities checks its type (of the first) with respect to the lists of verbs
    verbs_bf, verbs_bt, verbs_aft = rule_verbs(tree, entities, e1, e2)
    for i in range(len(verbs_bf)):
        features.append("verb_bf_" + verbs_bf[i])
    for j in range(len(verbs_bt)):
        features.append("verb_bt_" + verbs_bt[j])
    for k in range(len(verbs_aft)):
        features.append("verb_aft_" + verbs_aft[k])

    # Number of entities there are between the ones we are examining
    n_entities_bt = int(e2[-1]) - int(e1[-1]) - 1
    if n_entities_bt > 0:
        features.append("{}_entities_in_between".format(n_entities_bt))

    # TODO: WTF?
    """
    paths = path_verbs(tree, entities, e1, e2)
    if paths is not None:
        features.append("path1=" + paths)"""

    """# Checks whether an entity is above the other and returns the path between them
    paths = path_entities(tree, entities, e1, e2)
    if paths:
        features.append("path_above=" + paths)"""

    # Extracts the part of speech, 'rel' parameter, word and lemma of the entities
    information_entities = info_entities(tree, entities, e1, e2)
    labels = ["pos_e1=", "pos_e2=", "rel_e1=", "rel_e2=", "word_e1=", "word_e2=", "lemma_e1=", "lemma_e2=", "n_tokens_ib="]
    for i in range(len(information_entities) - 1):
        if information_entities[i] != "":
            features.append(labels[i] + information_entities[i])
    if information_entities[-1] != "0":
        features.append(labels[-1] + information_entities[-1])

    # Anotate all lemmas appearing before e1, between both entities and after e2
    lemmas_before, lemmas_between, lemmas_after = lemmas_pos_before_between_after(tree, entities, e1, e2)
    for i in range(len(lemmas_before)):
        features.append("lemma_bf=" + lemmas_before[i])
    for j in range(len(lemmas_between)):
        features.append("lemma_bt=" + lemmas_between[j])
    for k in range(len(lemmas_after)):
        features.append("lemma_aft=" + lemmas_after[k])

    # Information about the Least Common Subsumer of the entities: PoS, word, lemma, paths from e1 to LCS,
    # from LCS to e2, from e1 to e2 through LCS and type of verb if LCS is a verb
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


def rule_verbs(analysis, entities, e1, e2):
    effect = ['administer', 'potentiate', 'prevent', 'react', 'produce', 'attenuate', 'treat', 'alter', 'augment',
              'influence', 'prevent', 'antagonize', 'augment', 'block', 'cause']
    mechanism = ['reduce', 'increase', 'decrease', 'induce', 'elevate', 'enhance', 'metabolize', 'inhibit', 'lower']
    inter = ['interact', 'interaction']
    advice = ['consider', 'may', 'possible', 'recommended', 'caution', 'should', 'overdose', 'advise', 'advised']

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])

    verbs_before = []
    verbs_between = []
    verbs_after = []

    for i in range(1, len(analysis.nodes) + 1):
        if "start" in analysis.nodes[i]:
            if analysis.nodes[i]["tag"] in ["VB", "VBN", "VBD", "MD"] and analysis.nodes[i]["start"] < start_e1:
                if analysis.nodes[i]['lemma'] in effect:
                    verbs_before.append("effect_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in mechanism:
                    verbs_before.append("mechanism_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in inter:
                    verbs_before.append("int_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in advice:
                    verbs_before.append("advise_{}".format(analysis.nodes[i]["lemma"]))
            elif analysis.nodes[i]["tag"] in ["VB", "VBN", "VBD", "MD"] and analysis.nodes[i]["start"] > start_e1 and \
                    analysis.nodes[i]["end"] < start_e2:
                if analysis.nodes[i]['lemma'] in effect:
                    verbs_between.append("effect_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in mechanism:
                    verbs_between.append("mechanism_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in inter:
                    verbs_between.append("int_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in advice:
                    verbs_between.append("advise_{}".format(analysis.nodes[i]["lemma"]))
            elif analysis.nodes[i]["tag"] in ["VB", "VBN", "VBD", "MD"] and analysis.nodes[i]["start"] > start_e2:
                if analysis.nodes[i]['lemma'] in effect:
                    verbs_after.append("effect_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in mechanism:
                    verbs_after.append("mechanism_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in inter:
                    verbs_after.append("int_{}".format(analysis.nodes[i]["lemma"]))
                elif analysis.nodes[i]['lemma'] in advice:
                    verbs_after.append("advise_{}".format(analysis.nodes[i]["lemma"]))
    return verbs_before, verbs_between, verbs_after


def lemmas_pos_before_between_after(analysis, entities, e1, e2):
    lemmas_pos_before_1 = []
    lemmas_pos_between = []
    lemmas_pos_after_2 = []

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])
    for i in range(1, len(analysis.nodes) + 1):
        if "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
            if analysis.nodes[i]["start"] < start_e1 and analysis.nodes[i]["rel"] != "punct":
                lemmas_pos_before_1.append(analysis.nodes[i]["lemma"] + "_" + analysis.nodes[i]["tag"])
            elif start_e1 < analysis.nodes[i]["start"] < start_e2 and analysis.nodes[i]["rel"] != "punct":
                lemmas_pos_between.append(analysis.nodes[i]["lemma"] + "_" + analysis.nodes[i]["tag"])
            elif analysis.nodes[i]["start"] > start_e2 and analysis.nodes[i]["rel"] != "punct":
                lemmas_pos_after_2.append(analysis.nodes[i]["lemma"] + "_" + analysis.nodes[i]["tag"])

    return lemmas_pos_before_1, lemmas_pos_between, lemmas_pos_after_2


""" DE ESTA NO ESTOY MUY SEGURA, EN VERDAD SE PODRÍA MIRAR, ME OLVIDÉ JE
def path_verbs(analysis, entities, e1, e2):
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


def info_entities(analysis, entities, e1, e2):
    """
    :return: part of speech tag of the two entities
    """
    pos_first_entity = ""
    pos_second_entity = ""
    first_entity_rel = ""
    second_entity_rel = ""
    word_first_entity = ""
    word_second_entity = ""
    lemma_first_entity = ""
    lemma_second_entity = ""
    n_tokens_ib = 0

    start_e1 = int(entities[e1][0])
    start_e2 = int(entities[e2][0])
    for i in range(1, len(analysis.nodes) + 1):
        if pos_first_entity == "" or pos_second_entity == "":
            if "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                if start_e1 < analysis.nodes[i]["start"] < start_e2 and analysis.nodes[i]["rel"] != "punct":
                    n_tokens_ib += 1
                if analysis.nodes[i]["start"] == start_e1 and analysis.nodes[i]["tag"] is not None and \
                        analysis.nodes[i]["rel"] is not None:
                    pos_first_entity = analysis.nodes[i]["tag"]
                    first_entity_rel = analysis.nodes[i]["rel"]
                    word_first_entity = analysis.nodes[i]["word"]
                    lemma_first_entity = analysis.nodes[i]["lemma"]
                elif analysis.nodes[i]["start"] == start_e2 and analysis.nodes[i]["tag"] is not None and \
                        analysis.nodes[i]["rel"] is not None:
                    pos_second_entity = analysis.nodes[i]["tag"]
                    second_entity_rel = analysis.nodes[i]["rel"]
                    word_second_entity = analysis.nodes[i]["word"]
                    lemma_second_entity = analysis.nodes[i]["lemma"]
    return pos_first_entity, pos_second_entity, first_entity_rel, second_entity_rel,\
           word_first_entity, word_second_entity, lemma_first_entity, lemma_second_entity, str(n_tokens_ib)


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
            e1_LCS = rels_e1[:-(number_common_subsumers + 1)] + [least_common_subsumer["tag"]]
            e2_LCS = list(reversed(rels_e2[:-(number_common_subsumers + 1)] + [least_common_subsumer["tag"]]))
        else:
            e1_LCS = rels_e1[:-1] + [least_common_subsumer["tag"]]
            e2_LCS = list(reversed(rels_e2[:-1] + [least_common_subsumer["tag"]]))

        path_e1_LCS = "->".join(e1_LCS)
        results.append(path_e1_LCS)

        path_e2_LCS = "<-".join(e2_LCS)
        results.append(path_e2_LCS)

        path_e1_LCS_e2 = "=".join([path_e1_LCS, path_e2_LCS])
        results.append(path_e1_LCS_e2)

        # Check the type of verb of the LCS if it is a verb
        if least_common_subsumer["tag"] in ["VB", "VBN", "VBD", "MD"]:
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
