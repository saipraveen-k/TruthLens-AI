import logging
from typing import Dict, Any, List, Tuple
import re
from collections import Counter
import numpy as np

logger = logging.getLogger(__name__)


class ExplainableAI:
    """Provides explainable AI features for news analysis"""
    
    def __init__(self):
        self._initialized = False
        
        # Suspicious patterns for highlighting
        self.suspicious_patterns = {
            "unsubstantiated_claims": [
                r"(scientists|experts|researchers)\s+(have found|discovered|revealed)",
                r"(studies|research)\s+(show|prove|demonstrate|confirm)",
                r"(according to|based on)\s+(experts|research|studies)",
                r"(evidence|proof|data)\s+(shows|suggests|indicates)"
            ],
            "emotional_manipulation": [
                r"(shocking|terrifying|horrifying|outrageous|disgusting)",
                r"(amazing|incredible|unbelievable|miraculous|extraordinary)",
                r"(dangerous|deadly|fatal|catastrophic|devastating)",
                r"(urgent|emergency|critical|immediate|crisis)"
            ],
            "clickbait_patterns": [
                r"\d+\s+(ways|things|reasons|facts|secrets)",
                r"you\s+(won\'?t|will not)\s+(believe|imagine|guess)",
                r"this\s+(will|would)\s+(change|transform)\s+your\s+life",
                r"the\s+(secret|truth|reason)\s+(about|behind)",
                r"(what|happens|occurs)\s+when\s+you"
            ],
            "authority_appeals": [
                r"(doctors|scientists|experts|researchers)\s+(say|claim|believe)",
                r"(medical|scientific|research)\s+(community|experts)",
                r"(peer-reviewed|published|proven)\s+(research|study|evidence)",
                r"(harvard|stanford|mit|oxford)\s+(researchers|scientists|study)"
            ],
            "conspiracy_indicators": [
                r"(they|the government|the media)\s+(don\'?t|won\'?t|are not)\s+(telling|showing)",
                r"(secret|hidden|covered up|suppressed)\s+(information|truth|evidence)",
                r"(wake up|open your eyes|see the truth)",
                r"(mainstream|establishment|elite)\s+(media|narrative|story)"
            ]
        }
        
        # Explanation templates
        self.explanation_templates = {
            "unsubstantiated_claims": "This sentence makes claims about scientific evidence without providing specific sources or data.",
            "emotional_manipulation": "This sentence uses emotionally charged language to influence your feelings rather than present facts.",
            "clickbait_patterns": "This sentence uses clickbait techniques designed to attract attention rather than inform.",
            "authority_appeals": "This sentence appeals to authority without providing specific credentials or evidence.",
            "conspiracy_indicators": "This sentence contains language commonly associated with conspiracy theories."
        }
    
    async def initialize(self):
        """Initialize the explainable AI component"""
        if self._initialized:
            return
        
        logger.info("Initializing Explainable AI...")
        self._initialized = True
        logger.info("Explainable AI initialized successfully")
    
    async def explain(self, 
                     text: str,
                     fake_news_result: Dict[str, Any],
                     bias_result: Dict[str, Any],
                     emotion_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanations for the analysis results"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # Split text into sentences
            sentences = self._split_sentences(text)
            
            # Analyze each sentence
            sentence_analysis = []
            for i, sentence in enumerate(sentences):
                analysis = await self._analyze_sentence(sentence, i, fake_news_result, bias_result, emotion_result)
                sentence_analysis.append(analysis)
            
            # Generate highlighted text
            highlighted_text = self._generate_highlighted_text(sentences, sentence_analysis)
            
            # Generate overall explanations
            overall_explanations = self._generate_overall_explanations(
                fake_news_result, bias_result, emotion_result
            )
            
            # Generate word importance analysis
            word_importance = self._analyze_word_importance(text, fake_news_result, bias_result, emotion_result)
            
            # Generate comparison with trusted sources (placeholder)
            source_comparison = self._generate_source_comparison(fake_news_result)
            
            return {
                "highlighted_text": highlighted_text,
                "sentence_analysis": sentence_analysis,
                "overall_explanations": overall_explanations,
                "word_importance": word_importance,
                "source_comparison": source_comparison,
                "explanation_summary": self._generate_explanation_summary(sentence_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error in explainable AI analysis: {e}")
            return self._fallback_explanation(text)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        
        # Simple sentence splitting - can be improved with NLTK
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    async def _analyze_sentence(self, 
                               sentence: str, 
                               index: int,
                               fake_news_result: Dict[str, Any],
                               bias_result: Dict[str, Any],
                               emotion_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual sentence for suspicious patterns"""
        
        sentence_lower = sentence.lower()
        
        # Check for suspicious patterns
        detected_patterns = []
        pattern_scores = {}
        
        for pattern_type, patterns in self.suspicious_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, sentence_lower)
                if found:
                    matches.extend(found)
            
            if matches:
                detected_patterns.append({
                    "type": pattern_type,
                    "matches": matches,
                    "explanation": self.explanation_templates.get(pattern_type, "Suspicious pattern detected")
                })
                pattern_scores[pattern_type] = min(1.0, len(matches) * 0.3)
        
        # Calculate sentence suspiciousness score
        suspiciousness_score = sum(pattern_scores.values()) / len(self.suspicious_patterns)
        
        # Check for emotional content
        emotion_words = self._extract_emotion_words(sentence)
        emotion_score = len(emotion_words) / max(len(sentence.split()), 1)
        
        # Check for bias indicators
        bias_words = self._extract_bias_words(sentence)
        bias_score = len(bias_words) / max(len(sentence.split()), 1)
        
        # Overall sentence score
        overall_score = (suspiciousness_score * 0.5 + emotion_score * 0.3 + bias_score * 0.2)
        
        return {
            "sentence_index": index,
            "text": sentence,
            "suspiciousness_score": round(suspiciousness_score, 3),
            "emotion_score": round(emotion_score, 3),
            "bias_score": round(bias_score, 3),
            "overall_score": round(overall_score, 3),
            "detected_patterns": detected_patterns,
            "emotion_words": emotion_words,
            "bias_words": bias_words,
            "is_suspicious": overall_score > 0.3
        }
    
    def _extract_emotion_words(self, sentence: str) -> List[str]:
        """Extract emotion-inducing words from sentence"""
        
        emotion_words = [
            "shocking", "terrifying", "horrifying", "outrageous", "disgusting",
            "amazing", "incredible", "unbelievable", "miraculous", "extraordinary",
            "dangerous", "deadly", "fatal", "catastrophic", "devastating",
            "urgent", "emergency", "critical", "immediate", "crisis",
            "love", "hate", "fear", "anger", "joy", "sadness", "surprise"
        ]
        
        sentence_lower = sentence.lower()
        found_words = [word for word in emotion_words if word in sentence_lower]
        return found_words
    
    def _extract_bias_words(self, sentence: str) -> List[str]:
        """Extract bias-indicating words from sentence"""
        
        bias_words = [
            "liberal", "conservative", "left", "right", "progressive", "traditional",
            "biased", "unfair", "one-sided", "propaganda", "agenda", "ideology",
            "extremist", "radical", "moderate", "centrist", "neutral", "objective"
        ]
        
        sentence_lower = sentence.lower()
        found_words = [word for word in bias_words if word in sentence_lower]
        return found_words
    
    def _generate_highlighted_text(self, sentences: List[str], sentence_analysis: List[Dict[str, Any]]) -> str:
        """Generate HTML-highlighted text"""
        
        highlighted_parts = []
        
        for sentence, analysis in zip(sentences, sentence_analysis):
            if analysis["is_suspicious"]:
                # Determine highlight color based on score
                score = analysis["overall_score"]
                if score > 0.7:
                    color_class = "suspicious-high"
                elif score > 0.5:
                    color_class = "suspicious-medium"
                else:
                    color_class = "suspicious-low"
                
                highlighted_sentence = f'<mark class="{color_class}" title="{self._generate_tooltip(analysis)}">{sentence}</mark>'
            else:
                highlighted_sentence = sentence
            
            highlighted_parts.append(highlighted_sentence)
        
        return ". ".join(highlighted_parts) + "."
    
    def _generate_tooltip(self, analysis: Dict[str, Any]) -> str:
        """Generate tooltip text for highlighted sentence"""
        
        tooltip_parts = []
        
        if analysis["detected_patterns"]:
            for pattern in analysis["detected_patterns"]:
                tooltip_parts.append(f"• {pattern['explanation']}")
        
        if analysis["emotion_words"]:
            tooltip_parts.append(f"• Contains emotional words: {', '.join(analysis['emotion_words'][:3])}")
        
        if analysis["bias_words"]:
            tooltip_parts.append(f"• Contains bias words: {', '.join(analysis['bias_words'][:3])}")
        
        tooltip_parts.append(f"• Suspiciousness score: {analysis['suspiciousness_score']:.2f}")
        
        return "; ".join(tooltip_parts)
    
    def _generate_overall_explanations(self, 
                                     fake_news_result: Dict[str, Any],
                                     bias_result: Dict[str, Any],
                                     emotion_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall explanations for the analysis"""
        
        explanations = {
            "fake_news": self._explain_fake_news(fake_news_result),
            "bias": self._explain_bias(bias_result),
            "emotion": self._explain_emotion(emotion_result),
            "overall": self._explain_overall_assessment(fake_news_result, bias_result, emotion_result)
        }
        
        return explanations
    
    def _explain_fake_news(self, fake_news_result: Dict[str, Any]) -> List[str]:
        """Explain fake news detection results"""
        
        explanations = []
        
        prediction = fake_news_result.get("prediction", "unknown")
        confidence = fake_news_result.get("confidence", 0)
        
        if prediction == "fake":
            explanations.append(f"The model predicts this content is {confidence:.1%} likely to be fake news.")
            
            if fake_news_result.get("clickbait_score", 0) > 0.5:
                explanations.append("The content shows characteristics of clickbait, which is often associated with fake news.")
            
            if fake_news_result.get("sensationalism_score", 0) > 0.5:
                explanations.append("The content uses sensational language that exaggerates or misrepresents information.")
        
        elif prediction == "real":
            explanations.append(f"The model predicts this content is {confidence:.1%} likely to be real news.")
            
            if fake_news_result.get("authority_score", 0) > 0.5:
                explanations.append("The content references authoritative sources, which increases credibility.")
        
        return explanations
    
    def _explain_bias(self, bias_result: Dict[str, Any]) -> List[str]:
        """Explain bias detection results"""
        
        explanations = []
        
        bias_score = bias_result.get("overall_bias_score", 0)
        political_bias = bias_result.get("political_bias", {})
        
        if bias_score > 0.5:
            explanations.append(f"The content shows a high level of bias ({bias_score:.1%}).")
            
            leaning = political_bias.get("leaning", "unknown")
            if leaning != "neutral":
                explanations.append(f"The content appears to lean {leaning} politically.")
            
            loaded_score = bias_result.get("loaded_language", {}).get("loaded_score", 0)
            if loaded_score > 0.3:
                explanations.append("The content uses loaded language that may influence reader perception.")
        
        return explanations
    
    def _explain_emotion(self, emotion_result: Dict[str, Any]) -> List[str]:
        """Explain emotion analysis results"""
        
        explanations = []
        
        manipulation_score = emotion_result.get("overall_manipulation_score", 0)
        dominant_emotion = emotion_result.get("emotions", {}).get("dominant_emotion", "neutral")
        
        if manipulation_score > 0.5:
            explanations.append(f"The content shows signs of emotional manipulation ({manipulation_score:.1%}).")
            
            if dominant_emotion in ["fear", "anger"]:
                explanations.append(f"The content primarily uses {dominant_emotion}-inducing language to influence readers.")
        
        return explanations
    
    def _explain_overall_assessment(self, 
                                  fake_news_result: Dict[str, Any],
                                  bias_result: Dict[str, Any],
                                  emotion_result: Dict[str, Any]) -> List[str]:
        """Generate overall assessment explanation"""
        
        explanations = []
        
        # Combine all factors for overall assessment
        fake_prob = fake_news_result.get("fake_probability", 0.5)
        bias_score = bias_result.get("overall_bias_score", 0.5)
        emotion_score = emotion_result.get("overall_manipulation_score", 0.5)
        
        if fake_prob > 0.7 or bias_score > 0.7 or emotion_score > 0.7:
            explanations.append("Multiple red flags indicate this content may be unreliable.")
            explanations.append("Exercise extreme caution and verify with trusted sources.")
        elif fake_prob > 0.5 or bias_score > 0.5 or emotion_score > 0.5:
            explanations.append("Some concerns were identified about this content's reliability.")
            explanations.append("Consider seeking additional sources before accepting this information.")
        else:
            explanations.append("This content appears relatively reliable based on our analysis.")
            explanations.append("Still, it's good practice to verify important information.")
        
        return explanations
    
    def _analyze_word_importance(self, 
                               text: str,
                               fake_news_result: Dict[str, Any],
                               bias_result: Dict[str, Any],
                               emotion_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze word importance for explanation"""
        
        words = text.lower().split()
        word_freq = Counter(words)
        
        # Get important words from each analysis
        important_words = []
        
        # From fake news detection
        if fake_news_result.get("clickbait_score", 0) > 0.3:
            clickbait_words = ["shocking", "unbelievable", "miracle", "breakthrough", "secret"]
            for word in clickbait_words:
                if word in word_freq:
                    important_words.append({
                        "word": word,
                        "importance": word_freq[word] * 2,
                        "reason": "Clickbait indicator",
                        "impact": "negative"
                    })
        
        # From bias detection
        if bias_result.get("overall_bias_score", 0) > 0.3:
            bias_words = ["liberal", "conservative", "biased", "propaganda", "agenda"]
            for word in bias_words:
                if word in word_freq:
                    important_words.append({
                        "word": word,
                        "importance": word_freq[word] * 1.5,
                        "reason": "Bias indicator",
                        "impact": "negative"
                    })
        
        # From emotion analysis
        if emotion_result.get("overall_manipulation_score", 0) > 0.3:
            emotion_words = ["shocking", "terrifying", "outrageous", "amazing", "incredible"]
            for word in emotion_words:
                if word in word_freq:
                    important_words.append({
                        "word": word,
                        "importance": word_freq[word] * 1.8,
                        "reason": "Emotional manipulation",
                        "impact": "negative"
                    })
        
        # Sort by importance and return top 10
        important_words.sort(key=lambda x: x["importance"], reverse=True)
        return important_words[:10]
    
    def _generate_source_comparison(self, fake_news_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison with trusted sources (placeholder)"""
        
        # This would normally compare with actual trusted sources
        # For now, return a placeholder structure
        
        return {
            "trusted_sources_checked": 0,
            "matching_claims": 0,
            "contradictory_claims": 0,
            "unverified_claims": 0,
            "note": "Source comparison feature requires integration with fact-checking databases"
        }
    
    def _generate_explanation_summary(self, sentence_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of explanations"""
        
        total_sentences = len(sentence_analysis)
        suspicious_sentences = sum(1 for s in sentence_analysis if s["is_suspicious"])
        
        # Count pattern types
        pattern_counts = {}
        for analysis in sentence_analysis:
            for pattern in analysis["detected_patterns"]:
                pattern_type = pattern["type"]
                pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        return {
            "total_sentences": total_sentences,
            "suspicious_sentences": suspicious_sentences,
            "suspicious_percentage": round((suspicious_sentences / max(total_sentences, 1)) * 100, 1),
            "pattern_distribution": pattern_counts,
            "most_common_pattern": max(pattern_counts.items(), key=lambda x: x[1])[0] if pattern_counts else None
        }
    
    def _fallback_explanation(self, text: str) -> Dict[str, Any]:
        """Fallback explanation when main analysis fails"""
        
        return {
            "highlighted_text": text,
            "sentence_analysis": [],
            "overall_explanations": {
                "fake_news": ["Unable to generate detailed explanation due to analysis failure."],
                "bias": ["Unable to generate detailed explanation due to analysis failure."],
                "emotion": ["Unable to generate detailed explanation due to analysis failure."],
                "overall": ["Manual verification recommended due to analysis failure."]
            },
            "word_importance": [],
            "source_comparison": {
                "note": "Source comparison unavailable due to analysis failure"
            },
            "explanation_summary": {
                "total_sentences": 0,
                "suspicious_sentences": 0,
                "suspicious_percentage": 0,
                "pattern_distribution": {},
                "most_common_pattern": None,
                "error": "Main explanation analysis failed"
            }
        }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        
        return {
            "type": "rule_based_explainable_ai",
            "initialized": self._initialized,
            "features": [
                "sentence_highlighting",
                "pattern_detection",
                "word_importance",
                "explanation_generation"
            ],
            "pattern_types": list(self.suspicious_patterns.keys())
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the explainable AI"""
        
        if not self._initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test with sample text
            test_text = "This is a test sentence for health check."
            test_fake_news = {"prediction": "real", "confidence": 0.8}
            test_bias = {"overall_bias_score": 0.2}
            test_emotion = {"overall_manipulation_score": 0.1}
            
            result = await self.explain(test_text, test_fake_news, test_bias, test_emotion)
            
            return {
                "status": "healthy",
                "test_result": result
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
