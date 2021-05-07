def extract_features(tree, entities, e1, e2):
    """
    Task: Given an analyzed sentence and two target entities, compute a
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
     , ’path=dobj/combine\nmod\compound’, ’entity_in_between ’]
     """
    features = []

    rule_v_m = rule_verb_middle(tree, entities, e1, e2)
    if rule_v_m is not None:
        features.append(rule_v_m)

    # TODO: WTF?
    paths = path_verbs(tree, entities, e1, e2)
    if paths is not None:
        features.append("path1=" + paths)

    # TODO: aquí estás creando dos paths pero solo devuelves uno (ninguno en verdad)... path de cada entity hasta el ROOT de la frase
    paths = path_entities(tree, entities, e1, e2)
    if paths is not None:
        features.append("path_above=" + paths)

    # Part of Speech of each entity
    pos_entities = part_of_speech_entities(tree, entities, e1, e2)
    features.append("pos_e1=" + pos_entities[0])
    features.append("pos_e2=" + pos_entities[1])

    # TODO: todo lo referente al LCS lo haría en la misma función para no tener que repetir procesos de búsqueda
    LCS_results = LCS(tree, entities, e1, e2)
    if LCS_results is not None:
        features.append("LCSpostag=" + LCS_results[0])
        features.append("LCSword=" + LCS_results[1])
        features.append("LCSlemma=" + LCS_results[2])

    # TODO: sobran las comprobaciones todas
    rel_entities = obtain_rel_entities(tree, entities, e1, e2)
    if rel_entities is not None:
        if rel_entities[0] != "":
            features.append("RelE1=" + rel_entities[0])
        if rel_entities[1] != "":
            features.append("RelE2=" + rel_entities[1])

    # TODO:
    path_LCS = obtain_path_lcs(tree, entities, e1, e2)
    if path_LCS is not None:
        if path_LCS[0] != "":
            features.append("path_LCS1=" + path_LCS[0])
        if path_LCS[1] != "":
            features.append("path_LCS2=" + path_LCS[1])
    return features


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
                    if analysis.nodes[i]["tag"] in ["VB", "MD"] and analysis.nodes[i]["start"] > start_e1 and \
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
            for i in range(1, len(analysis.nodes) + 1):     # TODO quizás con un while se puede optimizar esto
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
    return None


def path_entities(analysis, entities, e1, e2):    # TODO: comprobar si una entity está encima de la otra y sacar el path
    first_entity = ""
    second_entity = ""
    lengths = {key: len(value) for key, value in entities.items()}
    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])
        flag_1 = False
        flag_2 = False
        if lengths[e1] == 2 and lengths[e2] == 2:
            end_e1 = int(entities[e1][1])
            end_e2 = int(entities[e2][1])
            for i in range(1, len(analysis.nodes) + 1):     # TODO quizás con un while se puede optimizar esto, o incluso eliminar el bucle teniendo en cuenta el offset
                if "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                    if analysis.nodes[i]["start"] == start_e1 and analysis.nodes[i]["end"] == end_e1:
                        first_entity = analysis.nodes[i]
                    elif analysis.nodes[i]["start"] == start_e2 and analysis.nodes[i]["end"] == end_e2:
                        second_entity = analysis.nodes[i]
            if first_entity != "" and second_entity != "":
                aux1 = first_entity
                path_e1_above = ""
                while aux1["head"] is not None and "start" in aux1 and "end" in aux1 and aux1["start"] != start_e2 and \
                        aux1["end"] != end_e2:
                    aux1 = analysis.nodes[aux1["head"]]  # TODO: aquí el aux1[rel] puede ser None si el anterior fue ROOT, no queremos esto, no?
                    path_e1_above = path_e1_above + "/" + str(aux1["rel"])
                aux2 = second_entity
                path_e2_above = ""
                while aux2['head'] is not None and "start" in aux2 and "end" in aux2 and aux2["start"] != start_e1 and \
                        aux2["end"] != end_e1:
                    aux2 = analysis.nodes[aux2["head"]]     # TODO: aquí pasa lo mismo, acaba en ROOT/None
                    path_e2_above = path_e2_above + "/" + str(aux2["rel"])
                if "start" in aux1 and "end" in aux1:   # TODO: acaba en el ROOT y después None no devuelve ningún path...
                    if aux1["start"] == start_e2 and aux1["end"] == end_e2:
                        flag_1 = True
                if "start" in aux2 and "end" in aux2:
                    if aux2["start"] == start_e1 and aux2["end"] == end_e1:
                        flag_2 = True

                if flag_1:
                    return path_e1_above
                elif flag_2:
                    return path_e2_above

    return None


def part_of_speech_entities(analysis, entities, e1, e2):
    pos_first_entity = ""
    pos_second_entity = ""
    lengths = {key: len(value) for key, value in entities.items()}
    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])
        if lengths[e1] == 2 and lengths[e2] == 2:
            for i in range(1, len(analysis.nodes) + 1):     # TODO: lo mismo, este bucle podría optimizarse creo sin necesidad de mirar todo, solo con el offset
                if "start" in analysis.nodes[i] and "end" in analysis.nodes[i]:
                    if analysis.nodes[i]["start"] == start_e1 and analysis.nodes[i]["tag"] is not None:
                        pos_first_entity = analysis.nodes[i]["tag"]
                    elif analysis.nodes[i]["start"] == start_e2 and analysis.nodes[i]["tag"] is not None:
                        pos_second_entity = analysis.nodes[i]["tag"]
        return pos_first_entity, pos_second_entity
    return None


def LCS(tree, entities, e1, e2):
    first_entity_tree = ""
    second_entity_tree = ""
    lengths = {key: len(value) for key, value in entities.items()}
    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])
        if lengths[e1] == 2 and lengths[e2] == 2:
            for i in range(1, len(tree.nodes) + 1):     # TODO: Lo de siempre, creo que este for no hace falta o se puede mejorar
                if "start" in tree.nodes[i] and "end" in tree.nodes[i]:
                    if tree.nodes[i]["start"] == start_e1:
                        first_entity_tree = tree.nodes[i]
                    elif tree.nodes[i]["start"] == start_e2:
                        second_entity_tree = tree.nodes[i]
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

        results = []
        all_common_subsumers = [elem for elem in list_first_entity if elem in list_second_entity]
        if all_common_subsumers:
            least_common_subsumer = all_common_subsumers[0]
            results.append(least_common_subsumer["tag"])     # TODO: quizás además el tipo de verbo de entre las listas
            results.append(least_common_subsumer["word"])
            results.append(least_common_subsumer["lemma"])

            return results
    return None


def obtain_rel_entities(tree, entities, e1, e2):
    first_entity_rel = ""
    second_entity_rel = ""
    to_return = []
    lengths = {key: len(value) for key, value in entities.items()}
    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])
        if lengths[e1] == 2 and lengths[e2] == 2:
            for i in range(1, len(tree.nodes) + 1):
                if "start" in tree.nodes[i] and "end" in tree.nodes[i]:
                    if tree.nodes[i]["start"] == start_e1 and tree.nodes[i]["rel"] is not None:
                        first_entity_rel = tree.nodes[i]["rel"]
                    elif tree.nodes[i]["start"] == start_e2 and tree.nodes[i]["rel"] is not None:
                        second_entity_rel = tree.nodes[i]["rel"]
    to_return.append(first_entity_rel)
    to_return.append(second_entity_rel)
    return to_return


def obtain_path_lcs(tree, entities, e1, e2):
    first_entity_tree = ""
    second_entity_tree = ""
    lengths = {key: len(value) for key, value in entities.items()}
    if e1 in entities and e2 in entities:
        start_e1 = int(entities[e1][0])
        start_e2 = int(entities[e2][0])
        if lengths[e1] == 2 and lengths[e2] == 2:
            for i in range(1, len(tree.nodes) + 1):
                if "start" in tree.nodes[i] and "end" in tree.nodes[i]:
                    if tree.nodes[i]["start"] == start_e1:
                        first_entity_tree = tree.nodes[i]
                    elif tree.nodes[i]["start"] == start_e2:
                        second_entity_tree = tree.nodes[i]
    copy_first_entity_tree = first_entity_tree
    copy_second_entity_tree = second_entity_tree
    if first_entity_tree != "" and second_entity_tree != "":
        list_first_entity = []
        list_second_entity = []
        while first_entity_tree['head'] is not None:
            if "start" in first_entity_tree and "end" in first_entity_tree:
                list_first_entity.append(first_entity_tree)
            first_entity_tree = tree.nodes[first_entity_tree["head"]]
        while second_entity_tree['head'] is not None:
            if "start" in second_entity_tree and "end" in second_entity_tree:
                list_second_entity.append(second_entity_tree)
            second_entity_tree = tree.nodes[second_entity_tree["head"]]
        results = []
        stepsfirst = 0
        for i in list_first_entity:
            stepssecond = 0
            for j in list_second_entity:
                if i == j:
                    if len(results) > 0:
                        if results[0] > (stepsfirst + stepssecond):
                            results[0] = stepsfirst + stepssecond
                            results[1] = i
                    else:
                        results.append(stepsfirst + stepssecond)
                        results.append(i)
                stepssecond = stepssecond + 1
            stepsfirst = stepsfirst + 1
        if len(results) > 0:
            path = ""
            path2 = ""
            while copy_first_entity_tree['head'] is not None:
                if copy_first_entity_tree != results[1]:
                    path = path + str(copy_first_entity_tree["rel"]) + "/"
                copy_first_entity_tree = tree.nodes[copy_first_entity_tree["head"]]
            while copy_second_entity_tree['head'] is not None:
                if copy_second_entity_tree != results[1]:
                    path2 = path2 + str(copy_second_entity_tree["rel"]) + "/"
                copy_second_entity_tree = tree.nodes[copy_second_entity_tree["head"]]
            return [path, path2]

    return None
