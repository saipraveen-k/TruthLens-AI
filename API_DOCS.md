# TruthLens AI - API Documentation

Complete API reference for the TruthLens AI News Credibility Analyzer.

## 📋 Table of Contents

1. [Base URLs](#base-urls)
2. [Authentication](#authentication)
3. [Analysis Endpoints](#analysis-endpoints)
4. [Sources Endpoints](#sources-endpoints)
5. [User Management](#user-management)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Webhooks](#webhooks)

## 🌐 Base URLs

### Development
```
http://localhost:8000
```

### Production
```
https://api.truthlens.ai
```

### API Versioning
All endpoints are versioned using URL paths:
```
/api/v1/analyze/text
```

## 🔐 Authentication

TruthLens AI uses JWT (JSON Web Tokens) for authentication.

### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "user_id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "user_id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Using the Token
Include the token in the Authorization header:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🔍 Analysis Endpoints

### Analyze Text
```http
POST /analyze/text
```

**Request Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Breaking: Scientists discover that eating chocolate cures all diseases! Researchers at the University of Miracle Studies have found that consuming just one chocolate bar per day can prevent cancer, reverse aging, and make you smarter.",
  "language": "en",
  "title": "Chocolate Cures All Diseases"
}
```

**Response:**
```json
{
  "article_id": "550e8400-e29b-41d4-a716-446655440000",
  "credibility_score": 15.2,
  "fake_probability": 84.8,
  "bias_score": "high",
  "emotional_manipulation": "high",
  "source_reliability": "unknown",
  "analysis": {
    "fake_news": {
      "prediction": "fake",
      "confidence": 0.848,
      "model_used": "bert-base-uncased",
      "fallback_used": false
    },
    "bias": {
      "political_leaning": "right",
      "subjectivity": 0.85,
      "loaded_language": 0.72,
      "clickbait_score": 0.91,
      "overall_bias_score": 0.83
    },
    "emotion": {
      "dominant_emotion": "excitement",
      "emotions": {
        "anger": 0.1,
        "fear": 0.2,
        "joy": 0.6,
        "sadness": 0.05,
        "surprise": 0.05
      },
      "manipulation_indicators": [
        "emotional_language",
        "exaggerated_claims",
        "appeal_to_emotion"
      ],
      "overall_manipulation_score": 0.78
    },
    "credibility": {
      "source_reliability": 0.3,
      "factual_accuracy": 0.2,
      "bias_impact": 0.4,
      "emotional_manipulation": 0.7,
      "overall_score": 0.152
    }
  },
  "explanation": {
    "highlighted_text": "Breaking: <span class='suspicious-high'>Scientists discover that eating chocolate cures all diseases!</span> Researchers at the <span class='suspicious-medium'>University of Miracle Studies</span> have found that consuming just one chocolate bar per day can <span class='suspicious-high'>prevent cancer, reverse aging, and make you smarter</span>.",
    "key_factors": [
      {
        "type": "unsubstantiated_claims",
        "text": "cures all diseases",
        "reason": "Extraordinary claim without scientific evidence",
        "impact": -0.8,
        "confidence": 0.95
      },
      {
        "type": "emotional_manipulation",
        "text": "make you smarter",
        "reason": "Appeals to personal improvement without evidence",
        "impact": -0.6,
        "confidence": 0.88
      }
    ],
    "pattern_analysis": [
      {
        "pattern": "clickbait_headline",
        "matches": ["Breaking:", "cures all diseases"],
        "severity": "high"
      },
      {
        "pattern": "unsubstantiated_medical_claims",
        "matches": ["prevent cancer", "reverse aging"],
        "severity": "high"
      }
    ],
    "explanation_summary": {
      "total_sentences": 3,
      "suspicious_sentences": 3,
      "suspicious_percentage": 100,
      "most_common_pattern": "unsubstantiated_claims"
    }
  },
  "metadata": {
    "language": "en",
    "word_count": 45,
    "processing_time": 1.23,
    "models_used": ["bert-base-uncased", "distilroberta-base"],
    "cache_hit": false
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Analyze URL
```http
POST /analyze/url
```

**Request Body:**
```json
{
  "url": "https://example.com/news-article",
  "extract_full_text": true,
  "language": "auto"
}
```

**Response:**
Same format as text analysis, plus:
```json
{
  "source_info": {
    "domain": "example.com",
    "reliability_score": 72.3,
    "bias_rating": "center-right",
    "factual_reporting": "medium",
    "country": "US",
    "category": "news",
    "notes": "Mixed reliability record"
  },
  "extracted_content": {
    "title": "Article Title",
    "author": "John Smith",
    "publish_date": "2024-01-15T08:00:00Z",
    "content": "Full article text...",
    "images": ["image1.jpg", "image2.jpg"]
  }
}
```

### Analyze PDF
```http
POST /analyze/pdf
```

**Request Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
```
file: [PDF file, max 10MB]
```

**Response:**
Same format as text analysis, plus:
```json
{
  "pdf_metadata": {
    "title": "Document Title",
    "author": "Document Author",
    "pages": 15,
    "creation_date": "2024-01-10T12:00:00Z",
    "extraction_method": "pdfplumber"
  }
}
```

### Get Analysis History
```http
GET /analyze/history
```

**Query Parameters:**
- `page` (int, default: 1): Page number
- `limit` (int, default: 20): Items per page (max 100)
- `sort` (string, default: "created_at"): Sort field
- `order` (string, default: "desc"): Sort order ("asc" or "desc")

**Response:**
```json
{
  "articles": [
    {
      "article_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Article Title",
      "credibility_score": 85.2,
      "fake_probability": 14.8,
      "created_at": "2024-01-15T10:30:00Z",
      "url": "https://example.com/article"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

### Get Specific Analysis
```http
GET /analyze/article/{article_id}
```

**Response:**
Complete analysis object as shown in text analysis response.

## 📊 Sources Endpoints

### Get All Sources
```http
GET /sources
```

**Query Parameters:**
- `page` (int, default: 1): Page number
- `limit` (int, default: 50): Items per page
- `search` (string): Search term
- `category` (string): Filter by category
- `min_reliability` (float): Minimum reliability score
- `max_reliability` (float): Maximum reliability score

**Response:**
```json
{
  "sources": [
    {
      "source_id": 1,
      "domain_name": "reuters.com",
      "reliability_score": 98.5,
      "bias_rating": "center",
      "factual_reporting": "high",
      "country": "US",
      "category": "news",
      "is_active": true,
      "analysis_count": 15420,
      "fake_news_count": 234,
      "last_checked": "2024-01-15T09:00:00Z",
      "notes": "Highly reliable international news organization"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 1250,
    "pages": 25
  }
}
```

### Get Source by Domain
```http
GET /sources/{domain}
```

**Response:**
Single source object as shown above.

### Get Top Reliable Sources
```http
GET /sources/top/reliable
```

**Query Parameters:**
- `limit` (int, default: 20): Number of sources

**Response:**
```json
{
  "sources": [
    {
      "domain_name": "reuters.com",
      "reliability_score": 98.5,
      "analysis_count": 15420
    }
  ]
}
```

### Get Top Unreliable Sources
```http
GET /sources/top/unreliable
```

**Response:**
Same format as reliable sources, sorted by lowest reliability.

### Get Source Statistics
```http
GET /sources/stats/overview
```

**Response:**
```json
{
  "total_sources": 1250,
  "active_sources": 1180,
  "average_reliability": 67.3,
  "bias_distribution": {
    "far-left": 8,
    "left": 45,
    "center-left": 120,
    "center": 380,
    "center-right": 150,
    "right": 89,
    "far-right": 23
  },
  "category_distribution": {
    "news": 650,
    "opinion": 180,
    "satire": 25,
    "conspiracy": 45,
    "blog": 350
  },
  "country_distribution": {
    "US": 520,
    "UK": 180,
    "Canada": 85,
    "Australia": 65,
    "Other": 400
  }
}
```

## 👤 User Management

### Get User Profile
```http
GET /auth/me
```

**Response:**
```json
{
  "user_id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z",
  "analysis_count": 45,
  "subscription": {
    "plan": "free",
    "analyses_remaining": 55,
    "reset_date": "2024-02-01T00:00:00Z"
  }
}
```

### Update Profile
```http
PUT /auth/profile
```

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "john.updated@example.com"
}
```

### Change Password
```http
POST /auth/change-password
```

**Request Body:**
```json
{
  "current_password": "oldPassword123",
  "new_password": "newPassword456"
}
```

### Logout
```http
POST /auth/logout
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

## ❌ Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "text",
      "issue": "Text must be between 50 and 10000 characters"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

### Validation Errors
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "text": ["Text must be at least 50 characters"],
      "url": ["Invalid URL format"]
    }
  }
}
```

## 🚦 Rate Limiting

### Rate Limits by Plan
| Plan | Requests/Hour | Requests/Day |
|------|---------------|--------------|
| Free | 100 | 1,000 |
| Basic | 500 | 5,000 |
| Pro | 2,000 | 20,000 |
| Enterprise | Unlimited | Unlimited |

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248600
```

### Rate Limit Exceeded Response
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "retry_after": 3600,
    "limit": 100,
    "reset_time": "2024-01-15T11:30:00Z"
  }
}
```

## 🪝 Webhooks

### Configure Webhook
```http
POST /webhooks/configure
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook/truthlens",
  "events": ["analysis_completed", "user_registered"],
  "secret": "your-webhook-secret"
}
```

### Webhook Events

#### Analysis Completed
```json
{
  "event": "analysis_completed",
  "data": {
    "article_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 123,
    "credibility_score": 85.2,
    "fake_probability": 14.8,
    "completed_at": "2024-01-15T10:30:00Z"
  }
}
```

#### User Registered
```json
{
  "event": "user_registered",
  "data": {
    "user_id": 124,
    "email": "newuser@example.com",
    "registered_at": "2024-01-15T10:35:00Z"
  }
}
```

### Webhook Security
- Webhooks include `X-TruthLens-Signature` header
- Verify signature using HMAC-SHA256 with your secret
- Example verification code:
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(), 
        payload.encode(), 
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## 📝 SDKs and Libraries

### Python SDK
```python
from truthlens import TruthLensClient

client = TruthLensClient(api_key="your-api-key")

# Analyze text
result = client.analyze_text("Your news text here...")
print(f"Credibility: {result.credibility_score}%")

# Analyze URL
result = client.analyze_url("https://example.com/news")
```

### JavaScript SDK
```javascript
import { TruthLensClient } from 'truthlens-js';

const client = new TruthLensClient({ apiKey: 'your-api-key' });

// Analyze text
const result = await client.analyzeText('Your news text here...');
console.log(`Credibility: ${result.credibilityScore}%`);
```

### cURL Examples
```bash
# Analyze text
curl -X POST "https://api.truthlens.ai/analyze/text" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your news text here..."}'

# Get sources
curl -X GET "https://api.truthlens.ai/sources" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔄 API Changelog

### v1.2.0 (2024-01-15)
- Added PDF analysis endpoint
- Improved error messages
- Added webhook support

### v1.1.0 (2024-01-01)
- Added multilingual support
- Enhanced bias detection
- Improved caching

### v1.0.0 (2023-12-01)
- Initial API release
- Text and URL analysis
- Source management

## 📞 Support

- **API Documentation**: https://docs.truthlens.ai
- **Status Page**: https://status.truthlens.ai
- **Support Email**: api-support@truthlens.ai
- **GitHub Issues**: https://github.com/truthlens-ai/truthlens-ai/issues

---

For more information, visit our [main documentation](https://truthlens.ai/docs).
