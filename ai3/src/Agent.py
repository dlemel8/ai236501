'''
Created on Jun 23, 2011

@author: ekfir
'''

from bag_of_words import BagOfWords
from learning_agent import LearningAgent
from nearest_neighbor import NearestNeighbor


class DanielAgent(LearningAgent):
    
    _use_stemming = True
    _use_elminating = True
    _num_features = 10
    _sort_threshold = 0
    _use_good_turing=False
        
    def createFeatureExtractor(self):
        return BagOfWords(self._num_features, self._use_stemming, self._use_elminating, self._sort_threshold, self._use_good_turing)
    
    def createClassifier(self):
        return NearestNeighbor()
    
    def __str__(self):
        s = 'Daniel ' + str(self._num_features)
        s += self._use_stemming and 'T' or 'F'
        s += self._use_elminating and 'T' or 'F'
        s += str(self._sort_threshold)
        s += self._use_good_turing and 'T' or 'F'
        return s
    
class BdioAgent(LearningAgent):
    
    _use_stemming = True
    _use_elminating = True
    _num_features = 10
    _sort_threshold = 0
    _use_good_turing=False
        
    def createFeatureExtractor(self):
        return BagOfWords(self._num_features, self._use_stemming, self._use_elminating, self._sort_threshold, self._use_good_turing)
    
    def createClassifier(self):
        return NearestNeighbor()
    
    def __str__(self):
        s = 'Bdio ' + str(self._num_features)
        s += self._use_stemming and 'T' or 'F'
        s += self._use_elminating and 'T' or 'F'
        s += str(self._sort_threshold)
        s += self._use_good_turing and 'T' or 'F'
        return s
