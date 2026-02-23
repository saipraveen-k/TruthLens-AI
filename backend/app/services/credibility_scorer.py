import logging
from typing import Dict, Any
import numpy as np

logger = logging.getLogger(__name__)


class CredibilityScorer:
    """Calculates overall credibility score based on multiple factors"""
    
    def __init__(self):
        self._initialized = False
        
        # Scoring weights (can be adjusted)
        self.weights = {
            "fake_news_confidence": 0.40,  # 40% weight
            "bias_score": 0.20,           # 20% weight
            "emotional_manipulation": 0.20, # 20% weight
            "source_reliability": 0.15,   # 15% weight
            "linguistic_quality": 0.05    # 5% weight
        }
        
        # Credibility thresholds
        self.thresholds = {
            "very_low": (0, 40),
            "low": (40, 60),
            "moderate": (60, 80),
            "high": (80, 100)
        }
    
    async def initialize(self):
        """Initialize the credibility scorer"""
        if self._initialized:
            return
        
        logger.info("Initializing Credibility Scorer...")
        self._initialized = True
        logger.info("Credibility Scorer initialized successfully")
    
    async def calculate_score(self, 
                            fake_news_result: Dict[str, Any],
                            bias_result: Dict[str, Any], 
                            emotion_result: Dict[str, Any],
                            source_reliability: float = 50.0) -> Dict[str, Any]:
        """Calculate overall credibility score"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # Extract individual scores
            fake_news_score = self._calculate_fake_news_score(fake_news_result)
            bias_score = self._calculate_bias_score(bias_result)
            emotion_score = self._calculate_emotion_score(emotion_result)
            source_score = source_reliability
            linguistic_score = self._calculate_linguistic_score(fake_news_result, bias_result)
            
            # Calculate weighted credibility score
            credibility_score = (
                fake_news_score * self.weights["fake_news_confidence"] +
                bias_score * self.weights["bias_score"] +
                emotion_score * self.weights["emotional_manipulation"] +
                source_score * self.weights["source_reliability"] +
                linguistic_score * self.weights["linguistic_quality"]
            )
            
            # Ensure score is within 0-100 range
            credibility_score = max(0, min(100, credibility_score))
            
            # Determine credibility level
            credibility_level = self._get_credibility_level(credibility_score)
            
            # Calculate fake probability (inverse of credibility)
            fake_probability = 100 - credibility_score
            
            # Determine bias and emotional manipulation levels
            bias_level = self._get_bias_level(bias_result.get("overall_bias_score", 0))
            emotion_level = self._get_emotion_level(emotion_result.get("overall_manipulation_score", 0))
            source_level = self._get_source_level(source_score)
            
            # Generate detailed breakdown
            breakdown = {
                "fake_news_detection": {
                    "score": round(fake_news_score, 2),
                    "weight": self.weights["fake_news_confidence"],
                    "contribution": round(fake_news_score * self.weights["fake_news_confidence"], 2)
                },
                "bias_analysis": {
                    "score": round(bias_score, 2),
                    "weight": self.weights["bias_score"],
                    "contribution": round(bias_score * self.weights["bias_score"], 2)
                },
                "emotional_manipulation": {
                    "score": round(emotion_score, 2),
                    "weight": self.weights["emotional_manipulation"],
                    "contribution": round(emotion_score * self.weights["emotional_manipulation"], 2)
                },
                "source_reliability": {
                    "score": round(source_score, 2),
                    "weight": self.weights["source_reliability"],
                    "contribution": round(source_score * self.weights["source_reliability"], 2)
                },
                "linguistic_quality": {
                    "score": round(linguistic_score, 2),
                    "weight": self.weights["linguistic_quality"],
                    "contribution": round(linguistic_score * self.weights["linguistic_quality"], 2)
                }
            }
            
            # Risk factors
            risk_factors = self._identify_risk_factors(
                fake_news_result, bias_result, emotion_result
            )
            
            # Recommendations
            recommendations = self._generate_recommendations(
                credibility_score, fake_news_result, bias_result, emotion_result
            )
            
            return {
                "credibility_score": round(credibility_score, 2),
                "fake_probability": round(fake_probability, 2),
                "credibility_level": credibility_level,
                "bias_score": round(bias_result.get("overall_bias_score", 0) * 100, 2),
                "bias_level": bias_level,
                "emotional_manipulation": round(emotion_result.get("overall_manipulation_score", 0) * 100, 2),
                "emotional_manipulation_level": emotion_level,
                "source_reliability": round(source_score, 2),
                "source_reliability_level": source_level,
                "breakdown": breakdown,
                "risk_factors": risk_factors,
                "recommendations": recommendations,
                "confidence": self._calculate_overall_confidence(
                    fake_news_result, bias_result, emotion_result
                )
            }
            
        except Exception as e:
            logger.error(f"Error in credibility scoring: {e}")
            return self._fallback_scoring()
    
    def _calculate_fake_news_score(self, fake_news_result: Dict[str, Any]) -> float:
        """Calculate score from fake news detection"""
        
        # Get real probability (inverse of fake probability)
        real_probability = fake_news_result.get("real_probability", 0.5)
        confidence = fake_news_result.get("confidence", 0.5)
        
        # Adjust score based on confidence
        if confidence > 0.8:
            score = real_probability * 100
        elif confidence > 0.6:
            score = real_probability * 90 + 5  # Small penalty for lower confidence
        else:
            score = real_probability * 80 + 10  # Larger penalty for low confidence
        
        # Consider linguistic indicators
        clickbait_score = fake_news_result.get("clickbait_score", 0)
        sensationalism_score = fake_news_result.get("sensationalism_score", 0)
        
        # Penalize for high clickbait/sensationalism
        penalty = (clickbait_score + sensationalism_score) * 20
        score = max(0, score - penalty)
        
        return score
    
    def _calculate_bias_score(self, bias_result: Dict[str, Any]) -> float:
        """Calculate score from bias analysis"""
        
        bias_score = bias_result.get("overall_bias_score", 0)
        
        # Convert bias score to credibility score (inverse relationship)
        # Lower bias = higher credibility
        credibility_score = (1 - bias_score) * 100
        
        # Consider subjectivity
        subjectivity = bias_result.get("subjectivity", {}).get("subjectivity_score", 0.5)
        
        # Penalize for high subjectivity
        if subjectivity > 0.7:
            credibility_score *= 0.8
        elif subjectivity > 0.5:
            credibility_score *= 0.9
        
        # Consider clickbait
        clickbait_score = bias_result.get("clickbait", {}).get("clickbait_score", 0)
        if clickbait_score > 0.5:
            credibility_score *= 0.85
        
        return max(0, credibility_score)
    
    def _calculate_emotion_score(self, emotion_result: Dict[str, Any]) -> float:
        """Calculate score from emotion analysis"""
        
        manipulation_score = emotion_result.get("overall_manipulation_score", 0)
        
        # Convert manipulation score to credibility score (inverse relationship)
        credibility_score = (1 - manipulation_score) * 100
        
        # Consider emotional intensity
        intensity = emotion_result.get("intensity", {}).get("intensity_score", 0)
        
        # Penalize for very high intensity
        if intensity > 0.8:
            credibility_score *= 0.8
        elif intensity > 0.6:
            credibility_score *= 0.9
        
        # Consider dominant emotion
        dominant_emotion = emotion_result.get("emotions", {}).get("dominant_emotion", "neutral")
        if dominant_emotion in ["fear", "anger"]:
            credibility_score *= 0.85  # Penalty for negative emotions
        
        return max(0, credibility_score)
    
    def _calculate_linguistic_score(self, fake_news_result: Dict[str, Any], bias_result: Dict[str, Any]) -> float:
        """Calculate linguistic quality score"""
        
        score = 50.0  # Base score
        
        # Authority indicators
        authority_score = fake_news_result.get("authority_score", 0)
        score += authority_score * 30
        
        # Uncertainty indicators
        uncertainty_score = fake_news_result.get("uncertainty_score", 0)
        score -= uncertainty_score * 20
        
        # Loaded language
        loaded_score = bias_result.get("loaded_language", {}).get("loaded_score", 0)
        score -= loaded_score * 25
        
        # Ensure score is within valid range
        return max(0, min(100, score))
    
    def _get_credibility_level(self, score: float) -> str:
        """Determine credibility level based on score"""
        
        for level, (min_score, max_score) in self.thresholds.items():
            if min_score <= score < max_score:
                return level.replace("_", " ").title()
        
        return "High"
    
    def _get_bias_level(self, bias_score: float) -> str:
        """Determine bias level"""
        
        if bias_score > 0.7:
            return "Extreme"
        elif bias_score > 0.5:
            return "High"
        elif bias_score > 0.3:
            return "Medium"
        elif bias_score > 0.1:
            return "Low"
        else:
            return "Minimal"
    
    def _get_emotion_level(self, emotion_score: float) -> str:
        """Determine emotional manipulation level"""
        
        if emotion_score > 0.7:
            return "Very High"
        elif emotion_score > 0.5:
            return "High"
        elif emotion_score > 0.3:
            return "Medium"
        elif emotion_score > 0.1:
            return "Low"
        else:
            return "Minimal"
    
    def _get_source_level(self, source_score: float) -> str:
        """Determine source reliability level"""
        
        if source_score >= 80:
            return "High"
        elif source_score >= 60:
            return "Medium"
        elif source_score >= 40:
            return "Low"
        else:
            return "Very Low"
    
    def _identify_risk_factors(self, fake_news_result, bias_result, emotion_result) -> list:
        """Identify specific risk factors"""
        
        risk_factors = []
        
        # Fake news risk factors
        if fake_news_result.get("fake_probability", 0) > 0.7:
            risk_factors.append("High probability of being fake news")
        
        if fake_news_result.get("clickbait_score", 0) > 0.5:
            risk_factors.append("Clickbait characteristics detected")
        
        # Bias risk factors
        bias_level = bias_result.get("bias_level", "")
        if bias_level in ["extreme", "high"]:
            risk_factors.append(f"Strong {bias_result.get('political_bias', {}).get('leaning', 'political')} bias detected")
        
        if bias_result.get("subjectivity", {}).get("subjectivity_score", 0) > 0.7:
            risk_factors.append("Highly subjective content")
        
        # Emotion risk factors
        emotion_level = emotion_result.get("manipulation_level", "")
        if emotion_level in ["very_high", "high"]:
            risk_factors.append("Strong emotional manipulation detected")
        
        dominant_emotion = emotion_result.get("emotions", {}).get("dominant_emotion", "")
        if dominant_emotion in ["fear", "anger"]:
            risk_factors.append(f"Uses {dominant_emotion}-inducing language")
        
        return risk_factors
    
    def _generate_recommendations(self, credibility_score, fake_news_result, bias_result, emotion_result) -> list:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        
        if credibility_score < 40:
            recommendations.append("This content appears highly unreliable. Verify with trusted sources before sharing.")
            recommendations.append("Consider checking fact-checking websites for claims made in this article.")
        elif credibility_score < 60:
            recommendations.append("This content shows some credibility concerns. Seek additional sources.")
            recommendations.append("Be cautious about sharing without verification.")
        elif credibility_score < 80:
            recommendations.append("This content appears moderately credible but has some limitations.")
            recommendations.append("Cross-reference with other reputable sources for complete understanding.")
        else:
            recommendations.append("This content appears generally credible.")
            recommendations.append("Still consider the source and context when evaluating.")
        
        # Specific recommendations based on analysis
        if fake_news_result.get("clickbait_score", 0) > 0.5:
            recommendations.append("Be wary of clickbait headlines that may exaggerate or mislead.")
        
        if bias_result.get("overall_bias_score", 0) > 0.5:
            recommendations.append("Consider the political perspective and look for balanced coverage.")
        
        if emotion_result.get("overall_manipulation_score", 0) > 0.5:
            recommendations.append("Be aware of emotional manipulation tactics that may influence judgment.")
        
        return recommendations
    
    def _calculate_overall_confidence(self, fake_news_result, bias_result, emotion_result) -> float:
        """Calculate overall confidence in the analysis"""
        
        # Get individual confidences
        fake_confidence = fake_news_result.get("confidence", 0.5)
        bias_confidence = 0.7  # Rule-based, moderate confidence
        emotion_confidence = emotion_result.get("emotions", {}).get("confidence", 0.5)
        
        # Weighted average
        overall_confidence = (
            fake_confidence * 0.5 +
            bias_confidence * 0.3 +
            emotion_confidence * 0.2
        )
        
        return round(overall_confidence, 3)
    
    def _fallback_scoring(self) -> Dict[str, Any]:
        """Fallback scoring when main analysis fails"""
        
        return {
            "credibility_score": 50.0,
            "fake_probability": 50.0,
            "credibility_level": "Moderate",
            "bias_score": 50.0,
            "bias_level": "Medium",
            "emotional_manipulation": 50.0,
            "emotional_manipulation_level": "Medium",
            "source_reliability": 50.0,
            "source_reliability_level": "Medium",
            "breakdown": {},
            "risk_factors": ["Analysis failed - using default scores"],
            "recommendations": ["Manual verification recommended due to analysis failure"],
            "confidence": 0.1,
            "error": "Main credibility scoring failed"
        }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        
        return {
            "type": "rule_based_credibility_scoring",
            "initialized": self._initialized,
            "weights": self.weights,
            "thresholds": self.thresholds
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the credibility scorer"""
        
        if not self._initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test with sample data
            test_fake_news = {"prediction": "real", "confidence": 0.8, "real_probability": 0.8}
            test_bias = {"overall_bias_score": 0.2}
            test_emotion = {"overall_manipulation_score": 0.1}
            
            result = await self.calculate_score(test_fake_news, test_bias, test_emotion)
            
            return {
                "status": "healthy",
                "test_result": result
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
