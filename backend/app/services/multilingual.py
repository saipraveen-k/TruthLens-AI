import logging
from typing import Dict, Any, Optional
import asyncio
from app.config import settings

logger = logging.getLogger(__name__)


class MultilingualProcessor:
    """Handles multilingual text processing and translation"""
    
    def __init__(self):
        self._initialized = False
        self.supported_languages = settings.supported_languages
        
        # Translation service configuration
        self.translation_service = None
        self.google_translate_api_key = settings.google_translate_api_key
        
        # Language detection patterns
        self.language_patterns = {
            "hi": r'[\u0900-\u097F]',  # Hindi Unicode range
            "es": r'[ñáéíóúü]',        # Spanish characters
            "fr": r'[àâäçéèêëïîôùûüÿ]',  # French characters
            "de": r'[äöüß]',            # German characters
        }
    
    async def initialize(self):
        """Initialize the multilingual processor"""
        if self._initialized:
            return
        
        logger.info("Initializing Multilingual Processor...")
        
        try:
            # Initialize translation service if API key is available
            if self.google_translate_api_key and self.google_translate_api_key != "your-google-translate-api-key-here":
                from googletrans import Translator
                self.translation_service = Translator()
                logger.info("Google Translate service initialized")
            else:
                logger.warning("Google Translate API key not configured, using basic language detection")
            
            self._initialized = True
            logger.info("Multilingual Processor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Multilingual Processor: {e}")
            # Continue with basic functionality
            self._initialized = True
            logger.warning("Multilingual Processor initialized in basic mode")
    
    async def process(self, 
                     text: str, 
                     source_language: str,
                     analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process multilingual content"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # If source is English, no translation needed
            if source_language == "en":
                return {
                    "original_language": "en",
                    "processed_language": "en",
                    "translation_performed": False,
                    "language_confidence": 0.9,
                    "translated_results": None
                }
            
            # Translate to English for analysis
            if self.translation_service:
                translated_text = await self._translate_text(text, source_language, "en")
                
                # Re-analyze translated text (simplified version)
                translated_analysis = await self._quick_analyze(translated_text)
                
                # Translate explanations back to original language
                translated_explanations = await self._translate_explanations(
                    analysis_results.get("explanation", {}), 
                    "en", 
                    source_language
                )
                
                return {
                    "original_language": source_language,
                    "processed_language": "en",
                    "translation_performed": True,
                    "translated_text": translated_text,
                    "translated_analysis": translated_analysis,
                    "translated_explanations": translated_explanations,
                    "language_confidence": 0.8
                }
            else:
                # Fallback: return original with note
                return {
                    "original_language": source_language,
                    "processed_language": source_language,
                    "translation_performed": False,
                    "note": "Translation service unavailable, analysis performed on original text",
                    "language_confidence": 0.6
                }
        
        except Exception as e:
            logger.error(f"Error in multilingual processing: {e}")
            return self._fallback_multilingual_result(source_language)
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of the input text"""
        
        if not self._initialized:
            await self.initialize()
        
        try:
            # Try using translation service for detection
            if self.translation_service:
                detected = self.translation_service.detect(text)
                return {
                    "detected_language": detected.lang,
                    "confidence": getattr(detected, 'confidence', 0.8),
                    "method": "google_translate"
                }
            else:
                # Fallback to pattern-based detection
                return self._detect_language_by_patterns(text)
        
        except Exception as e:
            logger.error(f"Error in language detection: {e}")
            return {
                "detected_language": "en",
                "confidence": 0.5,
                "method": "fallback",
                "error": str(e)
            }
    
    async def _translate_text(self, text: str, from_lang: str, to_lang: str) -> str:
        """Translate text from one language to another"""
        
        try:
            if not self.translation_service:
                raise Exception("Translation service not available")
            
            # Google Translate uses different language codes
            lang_mapping = {
                "hi": "hi",
                "es": "es", 
                "fr": "fr",
                "de": "de",
                "en": "en"
            }
            
            from_code = lang_mapping.get(from_lang, from_lang)
            to_code = lang_mapping.get(to_lang, to_lang)
            
            # Perform translation
            result = self.translation_service.translate(text, src=from_code, dest=to_code)
            return result.text
        
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text  # Return original text if translation fails
    
    async def _quick_analyze(self, text: str) -> Dict[str, Any]:
        """Quick analysis of translated text (simplified)"""
        
        # This would normally call the full NLP pipeline
        # For now, return a placeholder analysis
        return {
            "credibility_score": 50.0,
            "fake_probability": 50.0,
            "note": "Quick analysis of translated text"
        }
    
    async def _translate_explanations(self, explanations: Dict[str, Any], from_lang: str, to_lang: str) -> Dict[str, Any]:
        """Translate explanations back to original language"""
        
        if not self.translation_service:
            return explanations
        
        try:
            translated_explanations = {}
            
            for key, value in explanations.items():
                if isinstance(value, str):
                    translated_explanations[key] = await self._translate_text(value, from_lang, to_lang)
                elif isinstance(value, list):
                    translated_explanations[key] = [
                        await self._translate_text(item, from_lang, to_lang) if isinstance(item, str) else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    translated_explanations[key] = await self._translate_explanations(value, from_lang, to_lang)
                else:
                    translated_explanations[key] = value
            
            return translated_explanations
        
        except Exception as e:
            logger.error(f"Failed to translate explanations: {e}")
            return explanations
    
    def _detect_language_by_patterns(self, text: str) -> Dict[str, Any]:
        """Detect language using character patterns"""
        
        import re
        
        scores = {}
        
        for lang, pattern in self.language_patterns.items():
            matches = len(re.findall(pattern, text))
            scores[lang] = matches / len(text) if text else 0
        
        # Find the language with highest score
        if scores:
            best_lang = max(scores, key=scores.get)
            confidence = scores[best_lang]
            
            # Only return non-English if confidence is significant
            if confidence > 0.05:  # 5% threshold
                return {
                    "detected_language": best_lang,
                    "confidence": min(confidence * 10, 0.9),  # Scale confidence
                    "method": "pattern_based",
                    "scores": scores
                }
        
        # Default to English
        return {
            "detected_language": "en",
            "confidence": 0.7,
            "method": "default",
            "scores": scores
        }
    
    def _fallback_multilingual_result(self, source_language: str) -> Dict[str, Any]:
        """Fallback result when multilingual processing fails"""
        
        return {
            "original_language": source_language,
            "processed_language": source_language,
            "translation_performed": False,
            "error": "Multilingual processing failed, using original text",
            "language_confidence": 0.3
        }
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages with their names"""
        
        language_names = {
            "en": "English",
            "hi": "हिन्दी (Hindi)",
            "es": "Español (Spanish)",
            "fr": "Français (French)",
            "de": "Deutsch (German)"
        }
        
        return {
            code: language_names.get(code, code.upper())
            for code in self.supported_languages
        }
    
    async def translate_to_english(self, text: str, source_language: str) -> str:
        """Convenience method to translate text to English"""
        
        if source_language == "en":
            return text
        
        return await self._translate_text(text, source_language, "en")
    
    async def translate_from_english(self, text: str, target_language: str) -> str:
        """Convenience method to translate text from English"""
        
        if target_language == "en":
            return text
        
        return await self._translate_text(text, "en", target_language)
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        
        return {
            "type": "multilingual_processor",
            "initialized": self._initialized,
            "supported_languages": self.supported_languages,
            "translation_service": "google_translate" if self.translation_service else "none",
            "features": [
                "language_detection",
                "text_translation",
                "explanation_translation"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the multilingual processor"""
        
        if not self._initialized:
            return {"status": "not_initialized"}
        
        try:
            # Test language detection
            test_text = "This is a test sentence."
            detection_result = await self.detect_language(test_text)
            
            # Test translation if available
            translation_result = None
            if self.translation_service:
                translation_result = await self._translate_text("Hello", "en", "es")
            
            return {
                "status": "healthy",
                "language_detection": detection_result,
                "translation_test": translation_result,
                "supported_languages": self.supported_languages
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
