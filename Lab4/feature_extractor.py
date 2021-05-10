# Main function copied from the slides of the presentation
from Lab3.analyze_text import analyze
from extract_features import extract_features
from os import listdir
from xml.dom.minidom import parse
import sys

datadir = sys.argv[1]
outfile = sys.argv[3]

with open(outfile, 'w') as output:
    # process each file in directory
    for index_file, f in enumerate(listdir(datadir)):
        print(index_file, " - ", f)
        # parse XML file, obtaining a DOM tree
        tree = parse(datadir + "/" + f)
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences:
            sid = s.attributes["id"].value
            # get sentence ids
            stext = s.attributes["text"].value
            # get sentence text
            # load sentence ground truth entities
            entities = {}
            ents = s.getElementsByTagName("entity")
            for e in ents:
                id = e.attributes["id"].value
                entities[id] = e.attributes["charOffset"].value.split("-")
            # analyze (generate dependency tree) sentence if there is at least a pair of entities
            if len(entities) > 1:
                analysis = analyze(stext)

            # for each pair of entities, decide whether it is DDI and its type
            pairs = s.getElementsByTagName("pair")
            for p in pairs:
                # get  ground  truth
                ddi = p.attributes["ddi"].value
                dditype = p.attributes["type"].value if ddi == "true" else "null"
                # target  entities
                id_e1 = p.attributes["e1"].value
                id_e2 = p.attributes["e2"].value
                # feature  extraction
                feats = extract_features(analysis, entities, id_e1, id_e2)
                # resulting  feature  vector
                print(sid, id_e1, id_e2, dditype, "\t".join(feats), sep="\t", file=output)
