import asyncio
from typing import Dict, Any, Optional
import time
import logging

from app.services.fake_news_detector import FakeNewsDetector
from app.services.bias_detector import BiasDetector
from app.services.emotion_analyzer import EmotionAnalyzer
from app.services.credibility_scorer import CredibilityScorer
from app.services.explainable_ai import ExplainableAI
from app.services.multilingual import MultilingualProcessor
from app.utils.preprocessor import TextPreprocessor
from app.utils.validators import detect_language
from app.config import settings

logger = logging.getLogger(__name__)


class NLPipeline:
    """Main NLP pipeline orchestrating all analysis components"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.fake_news_detector = FakeNewsDetector()
        self.bias_detector = BiasDetector()
        self.emotion_analyzer = EmotionAnalyzer()
        self.credibility_scorer = CredibilityScorer()
        self.explainable_ai = ExplainableAI()
        self.multilingual_processor = MultilingualProcessor()
        
        self._initialized = False
    
    async def initialize(self):
        """Initialize all ML models and components"""
        if self._initialized:
            return
        
        logger.info("Initializing NLP pipeline...")
        
        try:
            # Initialize all components
            await self.fake_news_detector.initialize()
            await self.bias_detector.initialize()
            await self.emotion_analyzer.initialize()
            await self.credibility_scorer.initialize()
            await self.explainable_ai.initialize()
            await self.multilingual_processor.initialize()
            
            self._initialized = True
            logger.info("NLP pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP pipeline: {e}")
            raise
    
    async def analyze_text(self, text: str, language: str = None) -> Dict[str, Any]:
        """Complete text analysis pipeline"""
        
        if not self._initialized:
            await self.initialize()
        
        start_time = time.time()
        
        # Detect language if not provided
        if not language:
            language = detect_language(text)
        
        # Preprocess text
        cleaned_text = self.preprocessor.preprocess(text)
        sentences = self.preprocessor.sentence_tokenize(text)
        
        # Initialize results dictionary
        results = {
            "metadata": {
                "language": language,
                "word_count": len(text.split()),
                "sentence_count": len(sentences),
                "processing_time": 0
            }
        }
        
        try:
            # Step 1: Fake News Detection
            logger.info("Performing fake news detection...")
            fake_news_result = await self.fake_news_detector.analyze(cleaned_text)
            results["fake_news"] = fake_news_result
            
            # Step 2: Bias Detection
            logger.info("Performing bias detection...")
            bias_result = await self.bias_detector.analyze(text)
            results["bias"] = bias_result
            
            # Step 3: Emotion Analysis
            logger.info("Performing emotion analysis...")
            emotion_result = await self.emotion_analyzer.analyze(text)
            results["emotion"] = emotion_result
            
            # Step 4: Source Reliability (if URL provided)
            source_reliability = "unknown"
            source_reliability_score = 50.0
            
            # Step 5: Credibility Scoring
            logger.info("Calculating credibility score...")
            credibility_result = await self.credibility_scorer.calculate_score(
                fake_news_result=fake_news_result,
                bias_result=bias_result,
                emotion_result=emotion_result,
                source_reliability=source_reliability_score
            )
            
            results.update(credibility_result)
            
            # Step 6: Explainable AI
            logger.info("Generating explanations...")
            explanation = await self.explainable_ai.explain(
                text=text,
                fake_news_result=fake_news_result,
                bias_result=bias_result,
                emotion_result=emotion_result
            )
            results["explanation"] = explanation
            
            # Step 7: Multilingual processing (if needed)
            if language != "en" and settings.enable_multilingual:
                logger.info(f"Processing multilingual content ({language})...")
                multilingual_result = await self.multilingual_processor.process(
                    text=text,
                    source_language=language,
                    analysis_results=results
                )
                results["multilingual"] = multilingual_result
            
            # Calculate processing time
            processing_time = time.time() - start_time
            results["metadata"]["processing_time"] = round(processing_time, 2)
            
            logger.info(f"Analysis completed in {processing_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
        
        return results
    
    async def analyze_batch(self, texts: list, language: str = None) -> list:
        """Analyze multiple texts in batch"""
        
        if not self._initialized:
            await self.initialize()
        
        results = []
        
        # Process texts concurrently
        tasks = [
            self.analyze_text(text, language) 
            for text in texts
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing text {i}: {result}")
                processed_results.append({
                    "error": str(result),
                    "metadata": {"text_index": i}
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        
        if not self._initialized:
            await self.initialize()
        
        return {
            "fake_news_detector": await self.fake_news_detector.get_model_info(),
            "bias_detector": await self.bias_detector.get_model_info(),
            "emotion_analyzer": await self.emotion_analyzer.get_model_info(),
            "credibility_scorer": await self.credibility_scorer.get_model_info(),
            "explainable_ai": await self.explainable_ai.get_model_info(),
            "multilingual_processor": await self.multilingual_processor.get_model_info()
        }
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return settings.supported_languages
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for all components"""
        
        health_status = {
            "pipeline_initialized": self._initialized,
            "components": {}
        }
        
        if self._initialized:
            try:
                # Test each component
                health_status["components"]["fake_news_detector"] = await self.fake_news_detector.health_check()
                health_status["components"]["bias_detector"] = await self.bias_detector.health_check()
                health_status["components"]["emotion_analyzer"] = await self.emotion_analyzer.health_check()
                health_status["components"]["credibility_scorer"] = await self.credibility_scorer.health_check()
                health_status["components"]["explainable_ai"] = await self.explainable_ai.health_check()
                health_status["components"]["multilingual_processor"] = await self.multilingual_processor.health_check()
                
                health_status["overall_status"] = "healthy"
                
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                health_status["overall_status"] = "unhealthy"
                health_status["error"] = str(e)
        
        else:
            health_status["overall_status"] = "not_initialized"
        
        return health_status
