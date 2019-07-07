#!/usr/bin/python3

import fileinput
import math

class LetterMatch(object):
        def __init__(self, index, target_index, character):
                self.index = index
                self.target_index = target_index
                self.character = character

class Edge(object):
        def __init__(self, from_letter, to_letter):
                self.from_letter = from_letter
                self.to_letter = to_letter
                self.calculate_weight()

        def calculate_weight(self):
                present_letters = self.to_letter.index - 1 - \
                        self.from_letter.index 
                expected_letters = self.to_letter.target_index - 1 - \
                        self.from_letter.target_index
                self.weight = max([present_letters, expected_letters])

class Graph(object):
        def __init__(self, letters, target):
                self.letters = letters
                self.edges = []
                self.calculate_edges(target)

        def calculate_edges(self, target):
                if not target:
                        return
                letter = target[0]
                new_target = target[1:]
                followers = []
                followed = []
                for letter_match in self.letters:
                        if letter_match.character in new_target:
                                followers.append(letter_match)
                        if letter_match.character == letter:
                                followed.append(letter_match)
                for f in followed:
                        for follower in followers:
                                edge = Edge(f, follower)
                                if (f.index < follower.index and
                                    self.is_new_edge(edge)):
                                        self.edges.append(edge)
                self.calculate_edges(new_target)

        def is_new_edge(self, edge):
                for e in self.edges:
                        if (e.from_letter == edge.from_letter and
                            e.to_letter == edge.to_letter):
                                return False
                return True

        def minimal_cost(self):
                unvisited = self.letters.copy()
                current_node = None
                target_node = None
                for node in unvisited:
                        if node.character == '^':
                                node.distance = 0
                                current_node = node
                        else:
                                node.distance = math.inf
                        if node.character == '$':
                                target_node = node
                while unvisited and current_node != target_node:
                        for edge in self.edges:
                                if edge.from_letter == current_node and \
                                    edge.to_letter in unvisited:
                                        if edge.to_letter.distance > ( 
                                            edge.from_letter.distance +
                                            edge.weight):
                                                edge.to_letter.distance = \
                                                edge.from_letter.distance + \
                                                edge.weight
                        unvisited.remove(current_node)                        
                        current_node = None
                        for node in unvisited:
                                if (current_node == None or
                                    current_node.distance > node.distance):
                                        current_node = node
                return target_node.distance

def calculate_matches(original, target):
        result = []
        for oi, oc in enumerate(original):
                for ti, tc in enumerate(target):
                        letter = LetterMatch(oi, ti, tc)
                        if oc == tc:
                                result.append(letter)
        return result

def main():
    for line in fileinput.input():
        # conveniently marking the start/end
        sign = "^" + line.strip() + "$"
        target = "^Bärn häckt$"
        matching_letters = calculate_matches(sign, target)
        graph = Graph(matching_letters, target)
        cost = graph.minimal_cost()
        print(cost)

if __name__ == "__main__":
    main()
