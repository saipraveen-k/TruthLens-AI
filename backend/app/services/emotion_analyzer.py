import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import logging
from typing import Dict, Any, List
import re
from collections import Counter

logger = logging.getLogger(__name__)


class EmotionAnalyzer:
    """Analyzes emotional content and manipulation in text"""
    
    def __init__(self):
        self.model_name = "j-hartmann/emotion-english-distilroberta-base"
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = 512
        self._initialized = False
        
        # Emotion labels for the model
        self.emotion_labels = [
            "anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"
        ]
        
        # Manipulation indicators
        self.fear_inducing_words = [
            "dangerous", "threat", "crisis", "emergency", "warning", "alert",
            "scary", "terrifying", "horrifying", "deadly", "fatal", "catastrophic",
            "disaster", "panic", "chaos", "collapse", "breakdown"
        ]
        
        self.anger_inducing_words = [
            "outrageous", "unacceptable", "disgusting", "appalling", "shocking",
            "infuriating", "enraging", "outrage", "furious", "angry", "mad",
            "disgraceful", "shameful", "horrible", "terrible", "awful"
        ]
        
        self.joy_inducing_words = [
            "amazing", "wonderful", "fantastic", "incredible", "awesome",
            "beautiful", "perfect", "excellent", "brilliant", "outstanding",
            "miracle", "breakthrough", "victory", "triumph", "success"
        ]
        
        self.manipulation_patterns = [
            r"you\s+(must|have to|need to|should)",
            r"everyone\s+(knows|believes|thinks)",
            r"(no one|nobody)\s+(wants|likes|cares)",
            r"the\s+(truth|fact|reality)\s+is",
            r"don\'?t\s+be\s+(fooled|tricked|deceived)",
            r"(wake up|open your eyes)",
            r"(they|the government|the media)\s+(don\'?t|won\'?t)",
            r"(secret|hidden|covered up)\s+(truth|information)"
        ]
    
    async def initialize(self):
        """Initialize the emotion analysis model"""
        if self._initialized:
            return
        
        try:
            logger.info("Initializing Emotion Analyzer...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            
            # Move model to device
            self.model.to(self.device)
            self.model.eval()
            
            self._initialized = True
            logger.info("Emotion Analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Emotion Analyzer: {e}")
            # Continue with rule-based analysis
            self._initialized = True
            logger.warning("Emotion Analyzer initialized in rule-based mode")
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze emotional content and manipulation"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # Try model-based analysis first
            if self.model and self.tokenizer:
                emotion_result = await self._analyze_with_model(text)
            else:
                emotion_result = await self._analyze_emotions_rule_based(text)
            
            # Analyze manipulation indicators
            manipulation_result = await self._analyze_manipulation(text)
            
            # Analyze emotional intensity
            intensity_result = await self._analyze_emotional_intensity(text)
            
            # Calculate overall manipulation score
            overall_manipulation = self._calculate_manipulation_score(
                emotion_result, manipulation_result, intensity_result
            )
            
            return {
                "emotions": emotion_result,
                "manipulation": manipulation_result,
                "intensity": intensity_result,
                "overall_manipulation_score": overall_manipulation["score"],
                "manipulation_level": overall_manipulation["level"],
                "manipulation_indicators": overall_manipulation["indicators"]
            }
            
        except Exception as e:
            logger.error(f"Error in emotion analysis: {e}")
            return self._fallback_analysis(text)
    
    async def _analyze_with_model(self, text: str) -> Dict[str, Any]:
        """Analyze emotions using the transformer model"""
        
        # Tokenize input
        inputs = self.tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=-1)
        
        # Extract emotion probabilities
        emotion_probs = probabilities[0].cpu().numpy()
        emotion_scores = {}
        
        for i, emotion in enumerate(self.emotion_labels):
            emotion_scores[emotion] = float(emotion_probs[i])
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[dominant_emotion]
        
        # Calculate emotional diversity (entropy)
        entropy = -sum(p * np.log2(p) for p in emotion_probs if p > 0)
        max_entropy = np.log2(len(self.emotion_labels))
        emotional_diversity = entropy / max_entropy
        
        return {
            "dominant_emotion": dominant_emotion,
            "confidence": round(confidence, 3),
            "emotion_scores": {k: round(v, 3) for k, v in emotion_scores.items()},
            "emotional_diversity": round(emotional_diversity, 3),
            "method": "transformer_model"
        }
    
    async def _analyze_emotions_rule_based(self, text: str) -> Dict[str, Any]:
        """Rule-based emotion analysis as fallback"""
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Count emotion-inducing words
        fear_count = sum(1 for word in self.fear_inducing_words if word in text_lower)
        anger_count = sum(1 for word in self.anger_inducing_words if word in text_lower)
        joy_count = sum(1 for word in self.joy_inducing_words if word in text_lower)
        
        total_emotion_words = fear_count + anger_count + joy_count
        
        if total_emotion_words == 0:
            return {
                "dominant_emotion": "neutral",
                "confidence": 0.8,
                "emotion_scores": {
                    "anger": 0.0,
                    "disgust": 0.0,
                    "fear": 0.0,
                    "joy": 0.0,
                    "neutral": 1.0,
                    "sadness": 0.0,
                    "surprise": 0.0
                },
                "emotional_diversity": 0.0,
                "method": "rule_based"
            }
        
        # Calculate normalized scores
        fear_score = fear_count / total_emotion_words
        anger_score = anger_count / total_emotion_words
        joy_score = joy_count / total_emotion_words
        neutral_score = max(0, 1 - total_emotion_words / len(words))
        
        # Find dominant emotion
        emotion_scores = {
            "anger": anger_score,
            "disgust": 0.0,
            "fear": fear_score,
            "joy": joy_score,
            "neutral": neutral_score,
            "sadness": 0.0,
            "surprise": 0.0
        }
        
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[dominant_emotion]
        
        return {
            "dominant_emotion": dominant_emotion,
            "confidence": round(confidence, 3),
            "emotion_scores": {k: round(v, 3) for k, v in emotion_scores.items()},
            "emotional_diversity": len([s for s in emotion_scores.values() if s > 0.1]) / len(emotion_scores),
            "method": "rule_based"
        }
    
    async def _analyze_manipulation(self, text: str) -> Dict[str, Any]:
        """Analyze manipulation techniques"""
        
        text_lower = text.lower()
        
        # Check for manipulation patterns
        pattern_matches = []
        for pattern in self.manipulation_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                pattern_matches.append({
                    "pattern": pattern,
                    "matches": len(matches),
                    "type": "psychological_manipulation"
                })
        
        # Check for emotional manipulation
        fear_words_found = [word for word in self.fear_inducing_words if word in text_lower]
        anger_words_found = [word for word in self.anger_inducing_words if word in text_lower]
        
        # Check for authority appeals
        authority_patterns = [
            r"experts\s+(say|claim|believe)",
            r"scientists\s+(have found|prove|show)",
            r"studies\s+(show|prove|demonstrate)",
            r"research\s+(indicates|suggests|confirms)",
            r"according to\s+(experts|scientists|research)"
        ]
        
        authority_matches = []
        for pattern in authority_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                authority_matches.append({
                    "pattern": pattern,
                    "matches": len(matches),
                    "type": "authority_appeal"
                })
        
        # Check for urgency/scarcity
        urgency_patterns = [
            r"(act now|don\'?t wait|immediate)",
            r"(limited time|only \d+ left|running out)",
            r"(urgent|emergency|critical)",
            r"(before it\'?s too late|while you still can)"
        ]
        
        urgency_matches = []
        for pattern in urgency_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                urgency_matches.append({
                    "pattern": pattern,
                    "matches": len(matches),
                    "type": "urgency_scarcity"
                })
        
        # Calculate manipulation scores
        pattern_score = min(1.0, len(pattern_matches) / 3.0)
        emotional_score = min(1.0, (len(fear_words_found) + len(anger_words_found)) / 5.0)
        authority_score = min(1.0, len(authority_matches) / 2.0)
        urgency_score = min(1.0, len(urgency_matches) / 2.0)
        
        overall_score = (pattern_score + emotional_score + authority_score + urgency_score) / 4.0
        
        return {
            "manipulation_score": round(overall_score, 3),
            "pattern_matches": pattern_matches,
            "emotional_manipulation": {
                "fear_words": fear_words_found[:10],
                "anger_words": anger_words_found[:10],
                "score": round(emotional_score, 3)
            },
            "authority_appeals": authority_matches,
            "urgency_scarcity": urgency_matches,
            "detected_techniques": [
                "psychological_manipulation" if pattern_matches else None,
                "emotional_manipulation" if emotional_score > 0.3 else None,
                "authority_appeal" if authority_matches else None,
                "urgency_scarcity" if urgency_matches else None
            ]
        }
    
    async def _analyze_emotional_intensity(self, text: str) -> Dict[str, Any]:
        """Analyze emotional intensity and variability"""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {
                "intensity_score": 0.0,
                "variability_score": 0.0,
                "peak_emotion": "neutral",
                "sentence_count": 0
            }
        
        # Analyze each sentence's emotion
        sentence_emotions = []
        for sentence in sentences:
            if self.model and self.tokenizer:
                try:
                    result = await self._analyze_with_model(sentence)
                    sentence_emotions.append(result)
                except:
                    # Fallback to rule-based for individual sentences
                    result = await self._analyze_emotions_rule_based(sentence)
                    sentence_emotions.append(result)
            else:
                result = await self._analyze_emotions_rule_based(sentence)
                sentence_emotions.append(result)
        
        # Calculate intensity metrics
        intensities = [s["confidence"] for s in sentence_emotions]
        intensity_score = np.mean(intensities)
        
        # Calculate variability (standard deviation)
        variability_score = np.std(intensities) if len(intensities) > 1 else 0.0
        
        # Find peak emotion
        peak_sentence = max(sentence_emotions, key=lambda s: s["confidence"])
        peak_emotion = peak_sentence["dominant_emotion"]
        
        return {
            "intensity_score": round(intensity_score, 3),
            "variability_score": round(variability_score, 3),
            "peak_emotion": peak_emotion,
            "sentence_count": len(sentences),
            "emotion_distribution": {
                emotion: sum(1 for s in sentence_emotions if s["dominant_emotion"] == emotion)
                for emotion in self.emotion_labels
            }
        }
    
    def _calculate_manipulation_score(self, emotions, manipulation, intensity) -> Dict[str, Any]:
        """Calculate overall manipulation score"""
        
        # Weight different components
        emotion_weight = 0.3
        manipulation_weight = 0.4
        intensity_weight = 0.3
        
        # Extract scores
        emotion_score = emotions.get("confidence", 0)
        if emotions.get("dominant_emotion") in ["fear", "anger"]:
            emotion_score *= 1.5  # Higher weight for negative emotions
        
        manipulation_pattern_score = manipulation.get("manipulation_score", 0)
        intensity_score = intensity.get("intensity_score", 0)
        variability_score = intensity.get("variability_score", 0)
        
        # Calculate weighted score
        overall_score = (
            emotion_score * emotion_weight +
            manipulation_pattern_score * manipulation_weight +
            (intensity_score + variability_score) / 2 * intensity_weight
        )
        
        # Normalize to 0-1 range
        overall_score = min(1.0, overall_score)
        
        # Determine manipulation level
        if overall_score > 0.8:
            level = "very_high"
        elif overall_score > 0.6:
            level = "high"
        elif overall_score > 0.4:
            level = "medium"
        elif overall_score > 0.2:
            level = "low"
        else:
            level = "minimal"
        
        # Collect indicators
        indicators = []
        
        if emotions.get("dominant_emotion") in ["fear", "anger"]:
            indicators.append(f"Negative emotional manipulation: {emotions['dominant_emotion']}")
        
        if manipulation.get("manipulation_score", 0) > 0.5:
            indicators.append("Psychological manipulation techniques detected")
        
        if intensity.get("intensity_score", 0) > 0.7:
            indicators.append("High emotional intensity")
        
        if len(manipulation.get("detected_techniques", [])) > 2:
            indicators.append("Multiple manipulation techniques used")
        
        return {
            "score": round(overall_score, 3),
            "level": level,
            "indicators": indicators
        }
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback analysis when main analysis fails"""
        
        return {
            "emotions": {
                "dominant_emotion": "neutral",
                "confidence": 0.5,
                "emotion_scores": {
                    "anger": 0.0,
                    "disgust": 0.0,
                    "fear": 0.0,
                    "joy": 0.0,
                    "neutral": 1.0,
                    "sadness": 0.0,
                    "surprise": 0.0
                },
                "emotional_diversity": 0.0,
                "method": "fallback"
            },
            "manipulation": {
                "manipulation_score": 0.0,
                "pattern_matches": [],
                "emotional_manipulation": {
                    "fear_words": [],
                    "anger_words": [],
                    "score": 0.0
                },
                "authority_appeals": [],
                "urgency_scarcity": [],
                "detected_techniques": []
            },
            "intensity": {
                "intensity_score": 0.0,
                "variability_score": 0.0,
                "peak_emotion": "neutral",
                "sentence_count": 0
            },
            "overall_manipulation_score": 0.0,
            "manipulation_level": "minimal",
            "manipulation_indicators": ["Analysis failed - using fallback"],
            "error": "Main emotion analysis failed"
        }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        
        return {
            "model_name": self.model_name,
            "device": str(self.device),
            "max_length": self.max_length,
            "initialized": self._initialized,
            "emotion_labels": self.emotion_labels,
            "type": "emotion_classification"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the emotion analyzer"""
        
        if not self._initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test with sample text
            test_text = "This is a neutral test sentence for health check."
            result = await self.analyze(test_text)
            
            return {
                "status": "healthy",
                "test_result": result,
                "device": str(self.device)
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
