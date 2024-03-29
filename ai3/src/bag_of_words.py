from feature_extractor import FeatureExtractor
import re
from numpy.ma.core import log

class BagOfWords(FeatureExtractor):
    '''
    Extracts a bag of words representation with TFIDF scores from raw text.
    '''
    
    _unwanted_words = ["a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", 
                       "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then",  "there", 
                       "these", "they", "this", "to", "was", "will", "with"]
    
    def __init__(self, num_features, use_stemming=True, use_elminating=True, threshold_fact = 0, use_good_turing=False):
        '''
        Constructor.
        
        @param num_features: The number of features to extract.
        '''
        self.num_features = num_features
        self.use_stemming = use_stemming
        self.use_elminating = use_elminating
        self.threshold_fact = threshold_fact
        self.use_good_turing = use_good_turing
    
    def extract(self, raw_instance):
        '''
        Creates a new instance in the feature-space from the given raw instance.
        
        @param raw_instance: A string.
        @return: A tuple of numerical features, each feature representing a word 
                 and its TFIDF score.
        '''
        tf = self._countTermFrequency(raw_instance)
        features = []
        for word in self.order:
            if word in tf:
                features += [tf[word] * self.idf[word]]
            else:
                features += [0]
        return tuple(features)
    
    def setup(self, examples, extraction_time_limit, setup_time_limit):
        '''
        Prepares a dictionary of inverse-document-frequencies (IDFs) for each word,
        and selects the terms with the highest IDFs as the features.
        
        @param examples: A list of raw data examples.
        @param extraction_time_limit: The time that will be allocated for each example.
        @param setup_time_limit: The time limit for setting up this agent.
        '''
        self.extraction_time_limit = extraction_time_limit
        
        doc_count = float(len(examples))
        tf_examples = []
        for raw_example in examples: 
            tf_examples += [self._countTermFrequency(raw_example)]
        self.idf = self._countInverseDocumentFrequency(tf_examples)
        #print self.threshold_fact, len(self.idf), self.idf
        
        self.order = sorted(self.idf.items(), lambda item1, item2: -cmp(item1[1], item2[1]))
        self.order = self.order[:self.num_features]
        self.idf = dict(self.order)
        self.order = [x[0] for x in self.order]
        
        for word in self.idf.keys():
            self.idf[word] = log(doc_count / self.idf[word])
    
    def _stem_word(self, word):
        new_word = word
        if word.endswith('sses'):
            new_word = word[:-4] + 'ss'
        elif word.endswith('ies'):
            new_word = word[:-3] + 'i'
        elif word.endswith('eed') and len(word) > 3:
            new_word = word[:-3] + 'ee'
        elif word.endswith('ing'):
            new_word = word[:-3] + ''
        elif word.endswith('ss'):
            new_word = word[:-2] + 'ss'
        elif word.endswith('ed'):
            new_word = word[:-2] + ''
        elif word.endswith('at'):
            new_word = word[:-2] + 'ate'
        elif word.endswith('bl'):
            new_word = word[:-2] + 'ble'
        elif word.endswith('iz'):
            new_word = word[:-2] + 'ize'
        elif word.endswith('s'):
            new_word = word[:-1] + ''    
        
        return new_word
        
    def _stemming(self, words):
        res = []
        for w in words:
            res += [self._stem_word(w)]
        return list(set(res))
    
    def _countTermFrequency(self, raw_example):
        '''
        Counts the frequency of each word in each document.
        
        @param raw_example: A raw example (strings).
        @return: A term frequency (word count) dictionary.
        '''
        example = {}
        total_count = 0
        words = self._getTerms(raw_example)
        if self.use_elminating:
            words = [w for w in words if w not in self._unwanted_words]
        if self.use_stemming:
            words = self._stemming(words)
        for word in words:
            if word not in example:
                example[word] = 1.0
            else:
                example[word] += 1.0
            total_count += 1
        if not self.use_good_turing:
            for word in example.keys():
                example[word] = example[word] / total_count
        else:
            Nr = {}
            for v in example.values():
                if v in Nr:
                    Nr[v] += 1.0
                else:
                    Nr[v] = 1.0
            
            N = sum([r*Nr[r] for r in Nr])
                    
            for k in example.keys():
                r = example[k]
                if r+1 not in Nr:
                    Nr[r+1] = 0     
                example[k] = (r+1) * Nr[r+1] / (N * Nr[r])
            
        return example
    
    def _countInverseDocumentFrequency(self, tf_examples):
        '''
        Counts the number of documents containing each word.
        
        @param tf_examples: A list of processed examples, each one represented by a term frequency 
                            (word count) dictionary.
        @return: A dictionary of each word and the number of different documents it appears in.
        '''
        idf = {}
        idf_2 = {}
        for example in tf_examples:
            tmp_idf = {}
            for word in example.keys():
                if word not in idf:
                    idf[word] = 1
                else:
                    idf[word] += 1
                    
                if word not in tmp_idf:
                    tmp_idf[word] = True
                    
            for item in tmp_idf:
                if item not in idf_2:
                    idf_2[item] = 1
                else:
                    idf_2[item] += 1
        
        if self.threshold_fact:
            threshold = self.threshold_fact * len(tf_examples)
            idf = dict([x for x in idf.items() if idf_2[x[0]] < threshold]) 
        
        return idf
    
    def _getTerms(self, text):
        '''
        Retrieves all the terms (keywords) from the given text.
        This method defines a term to be an alphabetical string of at least three characters. 
        
        @param text: A string.
        @return: A list of terms.
        '''
        pattern = re.compile(r'[a-z]{3,}')
        return re.findall(pattern, text.lower())
