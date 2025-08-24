# Sports Data API Client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

A professional Python API client for extracting sports betting data directly from APIs with advanced security features, intelligent caching, and comprehensive data processing capabilities.

## 🌟 Features

- **Direct API Access**: Pure API integration without browser automation
- **Advanced Security**: Anti-detection measures with realistic headers and human-like behavior
- **Intelligent Caching**: Multi-tier caching system with configurable durations
- **Rate Limiting**: Sophisticated request throttling to avoid API restrictions
- **Event Details**: Comprehensive betting markets and odds extraction
- **Statistics Integration**: Match statistics, standings, and analytical data
- **Environment Configuration**: Secure configuration management with .env files
- **Professional CLI**: Feature-rich command-line interface with multiple output formats

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your API endpoints
   ```

3. **Run the CLI**
   ```bash
   # Get recent matches
   python sports_cli.py

   # Get detailed odds for specific event
   python sports_cli.py --event-details 2247399

   # Get match statistics
   python sports_cli.py --event-stats 2247399
   ```

## 📖 API Usage

### Basic Usage

```python
from api_client import SportsAPIClient

# Initialize client
client = SportsAPIClient()

# Get matches
matches = client.get_matches(limit=10)

# Get event details
details = client.get_event_details("2247399")

# Get event statistics  
stats = client.get_event_statistics("2247399")
```

### Advanced Configuration

```python
# Custom cache duration (seconds)
client = SportsAPIClient(cache_duration=600)

# Disable caching for real-time data
details = client.get_event_details("2247399", use_cache=False)
```

## ⚙️ Configuration

Create a `.env` file with your API configuration:

```env
# API Base URLs
SPORTS_API_BASE_URL=https://api-v2.example.com
STATISTICS_API_BASE_URL=https://stats-v2.example.com

# API Endpoints
SPORTS_API_ENDPOINT=/sports/events

# Security Settings
MIN_REQUEST_INTERVAL=2.5
CACHE_DURATION=300
DETAIL_CACHE_DURATION=600

# Headers Configuration
USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
ORIGIN_URL=https://www.example.com
REFERER_URL=https://www.example.com/
```

## 🛡️ Security Features

- **Rate Limiting**: Configurable minimum intervals between requests
- **Realistic Headers**: Browser-like request headers with dynamic values
- **Human Simulation**: Random delays and natural request patterns
- **Anti-Detection**: Advanced techniques to avoid API restrictions
- **Transaction IDs**: Unique request identifiers for tracking

## 📊 Data Processing

### Event Details
- Comprehensive betting markets extraction
- Market categorization (main, goals, handicap, other)
- Detailed odds and selections processing
- Market metadata and status tracking

### Statistics Integration
- Tournament standings and league tables
- Head-to-head match history
- Team performance analytics
- Referee and venue information

## 🖥️ Command Line Interface

```bash
# Basic usage
python sports_cli.py                           # Get recent matches
python sports_cli.py --limit 10                # Get 10 matches
python sports_cli.py --live                    # Get only live matches

# Event analysis
python sports_cli.py --event-details 2247399   # Get detailed odds
python sports_cli.py --event-stats 2247399     # Get statistics

# Output options
python sports_cli.py --json                    # JSON output
python sports_cli.py --no-cache                # Disable caching
```

## 🏗️ Architecture

```
api_client.py       # Core API client with security and caching
sports_cli.py       # Command-line interface
.env               # Environment configuration
requirements.txt   # Python dependencies
```

## 📈 Performance

- **Caching System**: Reduces API calls with intelligent cache management
- **Rate Limiting**: Prevents API restrictions with configurable intervals
- **Parallel Processing**: Efficient data processing and extraction
- **Memory Management**: Optimized for large datasets and long-running sessions

## 🔧 Development

### Running Tests
```bash
# Test basic functionality
python sports_cli.py --limit 3

# Test event details
python sports_cli.py --event-details 2247399

# Test statistics
python sports_cli.py --event-stats 2247399
```

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📄 License

This project is for educational and research purposes. Please comply with the target APIs' terms of service and respect rate limits.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This is a professional-grade API client designed for legitimate data extraction purposes. Always ensure compliance with API terms of service and applicable laws.
