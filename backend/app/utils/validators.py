import re
from typing import Optional
from urllib.parse import urlparse


def validate_text_input(text: str) -> str:
    """Validate and clean text input"""
    if not text or not text.strip():
        raise ValueError("Text input cannot be empty")
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Check minimum length
    if len(text) < 10:
        raise ValueError("Text input is too short (minimum 10 characters)")
    
    # Check maximum length
    if len(text) > 50000:
        raise ValueError("Text input is too long (maximum 50000 characters)")
    
    return text


def validate_url(url: str) -> str:
    """Validate URL format"""
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")
    
    url = url.strip()
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Basic URL validation
    parsed = urlparse(url)
    if not parsed.netloc or not parsed.scheme:
        raise ValueError("Invalid URL format")
    
    # Check for valid domain
    domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9])*$'
    if not re.match(domain_pattern, parsed.netloc.split(':')[0]):
        raise ValueError("Invalid domain name")
    
    return url


def validate_email(email: str) -> str:
    """Validate email format"""
    if not email or not email.strip():
        raise ValueError("Email cannot be empty")
    
    email = email.strip().lower()
    
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    
    return email


def validate_password(password: str) -> str:
    """Validate password strength"""
    if not password:
        raise ValueError("Password cannot be empty")
    
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if len(password) > 128:
        raise ValueError("Password is too long (maximum 128 characters)")
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain at least one uppercase letter")
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain at least one lowercase letter")
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        raise ValueError("Password must contain at least one digit")
    
    return password


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    if not filename:
        return "unnamed_file"
    
    # Remove path separators and special characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext if ext else name[:255]
    
    return filename.strip()


def detect_language(text: str) -> str:
    """Simple language detection (basic implementation)"""
    if not text:
        return "en"
    
    # Count characters that suggest different languages
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
    spanish_chars = len(re.findall(r'[ñáéíóúü]', text.lower()))
    french_chars = len(re.findall(r'[àâäçéèêëïîôùûüÿ]', text.lower()))
    german_chars = len(re.findall(r'[äöüß]', text.lower()))
    
    total_chars = len(text)
    
    # Simple heuristic based on character frequency
    if hindi_chars / total_chars > 0.1:
        return "hi"
    elif spanish_chars / total_chars > 0.05:
        return "es"
    elif french_chars / total_chars > 0.05:
        return "fr"
    elif german_chars / total_chars > 0.05:
        return "de"
    else:
        return "en"


def is_suspicious_domain(domain: str) -> bool:
    """Check if domain matches known suspicious patterns"""
    suspicious_patterns = [
        r'.*fake.*',
        r'.*satire.*',
        r'.*conspiracy.*',
        r'.*hoax.*',
        r'.*clickbait.*',
        r'.*sensational.*',
        r'.*gossip.*',
        r'.*rumor.*'
    ]
    
    domain_lower = domain.lower()
    
    for pattern in suspicious_patterns:
        if re.match(pattern, domain_lower):
            return True
    
    return False


def extract_domain_from_url(url: str) -> str:
    """Extract domain name from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return ""


def calculate_text_complexity(text: str) -> dict:
    """Calculate text complexity metrics"""
    if not text:
        return {"complexity_score": 0, "level": "Unknown"}
    
    words = text.split()
    sentences = text.split('.')
    
    # Average words per sentence
    avg_words_per_sentence = len(words) / max(len(sentences), 1)
    
    # Average word length
    avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
    
    # Complex words (words with more than 6 characters)
    complex_words = [word for word in words if len(word) > 6]
    complex_word_ratio = len(complex_words) / max(len(words), 1)
    
    # Calculate complexity score (0-100)
    complexity_score = min(100, (
        avg_words_per_sentence * 5 +
        avg_word_length * 10 +
        complex_word_ratio * 50
    ))
    
    # Determine complexity level
    if complexity_score < 30:
        level = "Simple"
    elif complexity_score < 60:
        level = "Moderate"
    else:
        level = "Complex"
    
    return {
        "complexity_score": round(complexity_score, 2),
        "level": level,
        "avg_words_per_sentence": round(avg_words_per_sentence, 2),
        "avg_word_length": round(avg_word_length, 2),
        "complex_word_ratio": round(complex_word_ratio, 2)
    }
