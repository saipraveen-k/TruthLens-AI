import re
import string
from typing import List
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class TextPreprocessor:
    """Text preprocessing utilities for NLP pipeline"""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        if not text:
            return ""
        return BeautifulSoup(text, "html.parser").get_text()
    
    def clean_special_characters(self, text: str) -> str:
        """Remove special characters and extra whitespace"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-alphanumeric characters except punctuation
        text = re.sub(r'[^\w\s\.\!\?\,\;\:\-\'\"]', '', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        if not text:
            return []
        
        # Convert to lowercase and tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and punctuation
        tokens = [
            token for token in tokens 
            if token not in self.stop_words 
            and token not in string.punctuation
            and len(token) > 2
        ]
        
        return tokens
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """Lemmatize tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def sentence_tokenize(self, text: str) -> List[str]:
        """Tokenize text into sentences"""
        if not text:
            return []
        
        sentences = sent_tokenize(text)
        # Clean each sentence
        return [self.clean_special_characters(sent.strip()) for sent in sentences if sent.strip()]
    
    def preprocess(self, text: str, remove_stopwords: bool = True) -> str:
        """Complete preprocessing pipeline"""
        if not text:
            return ""
        
        # Clean HTML
        text = self.clean_html(text)
        
        # Clean special characters
        text = self.clean_special_characters(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove stopwords if requested
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]
        
        # Lemmatize
        tokens = self.lemmatize(tokens)
        
        # Join back to text
        return ' '.join(tokens)
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract top keywords from text"""
        tokens = self.tokenize(text)
        tokens = self.lemmatize(tokens)
        
        # Simple frequency-based keyword extraction
        from collections import Counter
        freq = Counter(tokens)
        
        # Get most common tokens
        keywords = [word for word, count in freq.most_common(top_k)]
        
        return keywords
    
    def calculate_readability(self, text: str) -> dict:
        """Calculate basic readability metrics"""
        if not text:
            return {"flesch_score": 0, "reading_level": "Unknown"}
        
        sentences = self.sentence_tokenize(text)
        words = self.tokenize(text)
        
        if not sentences or not words:
            return {"flesch_score": 0, "reading_level": "Unknown"}
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Average syllables per word (simplified)
        def count_syllables(word):
            vowels = "aeiouy"
            count = 0
            prev_was_vowel = False
            
            for char in word.lower():
                if char in vowels:
                    if not prev_was_vowel:
                        count += 1
                    prev_was_vowel = True
                else:
                    prev_was_vowel = False
            
            if word.endswith("e"):
                count -= 1
            
            return max(1, count)
        
        total_syllables = sum(count_syllables(word) for word in words)
        avg_syllables_per_word = total_syllables / len(words)
        
        # Flesch Reading Ease Score
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Determine reading level
        if flesch_score >= 90:
            reading_level = "Very Easy"
        elif flesch_score >= 80:
            reading_level = "Easy"
        elif flesch_score >= 70:
            reading_level = "Fairly Easy"
        elif flesch_score >= 60:
            reading_level = "Standard"
        elif flesch_score >= 50:
            reading_level = "Fairly Difficult"
        elif flesch_score >= 30:
            reading_level = "Difficult"
        else:
            reading_level = "Very Difficult"
        
        return {
            "flesch_score": round(flesch_score, 2),
            "reading_level": reading_level,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2)
        }
