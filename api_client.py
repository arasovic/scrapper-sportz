#!/usr/bin/env python3
"""
Professional Sports Data API Client
Direct API access for sports betting data extraction
"""

import os
import time
import random
import json
import uuid
import requests
from datetime import datetime
from dotenv import load_dotenv
import validators


class SportsAPIClient:
    """Professional sports data API client with security and caching"""
    
    def __init__(self, cache_duration=300):
        """Initialize the API client with security and caching features"""
        # Load environment configuration
        load_dotenv()
        
        self.sports_api_base_url = os.getenv('SPORTS_API_BASE_URL', 'https://api-v2.example.com')
        self.stats_api_base_url = os.getenv('STATISTICS_API_BASE_URL', 'https://stats-v2.example.com')
        self.sports_api_endpoint = os.getenv('SPORTS_API_ENDPOINT', '/sports/events')
        self.default_sports_url = os.getenv('DEFAULT_SPORTS_URL', 'https://www.example.com/program/football')
        self.timeout = int(os.getenv('DEFAULT_TIMEOUT', 20))
        
        # Security and performance settings
        self.cache_duration = cache_duration or int(os.getenv('CACHE_DURATION', 300))
        self.detail_cache_duration = int(os.getenv('DETAIL_CACHE_DURATION', 600))
        self.cache = {}
        self.last_request_time = 0
        self.min_request_interval = float(os.getenv('MIN_REQUEST_INTERVAL', 2))
        
        # Logging
        self.logger = self._setup_logger()
        
        print(f"🚀 Sports API Client initialized")
        print(f"📡 Sports API: {self.sports_api_base_url}")
        print(f"📊 Stats API: {self.stats_api_base_url}")
    
    def _setup_logger(self):
        """Setup basic logging"""
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def _apply_rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            print(f"⏳ Rate limiting: waiting {sleep_time:.1f}s...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _get_enhanced_headers(self):
        """Generate realistic request headers"""
        client_transaction_id = str(uuid.uuid4())
        timestamp = str(int(time.time() * 1000))
        
        # Get configuration from environment
        user_agent = os.getenv('USER_AGENT', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        platform = os.getenv('BROWSER_PLATFORM', 'macOS')
        chrome_version = os.getenv('CHROME_VERSION', '139')
        origin_url = os.getenv('ORIGIN_URL', 'https://www.example.com')
        referer_url = os.getenv('REFERER_URL', 'https://www.example.com/')
        accept_language = os.getenv('ACCEPT_LANGUAGE', 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7')
        
        return {
            'User-Agent': f'{user_agent} (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': accept_language,
            'Accept-Encoding': 'gzip, deflate',  # Remove 'br' to avoid brotli issues
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Origin': origin_url,
            'Referer': referer_url,
            'X-Requested-With': 'XMLHttpRequest',
            'X-Client-Transaction-Id': client_transaction_id,
            'X-Request-Timestamp': timestamp,
            'DNT': '1',
            'Sec-GPC': '1'
        }
    
    def get_matches(self, limit=None, live_only=False):
        """
        Get sports matches from API
        
        Args:
            limit (int): Maximum number of matches to return
            live_only (bool): Return only live matches
            
        Returns:
            dict: API response with matches data
        """
        cache_key = f"matches_{limit}_{live_only}"
        
        # Check cache
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            cache_age = time.time() - cache_entry['timestamp']
            if cache_age < self.cache_duration:
                self.logger.info(f"Using cached matches data (age: {cache_age:.1f}s)")
                return cache_entry['data']
        
        try:
            print("🚀 Fetching matches from sports API...")
            
            # Apply rate limiting
            self._apply_rate_limit()
            
            # Build API URL
            api_url = f"{self.sports_api_base_url}{self.sports_api_endpoint}"
            
            # Add query parameters
            params = {
                'st': os.getenv('SPORTS_API_PARAMS_ST', '1'),
                'type': os.getenv('SPORTS_API_PARAMS_TYPE', '0'),
                'version': os.getenv('SPORTS_API_PARAMS_VERSION', '0')
            }
            
            # Make request with enhanced security headers
            headers = self._get_enhanced_headers()
            
            # Add human-like delay
            human_delay = random.uniform(1.5, 3.0)
            print(f"🤖 Human simulation delay: {human_delay:.1f}s")
            time.sleep(human_delay)
            
            response = requests.get(api_url, headers=headers, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process and filter data
                processed_data = self._process_matches_data(data, limit, live_only)
                
                # Cache the result
                self.cache[cache_key] = {
                    'data': processed_data,
                    'timestamp': time.time()
                }
                
                return processed_data
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.reason}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_event_details(self, event_id, use_cache=True):
        """
        Get detailed odds for a specific event
        
        Args:
            event_id (str): Event ID for which to get details
            use_cache (bool): Whether to use cached data if available
            
        Returns:
            dict: Event details with comprehensive betting markets
        """
        cache_key = f"event_details_{event_id}"
        
        # Check cache
        if use_cache and cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            cache_age = time.time() - cache_entry['timestamp']
            if cache_age < self.detail_cache_duration:
                print(f"📋 Using cached details for event {event_id}")
                return cache_entry['data']
        
        try:
            print(f"🔍 Fetching detailed odds for event {event_id}...")
            
            # Enhanced rate limiting for detail requests
            enhanced_interval = self.min_request_interval * 2
            current_time = time.time()
            if current_time - self.last_request_time < enhanced_interval:
                wait_time = enhanced_interval - (current_time - self.last_request_time)
                print(f"⏳ Enhanced rate limiting: waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
            
            # Build detail API URL
            detail_url = f"{self.sports_api_base_url}{self.sports_api_endpoint.replace('/events', '')}/event/{event_id}"
            headers = self._get_enhanced_headers()
            
            # Add extra human-like delay for detail requests
            extra_delay = random.uniform(2.0, 4.0)
            print(f"🤖 Human simulation delay: {extra_delay:.1f}s")
            time.sleep(extra_delay)
            
            response = requests.get(detail_url, headers=headers, timeout=self.timeout)
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('isSuccess') and 'data' in data:
                    event_data = data['data']
                    result = self._process_detailed_event(event_data, event_id)
                    
                    # Cache the result
                    if use_cache:
                        self.cache[cache_key] = {
                            'data': result,
                            'timestamp': time.time()
                        }
                    
                    print(f"✅ Retrieved detailed odds for event {event_id}")
                    return result
                else:
                    return {
                        "success": False,
                        "error": "API returned unsuccessful response",
                        "event_id": event_id,
                        "api_response": data.get('message', 'Unknown error')
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.reason}",
                    "event_id": event_id
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "event_id": event_id
            }
    
    def get_event_statistics(self, event_id, use_cache=True):
        """
        Get comprehensive statistics and analysis for a specific event
        
        Args:
            event_id (str): Event ID for which to get statistics
            use_cache (bool): Whether to use cached data if available
            
        Returns:
            dict: Event statistics including standings, head-to-head, analysis
        """
        cache_key = f"event_stats_{event_id}"
        
        # Check cache
        if use_cache and cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            cache_age = time.time() - cache_entry['timestamp']
            if cache_age < self.detail_cache_duration:
                print(f"📊 Using cached statistics for event {event_id}")
                return cache_entry['data']
        
        try:
            print(f"📊 Fetching statistics for event {event_id}...")
            
            # Enhanced rate limiting
            enhanced_interval = self.min_request_interval * 2
            current_time = time.time()
            if current_time - self.last_request_time < enhanced_interval:
                wait_time = enhanced_interval - (current_time - self.last_request_time)
                print(f"⏳ Enhanced rate limiting: waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
            
            # Build statistics API URL
            stats_url = f"{self.stats_api_base_url}/statistics/eventsummary/1/{event_id}"
            headers = self._get_enhanced_headers()
            
            # Add extra human-like delay
            extra_delay = random.uniform(2.0, 4.0)
            print(f"🤖 Human simulation delay: {extra_delay:.1f}s")
            time.sleep(extra_delay)
            
            response = requests.get(stats_url, headers=headers, timeout=self.timeout)
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                try:
                    # Use requests' built-in JSON parsing which handles compression automatically
                    data = response.json()
                except json.JSONDecodeError as e:
                    return {
                        "success": False,
                        "error": f"JSON parsing failed: {str(e)}",
                        "event_id": event_id
                    }
                
                if data.get('isSuccess') and 'data' in data:
                    stats_data = data['data']
                    result = self._process_event_statistics(stats_data, event_id)
                    
                    # Cache the result
                    if use_cache:
                        self.cache[cache_key] = {
                            'data': result,
                            'timestamp': time.time()
                        }
                    
                    print(f"✅ Retrieved statistics for event {event_id}")
                    return result
                else:
                    return {
                        "success": False,
                        "error": "API returned unsuccessful response",
                        "event_id": event_id,
                        "api_response": data.get('message', 'Unknown error')
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.reason}",
                    "event_id": event_id
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "event_id": event_id
            }
    
    def _process_matches_data(self, api_data, limit=None, live_only=False):
        """Process API response data and extract matches"""
        try:
            if not api_data.get('isSuccess') or 'data' not in api_data:
                return {
                    "success": False,
                    "error": "Invalid API response format",
                    "timestamp": datetime.now().isoformat()
                }
            
            events = api_data['data'].get('events', [])
            matches = []
            
            for event in events:
                # Filter live matches if requested
                if live_only and not event.get('il', False):
                    continue
                
                match_data = {
                    "event_id": event.get('i'),
                    "teams": f"{event.get('hn', '')} vs {event.get('an', '')}",
                    "home_team": event.get('hn', ''),
                    "away_team": event.get('an', ''),
                    "time": event.get('d', ''),
                    "is_live": event.get('il', False),
                    "status": event.get('s', ''),
                    "sport_id": event.get('sid', ''),
                    "main_odds": self._extract_main_odds(event.get('m', []))
                }
                
                matches.append(match_data)
                
                # Apply limit if specified
                if limit and len(matches) >= limit:
                    break
            
            return {
                "success": True,
                "total_matches": len(matches),
                "timestamp": datetime.now().isoformat(),
                "matches": matches,
                "cached": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing matches data: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_main_odds(self, markets):
        """Extract main 1X2 odds from markets"""
        main_odds = {}
        
        for market in markets:
            # Look for main 1X2 market (type 1)
            if market.get('t') == 1:
                odds = market.get('o', [])
                for odd in odds:
                    selection_no = odd.get('no')
                    odd_value = odd.get('odd')
                    
                    if selection_no == 1:
                        main_odds['home_win'] = odd_value
                    elif selection_no == 0:
                        main_odds['draw'] = odd_value
                    elif selection_no == 2:
                        main_odds['away_win'] = odd_value
                
                break  # Found main market, no need to continue
        
        return main_odds
    
    def _get_market_description(self, market_type, market_sub_type, special_odd_value):
        """Get descriptive name for market based on type and subtype"""
        market_key = f"{market_type}.{market_sub_type}"
        
        # Comprehensive market type mappings based on actual data
        market_descriptions = {
            # Type 1 - Match Result Markets
            "1.1": "1X2 - Match Result",
            "1.2": "1X2 - First Half",
            "1.3": "1X2 - Second Half", 
            
            # Type 2 - Goals and Statistics (extensive mapping)
            "2.92": "Double Chance",
            "2.719": "Odd/Even Total Goals",
            "2.720": "Both Teams to Score",
            "2.604": f"Total Goals Over/Under {special_odd_value or '2.5'}",
            "2.605": "Total Goals Over/Under 1.5",
            "2.606": "Total Goals Over/Under 3.5", 
            "2.607": "Total Goals Over/Under 0.5",
            "2.608": "Total Goals Over/Under 4.5",
            "2.85": "First Half 1X2",
            "2.88": "1X2 - Match Result (Alternative)",
            "2.36": "1X2 - Second Half", 
            "2.77": "Double Chance (Alternative)",
            "2.91": "Odd/Even (Alternative)",
            "2.89": "Both Teams to Score (Alternative)",
            "2.84": "First Half - 1X2",
            "2.4": "Goal Intervals (0-1/2-3/4-5/6+)",
            "2.821": "Both Teams to Score (Extended)",
            "2.730": "Team Clean Sheet",
            "2.729": "Win Either Half",
            "2.698": "1X2 & Both Teams Score",
            "2.699": "1X2 & Total Goals",
            "2.6": "First Half 1X2",
            "2.1": f"Match Result & Total Over/Under {special_odd_value or '2.5'}",
            
            # Type 3 - Correct Score
            "3.1": "Correct Score",
            "3.2": "Correct Score - First Half",
            
            # Type 4 - Asian Handicap  
            "4.1": f"Asian Handicap {special_odd_value or '0'}",
            "4.2": f"Asian Handicap - First Half {special_odd_value or '0'}",
            
            # Type 5 - Draw No Bet
            "5.1": "Draw No Bet",
            "5.2": "Draw No Bet - First Half",
            
            # Type 6 - European Handicap
            "6.1": f"European Handicap {special_odd_value or '0'}",
            "6.2": f"European Handicap - First Half {special_odd_value or '0'}",
            
            # Type 7 - Win to Nil
            "7.1": "Win to Nil",
            
            # Type 8 - Team Total Goals
            "8.1": f"Home Team Total Goals Over/Under {special_odd_value or '1.5'}",
            "8.2": f"Away Team Total Goals Over/Under {special_odd_value or '1.5'}",
            
            # Type 9 - Goal Scorers
            "9.1": "First Goal Scorer",
            "9.2": "Last Goal Scorer", 
            "9.3": "Anytime Goal Scorer",
            
            # Type 10 - Half Time / Full Time
            "10.1": "Half Time / Full Time",
            
            # Type 11 - Corners
            "11.1": f"Corners Over/Under {special_odd_value or '9.5'}",
            "11.2": f"Corners Handicap {special_odd_value or '0'}",
            
            # Type 12 - Cards
            "12.1": f"Cards Over/Under {special_odd_value or '3.5'}",
            "12.2": f"Cards Handicap {special_odd_value or '0'}",
        }
        
        # Try exact match first
        if market_key in market_descriptions:
            return market_descriptions[market_key]
        
        # For Type 2 markets with various subtypes, provide better descriptions
        if market_type == "2":
            if special_odd_value:
                # If there's a special odd value, it's likely an over/under market
                if any(sel in ['Alt', 'Üst', 'Over', 'Under'] for sel in ['']):
                    return f"Over/Under {special_odd_value}"
                elif any(sel in ['1', '0', '2'] for sel in ['']):
                    return f"1X2 with Special Value ({special_odd_value})"
                else:
                    return f"Goals & Statistics ({special_odd_value})"
            else:
                # Common Type 2 patterns
                subtype_patterns = {
                    "85": "First Half 1X2",
                    "88": "1X2 Alternative", 
                    "36": "Second Half 1X2",
                    "77": "Double Chance",
                    "91": "Odd/Even",
                    "89": "Both Teams to Score",
                    "84": "First Half Result",
                    "4": "Goal Intervals",
                    "821": "Both Teams to Score Extended",
                    "730": "Team Clean Sheet",
                    "729": "Win Either Half",
                    "698": "1X2 & Both Teams Score Combo",
                    "699": "1X2 & Total Goals Combo",
                    "6": "First Half 1X2"
                }
                
                if market_sub_type in subtype_patterns:
                    return subtype_patterns[market_sub_type]
        
        # Try main type match for other types
        main_type_descriptions = {
            "1": "Match Result Markets",
            "2": "Goals and Statistics", 
            "3": "Correct Score",
            "4": "Asian Handicap",
            "5": "Draw No Bet",
            "6": "European Handicap",
            "7": "Win to Nil",
            "8": "Team Total Goals",
            "9": "Goal Scorers",
            "10": "Half Time / Full Time",
            "11": "Corners",
            "12": "Cards",
            "13": "Specials",
            "14": "Player Props",
            "15": "Team Props"
        }
        
        main_desc = main_type_descriptions.get(str(market_type), f"Market Type {market_type}")
        
        if special_odd_value:
            return f"{main_desc} ({special_odd_value})"
        else:
            return f"{main_desc}.{market_sub_type}"
    
    def _categorize_market(self, market_type, market_sub_type):
        """Categorize market into logical groups"""
        market_type = str(market_type)
        
        # Main result markets
        if market_type in ['1', '5', '10']:
            return 'main_markets'
        
        # Goals related markets  
        elif market_type in ['2', '3', '8']:
            return 'goals_markets'
        
        # Handicap markets
        elif market_type in ['4', '6']:
            return 'handicap_markets'
            
        # Player/team specific markets
        elif market_type in ['7', '9', '14', '15']:
            return 'player_markets'
            
        # Game events (corners, cards, etc.)
        elif market_type in ['11', '12', '13']:
            return 'events_markets'
            
        else:
            return 'other_markets'

    def _process_detailed_event(self, event_data, event_id):
        """Process detailed event data with all betting markets"""
        try:
            result = {
                "success": True,
                "event_id": event_id,
                "timestamp": datetime.now().isoformat(),
                "event_info": {
                    "name": f"{event_data.get('hn', '')} vs {event_data.get('an', '')}",
                    "home_team": event_data.get('hn', ''),
                    "away_team": event_data.get('an', ''),
                    "start_time": event_data.get('d', ''),
                    "status": event_data.get('s', ''),
                    "is_live": event_data.get('il', False),
                    "sport_id": event_data.get('sid', ''),
                    "event_id": event_data.get('i', ''),
                    "match_bet_count": event_data.get('mbc', 0)
                },
                "markets_count": len(event_data.get('m', [])),
                "betting_markets": []
            }
            
            # Process all betting markets
            markets = event_data.get('m', [])
            for market in markets:
                market_type = market.get('t', '')
                market_sub_type = market.get('st', '')
                special_odd_value = market.get('sov', '')
                
                market_info = {
                    "market_id": market.get('i'),
                    "market_type": market_type,
                    "market_sub_type": market_sub_type,
                    "market_description": self._get_market_description(market_type, market_sub_type, special_odd_value),
                    "market_category": self._categorize_market(market_type, market_sub_type),
                    "status": market.get('s', ''),
                    "version": market.get('v', ''),
                    "special_odd_value": special_odd_value,
                    "selections": []
                }
                
                # Process selections/odds
                odds = market.get('o', [])
                for odd in odds:
                    selection_info = {
                        "selection_no": odd.get('no'),
                        "name": odd.get('n', ''),
                        "odd": odd.get('odd'),
                        "winning_odd": odd.get('wodd'),
                        "status": odd.get('s', '')
                    }
                    market_info["selections"].append(selection_info)
                
                result["betting_markets"].append(market_info)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing detailed event: {str(e)}",
                "event_id": event_id,
                "raw_data": event_data
            }
    
    def _process_event_statistics(self, stats_data, event_id):
        """Process event statistics data"""
        try:
            result = {
                "success": True,
                "event_id": event_id,
                "timestamp": datetime.now().isoformat(),
                "event_info": {},
                "tournament_standings": {},
                "head_to_head": {},
                "recent_matches": {},
                "betting_analysis": {},
                "referee_info": {},
                "team_stats": {}
            }
            
            # Event information
            event_info = stats_data.get('eventInformationModel', {})
            if event_info:
                result["event_info"] = {
                    "event_id": event_info.get('eventId'),
                    "event_date": event_info.get('eventDate'),
                    "home_team": {
                        "id": event_info.get('homeTeam', {}).get('id'),
                        "name": event_info.get('homeTeam', {}).get('name'),
                        "short_name": event_info.get('homeTeam', {}).get('shortName'),
                        "logo": event_info.get('homeTeam', {}).get('logo')
                    },
                    "away_team": {
                        "id": event_info.get('awayTeam', {}).get('id'),
                        "name": event_info.get('awayTeam', {}).get('name'),
                        "short_name": event_info.get('awayTeam', {}).get('shortName'),
                        "logo": event_info.get('awayTeam', {}).get('logo')
                    },
                    "tournament": {
                        "id": event_info.get('tournamentInformation', {}).get('id'),
                        "name": event_info.get('tournamentInformation', {}).get('name'),
                        "short_name": event_info.get('tournamentInformation', {}).get('shortName')
                    },
                    "round": {
                        "id": event_info.get('roundInformation', {}).get('id'),
                        "name": event_info.get('roundInformation', {}).get('name'),
                        "short_name": event_info.get('roundInformation', {}).get('shortName')
                    },
                    "status": {
                        "id": event_info.get('statusInformation', {}).get('id'),
                        "name": event_info.get('statusInformation', {}).get('name')
                    },
                    "venue": {
                        "stadium": event_info.get('eventPlaceInformation', {}).get('stadiumName'),
                        "temperature": event_info.get('eventPlaceInformation', {}).get('temperatureC'),
                        "weather": event_info.get('eventPlaceInformation', {}).get('weatherStatus')
                    }
                }
            
            # Tournament standings
            if 'tournamentStandingsModel' in stats_data:
                standings_data = stats_data['tournamentStandingsModel']
                if standings_data and len(standings_data) > 0:
                    result["tournament_standings"] = {
                        "tournament_name": standings_data[0].get('tournamentName'),
                        "season": standings_data[0].get('name'),
                        "overall_table": standings_data[0].get('overAll', []),
                        "home_table": standings_data[0].get('homeTeam', []),
                        "away_table": standings_data[0].get('awayTeam', [])
                    }
            
            # Head-to-head records
            if 'recentEventModel' in stats_data:
                h2h_data = stats_data['recentEventModel']
                if h2h_data:
                    result["head_to_head"] = {
                        "overall_matches": h2h_data.get('overall', []),
                        "home_team_matches": h2h_data.get('homeTeam', []),
                        "away_team_matches": h2h_data.get('awayTeam', [])
                    }
            
            # Recent form
            if 'lastEventModel' in stats_data:
                form_data = stats_data['lastEventModel']
                if form_data:
                    result["recent_form"] = {
                        "home_team": {
                            "id": form_data.get('homeTeam', {}).get('id'),
                            "name": form_data.get('homeTeam', {}).get('name'),
                            "recent_matches": form_data.get('homeOverAll', [])
                        },
                        "away_team": {
                            "id": form_data.get('awayTeam', {}).get('id'),
                            "name": form_data.get('awayTeam', {}).get('name'),
                            "recent_matches": form_data.get('awayOverAll', [])
                        }
                    }
            
            # Betting analysis
            if 'soccerIddaaAnalysModel' in stats_data:
                betting_data = stats_data['soccerIddaaAnalysModel']
                if betting_data:
                    result["betting_analysis"] = {
                        "general_info": betting_data.get('generalInformations', []),
                        "market_analysis": betting_data.get('bettingAnalysis', [])
                    }
            
            # Referee information
            if 'soccerRefereePageModel' in stats_data:
                ref_data = stats_data['soccerRefereePageModel']
                if ref_data and ref_data.get('referee', {}).get('id', 0) > 0:
                    result["referee_info"] = {
                        "id": ref_data.get('referee', {}).get('id'),
                        "age": ref_data.get('referee', {}).get('age'),
                        "country": ref_data.get('referee', {}).get('country', {}),
                        "tournaments": ref_data.get('refereeTournaments', []),
                        "recent_matches": ref_data.get('refereeMatches', [])
                    }
            
            # Tournament standings
            standings_data = stats_data.get('leagueTableModel', {})
            if standings_data:
                result["tournament_standings"] = {
                    "home_team_position": standings_data.get('homeTeamPosition'),
                    "away_team_position": standings_data.get('awayTeamPosition'),
                    "league_table": []
                }
                
                league_table = standings_data.get('leagueTable', [])
                for team in league_table:
                    result["tournament_standings"]["league_table"].append({
                        "position": team.get('position'),
                        "team_name": team.get('teamName'),
                        "played": team.get('played'),
                        "won": team.get('won'),
                        "drawn": team.get('drawn'),
                        "lost": team.get('lost'),
                        "goals_for": team.get('goalsFor'),
                        "goals_against": team.get('goalsAgainst'),
                        "goal_difference": team.get('goalDifference'),
                        "points": team.get('points')
                    })
            
            # Head to head statistics
            h2h_data = stats_data.get('headToHeadModel', {})
            if h2h_data:
                result["head_to_head"] = {
                    "total_matches": h2h_data.get('totalMatches'),
                    "home_team_wins": h2h_data.get('homeTeamWins'),
                    "away_team_wins": h2h_data.get('awayTeamWins'),
                    "draws": h2h_data.get('draws'),
                    "recent_matches": []
                }
                
                recent_h2h = h2h_data.get('headToHeadMatches', [])
                for match in recent_h2h:
                    result["head_to_head"]["recent_matches"].append({
                        "date": match.get('matchDate'),
                        "home_team": match.get('homeTeamName'),
                        "away_team": match.get('awayTeamName'),
                        "score": f"{match.get('homeTeamScore')}-{match.get('awayTeamScore')}",
                        "tournament": match.get('tournamentName')
                    })
            
            # Recent form for both teams
            recent_form = stats_data.get('recentFormModel', {})
            if recent_form:
                result["recent_matches"] = {
                    "home_team_form": [],
                    "away_team_form": []
                }
                
                home_form = recent_form.get('homeTeamForm', [])
                for match in home_form:
                    result["recent_matches"]["home_team_form"].append({
                        "date": match.get('matchDate'),
                        "opponent": match.get('opponentName'),
                        "result": match.get('result'),
                        "score": f"{match.get('homeScore')}-{match.get('awayScore')}",
                        "home_away": match.get('homeAway'),
                        "tournament": match.get('tournamentName')
                    })
                
                away_form = recent_form.get('awayTeamForm', [])
                for match in away_form:
                    result["recent_matches"]["away_team_form"].append({
                        "date": match.get('matchDate'),
                        "opponent": match.get('opponentName'),
                        "result": match.get('result'),
                        "score": f"{match.get('homeScore')}-{match.get('awayScore')}",
                        "home_away": match.get('homeAway'),
                        "tournament": match.get('tournamentName')
                    })
            
            # Betting analysis and odds movement
            betting_data = stats_data.get('bettingAnalysisModel', {})
            if betting_data:
                result["betting_analysis"] = {
                    "opening_odds": {
                        "home": betting_data.get('openingOdds', {}).get('home'),
                        "draw": betting_data.get('openingOdds', {}).get('draw'),
                        "away": betting_data.get('openingOdds', {}).get('away')
                    },
                    "current_odds": {
                        "home": betting_data.get('currentOdds', {}).get('home'),
                        "draw": betting_data.get('currentOdds', {}).get('draw'),
                        "away": betting_data.get('currentOdds', {}).get('away')
                    },
                    "odds_movement": betting_data.get('oddsMovement', [])
                }
            
            # Referee information
            referee_data = stats_data.get('refereeInformation', {})
            if referee_data:
                result["referee_info"] = {
                    "name": referee_data.get('refereeName'),
                    "nationality": referee_data.get('nationality'),
                    "experience": {
                        "total_matches": referee_data.get('totalMatches'),
                        "yellow_cards_per_match": referee_data.get('avgYellowCards'),
                        "red_cards_per_match": referee_data.get('avgRedCards'),
                        "penalties_per_match": referee_data.get('avgPenalties')
                    }
                }
            
            # Team statistics comparison
            team_stats = stats_data.get('teamStatisticsModel', {})
            if team_stats:
                result["team_stats"] = {
                    "home_team": {
                        "attack_strength": team_stats.get('homeTeam', {}).get('attackStrength'),
                        "defense_strength": team_stats.get('homeTeam', {}).get('defenseStrength'),
                        "recent_form_points": team_stats.get('homeTeam', {}).get('recentFormPoints'),
                        "avg_goals_scored": team_stats.get('homeTeam', {}).get('avgGoalsScored'),
                        "avg_goals_conceded": team_stats.get('homeTeam', {}).get('avgGoalsConceded'),
                        "home_advantage": team_stats.get('homeTeam', {}).get('homeAdvantage')
                    },
                    "away_team": {
                        "attack_strength": team_stats.get('awayTeam', {}).get('attackStrength'),
                        "defense_strength": team_stats.get('awayTeam', {}).get('defenseStrength'),
                        "recent_form_points": team_stats.get('awayTeam', {}).get('recentFormPoints'),
                        "avg_goals_scored": team_stats.get('awayTeam', {}).get('avgGoalsScored'),
                        "avg_goals_conceded": team_stats.get('awayTeam', {}).get('avgGoalsConceded'),
                        "away_performance": team_stats.get('awayTeam', {}).get('awayPerformance')
                    }
                }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing event statistics: {str(e)}",
                "event_id": event_id,
                "raw_data": stats_data
            }


def main():
    """Demo usage"""
    client = SportsAPIClient()
    
    # Test getting matches
    result = client.get_matches(limit=3)
    
    if result["success"]:
        print(f"✅ Found {result['total_matches']} matches")
        for i, match in enumerate(result['matches'], 1):
            print(f"{i}. {match['teams']} - Event ID: {match['event_id']}")
    else:
        print(f"❌ Error: {result.get('error')}")


if __name__ == "__main__":
    main()
