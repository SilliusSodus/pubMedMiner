def writetograph(words, links):

    file = open("/home/owe8_pg4/public_html/Applicatie.1/static/js/graph.js", "w+")
    file.write('var graph = {\n\t"nodes": [\n')

    for word, group in words.items():
        file.write('\t\t{"id": "' + word + '", "group": ' + str(group) + '},\n')


    file.write('],\n\t"links":[\n')
    for words, values in links.items():
        word1, word2 = words.split(" ")
        simularity = values[0]
        pubids = values[1:]
        file.write('\t\t{"source": "' + word1 + '", "target": "' + word2 + '", "value": ' + str(simularity) + ', "pubids": [' + str(pubids[0]))
        for ids in pubids[1:]:
            file.write(", " + str(ids))
        file.write("]},\n")
    file.write("\t]\n}")
    file.close()



