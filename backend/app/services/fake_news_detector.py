import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class FakeNewsDetector:
    """BERT-based fake news detection model"""
    
    def __init__(self):
        self.model_name = "bert-base-uncased"
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = 512
        self._initialized = False
    
    async def initialize(self):
        """Initialize the BERT model and tokenizer"""
        if self._initialized:
            return
        
        try:
            logger.info("Initializing Fake News Detector...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Load model
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=2  # Binary classification: real/fake
            )
            
            # Move model to device
            self.model.to(self.device)
            self.model.eval()
            
            # Try to load fine-tuned weights if available
            model_path = os.getenv("BERT_MODEL_PATH", "./models_training/saved_models/bert_fake_news.pt")
            if os.path.exists(model_path):
                logger.info(f"Loading fine-tuned model from {model_path}")
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            else:
                logger.warning("Fine-tuned model not found, using pre-trained BERT")
            
            self._initialized = True
            logger.info("Fake News Detector initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Fake News Detector: {e}")
            raise
    
    async def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text for fake news probability"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
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
            
            # Extract results
            fake_prob = probabilities[0][1].item()  # Probability of being fake
            real_prob = probabilities[0][0].item()  # Probability of being real
            
            prediction = "fake" if fake_prob > 0.5 else "real"
            confidence = max(fake_prob, real_prob)
            
            # Additional analysis features
            result = {
                "prediction": prediction,
                "confidence": round(confidence, 3),
                "fake_probability": round(fake_prob, 3),
                "real_probability": round(real_prob, 3),
                "model": "bert",
                "threshold": 0.5
            }
            
            # Add linguistic indicators
            result.update(self._analyze_linguistic_features(text))
            
            return result
            
        except Exception as e:
            logger.error(f"Error in fake news analysis: {e}")
            # Fallback to rule-based analysis
            return self._fallback_analysis(text)
    
    def _analyze_linguistic_features(self, text: str) -> Dict[str, Any]:
        """Analyze linguistic features associated with fake news"""
        
        features = {}
        
        # Clickbait indicators
        clickbait_words = [
            "shocking", "unbelievable", "miracle", "breakthrough", "secret",
            "revealed", "exposed", "conspiracy", "cover-up", "scandal"
        ]
        
        text_lower = text.lower()
        clickbait_count = sum(1 for word in clickbait_words if word in text_lower)
        features["clickbait_score"] = min(1.0, clickbait_count / 5.0)
        
        # Sensationalism indicators
        sensational_words = [
            "amazing", "incredible", "stunning", "mind-blowing", "life-changing",
            "revolutionary", "game-changing", "historic", "unprecedented"
        ]
        
        sensational_count = sum(1 for word in sensational_words if word in text_lower)
        features["sensationalism_score"] = min(1.0, sensational_count / 5.0)
        
        # Uncertainty indicators
        uncertainty_words = [
            "might", "could", "perhaps", "maybe", "allegedly", "reportedly",
            "supposedly", "claims", "suggests", "rumored"
        ]
        
        uncertainty_count = sum(1 for word in uncertainty_words if word in text_lower)
        word_count = len(text.split())
        features["uncertainty_score"] = min(1.0, uncertainty_count / max(word_count * 0.1, 1))
        
        # Authority indicators
        authority_words = [
            "expert", "doctor", "scientist", "research", "study", "evidence",
            "proof", "confirmed", "verified", "official"
        ]
        
        authority_count = sum(1 for word in authority_words if word in text_lower)
        features["authority_score"] = min(1.0, authority_count / 5.0)
        
        return features
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback rule-based analysis when model is unavailable"""
        
        logger.warning("Using fallback rule-based analysis")
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Fake news indicators
        fake_indicators = [
            "fake news", "conspiracy", "hoax", "satire", "clickbait",
            "unbelievable", "impossible", "miracle cure", "secret revealed"
        ]
        
        # Real news indicators
        real_indicators = [
            "according to", "research shows", "study finds", "expert says",
            "official statement", "confirmed", "verified", "evidence suggests"
        ]
        
        fake_score = sum(1 for indicator in fake_indicators if indicator in text_lower)
        real_score = sum(1 for indicator in real_indicators if indicator in text_lower)
        
        # Calculate probabilities
        total_indicators = fake_score + real_score
        if total_indicators == 0:
            fake_prob = 0.5  # Neutral
        else:
            fake_prob = fake_score / total_indicators
        
        prediction = "fake" if fake_prob > 0.6 else "real"
        confidence = 0.6  # Lower confidence for rule-based
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "fake_probability": round(fake_prob, 3),
            "real_probability": round(1 - fake_prob, 3),
            "model": "rule_based_fallback",
            "threshold": 0.6,
            "note": "Using rule-based analysis due to model unavailability"
        }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        
        return {
            "model_name": self.model_name,
            "device": str(self.device),
            "max_length": self.max_length,
            "initialized": self._initialized,
            "type": "transformer_classification"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the model"""
        
        if not self._initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test with sample text
            test_text = "This is a test sentence for health check."
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
