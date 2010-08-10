from graph.base import Graph
from itertools import count
import sys


class GrammarTagger:

    def __init__(self, graph):
        self._structure_graph = graph
        self.taggingList = []
        self.id = 0

    @property
    def structureGraph(self):
        return self._structure_graph


    def tag(self, tagsList):
        taggingGraph = Graph()
        self.taggingList =[]
        step = 0
        #we add atoms
        validatedList = self.add_atoms(taggingGraph, tagsList)
        self.export_graph(taggingGraph, step)
        step += 1
       
        while step < 20 :
            # we add rules
            self.add_rule(taggingGraph, validatedList)
            self.export_graph(taggingGraph, step)
            print("END ADD_RULE ", step)
            step += 1
            print(self.taggingList)
            # we validate some rules
            self.validate_rule(taggingGraph)
            self.export_graph(taggingGraph, step)
            print("END VALIDATE_RULE", step)
            step += 1
            # remove rule which have a children impossible to connect in current sentence
            self.remove_impossible_rule(taggingGraph)
            self.export_graph(taggingGraph, step)
            print("END REMOVE_IMPOSSIBLE", step)
            step += 1

            # we fusion rules
            self.fusion_rule(taggingGraph)
            self.export_graph(taggingGraph, step)
            print("END FUSION", step)
            step += 1

            # we validate rules (as some could have changed with fusion)
            self.validate_rule(taggingGraph)
            self.export_graph(taggingGraph, step)
            print("END VALIDATE", step)
            step += 1

            # we remove rules that are left without children after fusion
            self.remove_non_connected_rule(taggingGraph)
            self.export_graph(taggingGraph, step)
            print("END REMOVE NON CONNECTED", step)
            step += 1
            #prepare new turn
            validatedList = self.prepare_new_base(taggingGraph)
            if not validatedList:
                break
            print()
            print(validatedList)
            print('final')
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()
            print()

    def export_graph(self, taggingGraph, step) :
        
        #print(self.taggingList)
        from graph.extras import dot
        from subprocess import getstatusoutput

        # build the drawing tool
        drawer = dot.DotGenerator()

        # populate the output file
        name = "tagging_graph" + str(step)
        with open('dot/' + name + '.dot', 'w') as f:
            output = drawer.draw(taggingGraph, "tag_graph")
            f.write(output)

        getstatusoutput("dot -Tsvg -o picture/tag/"+name+".svg -v dot/"+name+".dot")

    def add_atoms(self, taggingGraph, atoms):
        i = 0
        addedList = []
        for atomType in atoms:
            newConnectorName = atomType + "_" + str(self.id) #uuid4().hex
            self.id += 1
            connectors = self.structureGraph.search_nodes(type=atomType, category="child")
            for connector in connectors:
                if newConnectorName not in taggingGraph:
                    connectorNode = taggingGraph.add_node( newConnectorName, **connector.data)
                    connectorNode.color = "violet"
                    connectorNode.shape = "box"
                    connectorNode.connected = True
                    connectorNode.validated = False
                    addedList.append([newConnectorName])
                    break
            i += 1
        print("added list")
        print(addedList)
        return addedList

    def add_rule(self, taggingGraph, validatedList):
        i = 0
        self.taggingList = [];
        for position in validatedList:
            positionList = [];
            for tag in position:
                atomNode = taggingGraph[tag]
                if not atomNode.connected:
                    continue
                atomNode.validated = True
                atomNode.color = "red"
                connectors = self.structureGraph.search_nodes(type=atomNode.type, category="child")
                connectorsList = []

            
                for connector in connectors:
                    edge = connector.incoming[0]
                    topNode = edge.start#other_end(connector)
                    #TODO this is a hack
                    #we test if the rule does not already exist
                    #ruleAlreadyConnected = False
                    #for topEdge in atomNode.incoming:
                    #   if topNode.rule_id == topEdge.start.rule_id:
                    #        ruleAlreadyConnected = True
                    #        break
                    #if ruleAlreadyConnected:
                    #    continue
                    #print(connector)
                    #print(topNode)
                    # We add in the sentence's graph the element (connector) and the
                    # group (top Node)
                    newTopNodeName = topNode.name + "_" + str(self.id) # uuid4().hex
                    self.id += 1
                    
                    #we add the rule Node which current node can be part of
                    newTopNode = taggingGraph.add_node( newTopNodeName , **topNode.data )
                    #only for style
                    newTopNode.color = 'green'
                    newTopNode.shape = "box"
                    newTopNode.connected = False
                    newTopNode.validated = False
                    

                    # now we had the non-connected terminal of the rule
                    j = 0
                    for outgoingEdge in topNode.outgoing:
                        if edge.order == outgoingEdge.order:
                            currentEdge = taggingGraph.add_edge(
                                newTopNodeName,
                                tag,
                                label = edge.order,
                                order = edge.order,
                            )
                            j += 1
                            continue
                        
                        unconnectedAtom = outgoingEdge.other_end(topNode)
                        tempNodeName = unconnectedAtom.name + "_" + str(j) + str(self.id)
                        unconnectedTagNode = taggingGraph.add_node(tempNodeName, **unconnectedAtom.data)
                        unconnectedTagNode.color = "blue"
                        unconnectedTagNode.shape = "box"
                        unconnectedTagNode.connected = False
                        unconnectedTagNode.validated = False

                        taggingGraph.add_edge(
                            newTopNodeName,
                            tempNodeName,
                            label = outgoingEdge.order,
                            order = outgoingEdge.order,
                        )

                        j += 1
                    print("add ",newTopNodeName);
                    connectorsList.append(
                        newTopNodeName
                    )
                    #print('dede')
                    #print(connectorsList)
                    i += 1
                positionList.append(connectorsList)
            self.taggingList.append(positionList)#print(self.taggingList)

    # stage 2 validate rule having all its node connected
    def validate_rule(self, taggingGraph):
        print()
        print()
        print("stage 2")
        print()
        print()
        print(self.taggingList)
        for position in self.taggingList:
            print("\t",position);
            for rule in position:
                print("\t\t",rule);
                ruleNode = taggingGraph[rule]
                print("\t\t",ruleNode);
                allConnected = True
                if ruleNode.connected:
                    continue
                for edge in ruleNode.outgoing:
                    atomNode = edge.end
                    if not atomNode.connected:
                        allConnected = False
                        break
                if allConnected :
                    ruleNode.connected = True
                    print('@@turn to violet ', ruleNode.name) 
                    ruleNode.color= "violet"
                #print(ruleNode)
        return 0

    # stage 3 fusion same occurence of a rule which different
    # connected and unconnected atom
    def fusion_rule(self,taggingGraph):
        print()
        print()
        print("stage 3")
        print()
        print()
        i = 0
        for position in self.taggingList:
            for ruleInstance in position: 
                lastConnected = 0
                ruleNode = taggingGraph[ruleInstance]
                # if the node already have all its item connected
                # then we already know no fusion is possible
                if ruleNode.connected == True:
                    break
                ruleId = ruleNode.rule_id
                #print(ruleInstance)
                for atomEdge in ruleNode.outgoing:
                    #print(atomEdge)
                    if atomEdge.end.connected == False:
                        break
                    lastConnected +=1
                if lastConnected != 0 :
                    nextPosition = self.taggingList[i+1]
                    for nextRule in nextPosition:
                        nextRuleNode = taggingGraph[nextRule]
                        if nextRuleNode.rule_id != ruleId:
                            break
                        #print("possible fusion")
                        for nextAtomEdge in nextRuleNode.outgoing:
                            nextAtomNode = nextAtomEdge.end
                            if nextAtomEdge.order < lastConnected:
                                if nextAtomNode.connected == True:
                                    break
                            else:
                                if nextAtomNode.connected == False:
                                    break
                                nextAtomNode.connected = False
                                nextAtomNode.color = "blue"
                                
                                tempNode = ruleNode.outgoing[nextAtomEdge.order].end
                                tempNode.connected = True
                                tempNode.color = "red"



            i += 1

    def remove_non_connected_rule(self,taggingGraph):
        print()
        print()
        print("stage 4")
        print()
        print()

        lenTaggingList = len(self.taggingList)
        i = 0
        while i < lenTaggingList:
            position = self.taggingList[i]
            nbrRuleInstance = len(position)
            j = 0
            while j < nbrRuleInstance:
                ruleInstance = position[j]
                ruleNode = taggingGraph[ruleInstance]
                if ruleNode.connected:
                    j +=1
                    continue
                #first removed rule which don't have any node connected
                #anymore
                noneConnected = True
                for edge in ruleNode.outgoing:
                    atomNode = edge.end
                    if atomNode.connected:
                        noneConnected = False
                        break
                if  noneConnected :
                    for edge in ruleNode.outgoing:
                        atomNode = edge.end
                        taggingGraph.remove_edge(edge)
                        taggingGraph.remove_node(atomNode)
                    print("## we remove cause orphan",ruleNode)
                    taggingGraph.remove_node(ruleNode)
                    position.remove(ruleInstance)
                    j -= 1
                    nbrRuleInstance -= 1
                    if not position:
                        self.taggingList.remove(position)
                        lenTaggingList -=1
                        i -= 1
                j += 1
            i +=1

    def remove_impossible_rule(self,taggingGraph):
        print()
        print()
        print("stage 5")
        print()
        print()
        print(self.taggingList)
        
        lenTaggingList = len(self.taggingList)
        i = 0
        while i < lenTaggingList:
            position = self.taggingList[i]
            nbrRuleInstance = len(position)
            j = 0
            while j < nbrRuleInstance:
                ruleInstance = position[j]
                ruleNode = taggingGraph[ruleInstance]
                if ruleNode.connected or ruleNode.position != "begin":
                    j +=1
                    continue
                #print(ruleInstance); 
                #then removed rule which are looking for an atom which is not present
                atomNodeFound = False
                for edge in ruleNode.outgoing:
                    atomNode = edge.end
                    if not atomNode.connected:
                        if atomNode.isAtom:
                            for foudNode in taggingGraph.search_nodes(type = atomNode.type, connected = True):
                                atomNodeFound = True
                                break
                            if not atomNodeFound:
                                break
                if not atomNodeFound:
                    for edge in ruleNode.outgoing:
                        atomNode = edge.end
                        taggingGraph.remove_edge(edge)
                        if not atomNode.connected:
                            taggingGraph.remove_node(atomNode)
                    
                    print("## we remove impossible ",ruleNode)
                    taggingGraph.remove_node(ruleNode)
                    position.remove(ruleInstance)
                    j -= 1
                    nbrRuleInstance -= 1
                    if not position:
                        self.taggingList.remove(position)
                        lenTaggingList -=1
                        i -= 1
                j += 1
            i +=1
    def prepare_new_base(self, taggingGraph):
        print("prepare")
        tagsList = []
        for position in self.taggingList:
            tempTupple = []
            for ruleInstance in position:
                #print(ruleInstance)
                ruleNode = taggingGraph[ruleInstance]
                if ruleNode.connected and not ruleNode.validated:
                    #print("pouet")
                    print("append ", ruleInstance);
                    tempTupple.append(ruleInstance)
                    #print(tempTupple)
            if tempTupple:
                tagsList.append(tempTupple)
                #print("prout")
                #print(tagsList)
        return tagsList
