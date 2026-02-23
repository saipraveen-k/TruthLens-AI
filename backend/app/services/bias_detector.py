import re
import numpy as np
from textblob import TextBlob
import logging
from typing import Dict, Any, List
from collections import Counter

logger = logging.getLogger(__name__)


class BiasDetector:
    """Detects political bias and loaded language in text"""
    
    def __init__(self):
        # Political bias dictionaries
        self.left_leaning_words = [
            "progressive", "liberal", "social justice", "equality", "diversity",
            "inclusion", "climate change", "healthcare", "immigration reform",
            "gun control", "reproductive rights", "lgbtq+", "racial justice"
        ]
        
        self.right_leaning_words = [
            "conservative", "traditional values", "free market", "tax cuts",
            "second amendment", "pro-life", "family values", "national security",
            "border security", "law and order", "patriotism", "religious freedom"
        ]
        
        self.center_words = [
            "bipartisan", "moderate", "centrist", "balanced", "neutral",
            "objective", "fair", "impartial", "unbiased", "balanced approach"
        ]
        
        # Loaded language indicators
        self.loaded_positive = [
            "amazing", "incredible", "outstanding", "revolutionary", "breakthrough",
            "heroic", "courageous", "inspiring", "remarkable", "extraordinary"
        ]
        
        self.loaded_negative = [
            "disgusting", "horrible", "terrible", "devastating", "catastrophic",
            "shocking", "outrageous", "appalling", "disgraceful", "unacceptable"
        ]
        
        self.sensational_words = [
            "bombshell", "explosive", "scandal", "controversy", "shocking",
            "unbelievable", "miracle", "breakthrough", "game-changing", "historic"
        ]
        
        self._initialized = False
    
    async def initialize(self):
        """Initialize the bias detector"""
        if self._initialized:
            return
        
        logger.info("Initializing Bias Detector...")
        self._initialized = True
        logger.info("Bias Detector initialized successfully")
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text for bias and loaded language"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            text_lower = text.lower()
            words = text_lower.split()
            
            # Political leaning analysis
            political_bias = self._analyze_political_bias(text_lower, words)
            
            # Loaded language analysis
            loaded_language = self._analyze_loaded_language(text_lower, words)
            
            # Subjectivity analysis
            subjectivity = self._analyze_subjectivity(text)
            
            # Sentiment analysis
            sentiment = self._analyze_sentiment(text)
            
            # Clickbait analysis
            clickbait = self._analyze_clickbait(text_lower)
            
            # Overall bias score
            overall_bias = self._calculate_overall_bias(
                political_bias, loaded_language, subjectivity, clickbait
            )
            
            return {
                "political_bias": political_bias,
                "loaded_language": loaded_language,
                "subjectivity": subjectivity,
                "sentiment": sentiment,
                "clickbait": clickbait,
                "overall_bias_score": overall_bias["score"],
                "bias_level": overall_bias["level"],
                "bias_indicators": overall_bias["indicators"]
            }
            
        except Exception as e:
            logger.error(f"Error in bias analysis: {e}")
            return self._fallback_analysis(text)
    
    def _analyze_political_bias(self, text_lower: str, words: List[str]) -> Dict[str, Any]:
        """Analyze political leaning of the text"""
        
        left_count = sum(1 for phrase in self.left_leaning_words if phrase in text_lower)
        right_count = sum(1 for phrase in self.right_leaning_words if phrase in text_lower)
        center_count = sum(1 for phrase in self.center_words if phrase in text_lower)
        
        total_political_words = left_count + right_count + center_count
        
        if total_political_words == 0:
            return {
                "leaning": "neutral",
                "confidence": 0.0,
                "left_score": 0.0,
                "right_score": 0.0,
                "center_score": 0.0,
                "detected_phrases": []
            }
        
        # Calculate normalized scores
        left_score = left_count / total_political_words
        right_score = right_count / total_political_words
        center_score = center_count / total_political_words
        
        # Determine leaning
        if left_score > right_score and left_score > center_score:
            leaning = "left"
            confidence = left_score
        elif right_score > left_score and right_score > center_score:
            leaning = "right"
            confidence = right_score
        elif center_score > 0.3:
            leaning = "center"
            confidence = center_score
        else:
            leaning = "neutral"
            confidence = 0.5
        
        # Detect specific phrases
        detected_phrases = []
        for phrase in self.left_leaning_words:
            if phrase in text_lower:
                detected_phrases.append(f"LEFT: {phrase}")
        for phrase in self.right_leaning_words:
            if phrase in text_lower:
                detected_phrases.append(f"RIGHT: {phrase}")
        for phrase in self.center_words:
            if phrase in text_lower:
                detected_phrases.append(f"CENTER: {phrase}")
        
        return {
            "leaning": leaning,
            "confidence": round(confidence, 3),
            "left_score": round(left_score, 3),
            "right_score": round(right_score, 3),
            "center_score": round(center_score, 3),
            "detected_phrases": detected_phrases[:10]  # Limit to top 10
        }
    
    def _analyze_loaded_language(self, text_lower: str, words: List[str]) -> Dict[str, Any]:
        """Analyze loaded language usage"""
        
        positive_count = sum(1 for word in self.loaded_positive if word in text_lower)
        negative_count = sum(1 for word in self.loaded_negative if word in text_lower)
        sensational_count = sum(1 for word in self.sensational_words if word in text_lower)
        
        total_words = len(words)
        
        # Calculate ratios
        positive_ratio = positive_count / max(total_words, 1)
        negative_ratio = negative_count / max(total_words, 1)
        sensational_ratio = sensational_count / max(total_words, 1)
        
        # Overall loaded language score
        loaded_score = (positive_ratio + negative_ratio + sensational_ratio * 1.5)
        
        # Find specific loaded words
        detected_words = []
        for word in self.loaded_positive:
            if word in text_lower:
                detected_words.append(f"POSITIVE: {word}")
        for word in self.loaded_negative:
            if word in text_lower:
                detected_words.append(f"NEGATIVE: {word}")
        for word in self.sensational_words:
            if word in text_lower:
                detected_words.append(f"SENSATIONAL: {word}")
        
        return {
            "loaded_score": round(loaded_score, 3),
            "positive_ratio": round(positive_ratio, 3),
            "negative_ratio": round(negative_ratio, 3),
            "sensational_ratio": round(sensational_ratio, 3),
            "detected_words": detected_words[:15]  # Limit to top 15
        }
    
    def _analyze_subjectivity(self, text: str) -> Dict[str, Any]:
        """Analyze subjectivity using TextBlob"""
        
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            # Subjectivity ranges from 0 (objective) to 1 (subjective)
            subjectivity = sentiment.subjectivity
            
            # Classify subjectivity level
            if subjectivity < 0.3:
                level = "objective"
            elif subjectivity < 0.7:
                level = "mixed"
            else:
                level = "subjective"
            
            return {
                "subjectivity_score": round(subjectivity, 3),
                "subjectivity_level": level,
                "polarity": round(sentiment.polarity, 3)  # -1 (negative) to 1 (positive)
            }
            
        except Exception as e:
            logger.error(f"Error in subjectivity analysis: {e}")
            return {
                "subjectivity_score": 0.5,
                "subjectivity_level": "mixed",
                "polarity": 0.0,
                "error": "TextBlob analysis failed"
            }
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Detailed sentiment analysis"""
        
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            polarity = sentiment.polarity
            
            # Classify sentiment
            if polarity > 0.3:
                sentiment_label = "positive"
            elif polarity < -0.3:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            # Calculate intensity
            intensity = abs(polarity)
            
            return {
                "sentiment_label": sentiment_label,
                "polarity": round(polarity, 3),
                "intensity": round(intensity, 3),
                "confidence": round(intensity, 3)
            }
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                "sentiment_label": "neutral",
                "polarity": 0.0,
                "intensity": 0.0,
                "confidence": 0.0,
                "error": "Sentiment analysis failed"
            }
    
    def _analyze_clickbait(self, text_lower: str) -> Dict[str, Any]:
        """Analyze clickbait characteristics"""
        
        clickbait_patterns = [
            r'\d+\s+(ways|things|reasons|facts|secrets)',
            r'you\s+won\'?t\s+believe',
            r'this\s+will\s+change\s+your\s+life',
            r'the\s+(secret|truth|reason)\s+(about|behind)',
            r'what\s+(happens|happened)\s+next',
            r'(shocking|unbelievable|incredible|amazing)',
            r'number\s+\d+\s+(will|is)',
            r'(don\'?t|never)\s+\w+\s+(again|before)',
            r'(only|just)\s+\d+\s+(percent|%)',
            r'(breaking|exclusive)\s*:',
        ]
        
        clickbait_score = 0
        matched_patterns = []
        
        for pattern in clickbait_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                clickbait_score += len(matches)
                matched_patterns.extend([pattern] * len(matches))
        
        # Check for excessive punctuation
        exclamation_count = text_lower.count('!')
        question_count = text_lower.count('?')
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        # Additional clickbait indicators
        if exclamation_count > 2:
            clickbait_score += 1
        if question_count > 1:
            clickbait_score += 0.5
        if caps_ratio > 0.3:
            clickbait_score += 0.5
        
        # Normalize score
        normalized_score = min(1.0, clickbait_score / 5.0)
        
        # Classify clickbait level
        if normalized_score > 0.7:
            level = "high"
        elif normalized_score > 0.3:
            level = "medium"
        else:
            level = "low"
        
        return {
            "clickbait_score": round(normalized_score, 3),
            "clickbait_level": level,
            "exclamation_count": exclamation_count,
            "question_count": question_count,
            "caps_ratio": round(caps_ratio, 3),
            "matched_patterns": matched_patterns[:5]
        }
    
    def _calculate_overall_bias(self, political_bias, loaded_language, subjectivity, clickbait) -> Dict[str, Any]:
        """Calculate overall bias score"""
        
        # Weight different components
        political_weight = 0.3
        loaded_language_weight = 0.3
        subjectivity_weight = 0.2
        clickbait_weight = 0.2
        
        # Calculate weighted scores
        political_score = political_bias["confidence"] * political_weight
        loaded_score = loaded_language["loaded_score"] * loaded_language_weight
        subjectivity_score = subjectivity["subjectivity_score"] * subjectivity_weight
        clickbait_score = clickbait["clickbait_score"] * clickbait_weight
        
        # Overall bias score
        overall_score = political_score + loaded_score + subjectivity_score + clickbait_score
        
        # Determine bias level
        if overall_score > 0.7:
            level = "extreme"
        elif overall_score > 0.5:
            level = "high"
        elif overall_score > 0.3:
            level = "medium"
        elif overall_score > 0.1:
            level = "low"
        else:
            level = "minimal"
        
        # Collect indicators
        indicators = []
        
        if political_bias["confidence"] > 0.5:
            indicators.append(f"Political bias: {political_bias['leaning']}")
        
        if loaded_language["loaded_score"] > 0.3:
            indicators.append("Loaded language detected")
        
        if subjectivity["subjectivity_score"] > 0.7:
            indicators.append("Highly subjective content")
        
        if clickbait["clickbait_score"] > 0.5:
            indicators.append("Clickbait characteristics")
        
        return {
            "score": round(overall_score, 3),
            "level": level,
            "indicators": indicators
        }
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback analysis when main analysis fails"""
        
        return {
            "political_bias": {
                "leaning": "neutral",
                "confidence": 0.0,
                "left_score": 0.0,
                "right_score": 0.0,
                "center_score": 0.0,
                "detected_phrases": []
            },
            "loaded_language": {
                "loaded_score": 0.0,
                "positive_ratio": 0.0,
                "negative_ratio": 0.0,
                "sensational_ratio": 0.0,
                "detected_words": []
            },
            "subjectivity": {
                "subjectivity_score": 0.5,
                "subjectivity_level": "mixed",
                "polarity": 0.0
            },
            "sentiment": {
                "sentiment_label": "neutral",
                "polarity": 0.0,
                "intensity": 0.0,
                "confidence": 0.0
            },
            "clickbait": {
                "clickbait_score": 0.0,
                "clickbait_level": "low",
                "exclamation_count": 0,
                "question_count": 0,
                "caps_ratio": 0.0,
                "matched_patterns": []
            },
            "overall_bias_score": 0.0,
            "bias_level": "minimal",
            "bias_indicators": ["Analysis failed - using fallback"],
            "error": "Main bias analysis failed"
        }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        
        return {
            "type": "rule_based_bias_detection",
            "initialized": self._initialized,
            "features": [
                "political_bias",
                "loaded_language",
                "subjectivity",
                "sentiment",
                "clickbait_detection"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the bias detector"""
        
        if not self._initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test with sample text
            test_text = "This is a neutral test sentence for health check."
            result = await self.analyze(test_text)
            
            return {
                "status": "healthy",
                "test_result": result
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
