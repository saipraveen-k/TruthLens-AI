-- TruthLens AI Database Schema
-- PostgreSQL database initialization script

-- Drop existing tables if they exist (for development)
DROP TABLE IF EXISTS analysis_cache CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS sources CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create Sources table
CREATE TABLE sources (
    source_id SERIAL PRIMARY KEY,
    domain_name VARCHAR(255) UNIQUE NOT NULL,
    reliability_score FLOAT,
    bias_rating VARCHAR(50),
    factual_reporting VARCHAR(50),
    country VARCHAR(10),
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    last_checked TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    analysis_count INTEGER DEFAULT 0,
    fake_news_count INTEGER DEFAULT 0
);

-- Create Articles table
CREATE TABLE articles (
    article_id VARCHAR(36) PRIMARY KEY,  -- UUID
    user_id INTEGER REFERENCES users(user_id),
    title VARCHAR(500),
    content TEXT NOT NULL,
    url VARCHAR(1000),
    credibility_score FLOAT,
    fake_probability FLOAT,
    bias_score VARCHAR(50),
    emotional_manipulation VARCHAR(50),
    source_reliability VARCHAR(50),
    analysis JSONB,
    explanation JSONB,
    language VARCHAR(10) DEFAULT 'en',
    word_count INTEGER,
    processing_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create Analysis Cache table
CREATE TABLE analysis_cache (
    cache_id SERIAL PRIMARY KEY,
    content_hash VARCHAR(64) UNIQUE,
    analysis_result JSONB,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_sources_domain ON sources(domain_name);
CREATE INDEX idx_sources_active ON sources(is_active);
CREATE INDEX idx_sources_reliability ON sources(reliability_score);
CREATE INDEX idx_articles_user_id ON articles(user_id);
CREATE INDEX idx_articles_created_at ON articles(created_at DESC);
CREATE INDEX idx_articles_credibility ON articles(credibility_score);
CREATE INDEX idx_cache_content_hash ON analysis_cache(content_hash);
CREATE INDEX idx_cache_expires_at ON analysis_cache(expires_at);

-- Create full-text search indexes
CREATE INDEX idx_articles_content_fts ON articles USING gin(to_tsvector('english', content));
CREATE INDEX idx_articles_title_fts ON articles USING gin(to_tsvector('english', title));

-- Insert default reliable sources
INSERT INTO sources (domain_name, reliability_score, bias_rating, factual_reporting, country, category, notes) VALUES
('reuters.com', 98.5, 'center', 'high', 'US', 'news', 'Highly reliable international news organization'),
('bbc.com', 96.8, 'center-left', 'high', 'UK', 'news', 'Public service broadcaster with strong editorial standards'),
('ap.org', 95.2, 'center', 'high', 'US', 'news', 'Associated Press - nonprofit news agency'),
('npr.org', 94.1, 'center-left', 'high', 'US', 'news', 'National Public Radio - nonprofit media'),
('wsj.com', 92.3, 'center-right', 'high', 'US', 'news', 'Wall Street Journal - business focused'),
('theguardian.com', 89.7, 'left', 'high', 'UK', 'news', 'Progressive perspective with good fact-checking'),
('washingtonpost.com', 88.9, 'center-left', 'high', 'US', 'news', 'American newspaper with investigative journalism'),
('cnn.com', 85.6, 'center-left', 'medium', 'US', 'news', 'Cable news network with some bias concerns'),
('foxnews.com', 72.3, 'right', 'medium', 'US', 'news', 'Conservative perspective with factual issues'),
('dailymail.co.uk', 45.2, 'right', 'low', 'UK', 'news/tabloid', 'Tabloid with sensationalism'),
('theonion.com', 15.8, 'satire', 'low', 'US', 'satire', 'Satirical news site'),
('breitbart.com', 35.7, 'far-right', 'low', 'US', 'news', 'Controversial right-wing site'),
('infowars.com', 12.4, 'far-right', 'very-low', 'US', 'conspiracy', 'Conspiracy theory site');

-- Create triggers for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_articles_updated_at 
    BEFORE UPDATE ON articles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create view for article statistics
CREATE VIEW article_stats AS
SELECT 
    DATE_TRUNC('day', created_at) as analysis_date,
    COUNT(*) as total_analyses,
    AVG(credibility_score) as avg_credibility,
    AVG(fake_probability) as avg_fake_probability,
    COUNT(CASE WHEN credibility_score < 40 THEN 1 END) as low_credibility_count,
    COUNT(CASE WHEN credibility_score >= 80 THEN 1 END) as high_credibility_count
FROM articles 
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY analysis_date DESC;

-- Create view for source statistics
CREATE VIEW source_stats AS
SELECT 
    s.domain_name,
    s.reliability_score,
    s.bias_rating,
    COUNT(a.article_id) as analysis_count,
    AVG(a.credibility_score) as avg_article_credibility,
    AVG(a.fake_probability) as avg_fake_probability
FROM sources s
LEFT JOIN articles a ON a.url LIKE '%' || s.domain_name || '%'
GROUP BY s.source_id, s.domain_name, s.reliability_score, s.bias_rating
ORDER BY analysis_count DESC;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO truthlens_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO truthlens_user;

COMMIT;
