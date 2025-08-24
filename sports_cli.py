#!/usr/bin/env python3
"""
Sports Data Extraction CLI
Command-line interface for extracting sports betting data via API
"""

import json
import argparse
import sys
from datetime import datetime
from api_client import SportsAPIClient


def print_colored(text, color='white'):
    """Print colored text to console"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")


def format_match_summary(match):
    """Format match data for display"""
    status = "🔴 LIVE" if match.get('is_live') else "⏰ Scheduled"
    teams = match.get('teams', 'Unknown vs Unknown')
    time = match.get('time', 'Unknown time')
    event_id = match.get('event_id', 'N/A')
    
    odds = match.get('main_odds', {})
    odds_text = ""
    if odds:
        home = odds.get('home_win', '-')
        draw = odds.get('draw', '-')
        away = odds.get('away_win', '-')
        odds_text = f" | Odds: {home} - {draw} - {away}"
    
    return f"{status} {teams} ({time}) | ID: {event_id}{odds_text}"


def format_event_details(details):
    """Format detailed event data for display"""
    if not details.get('success'):
        return f"❌ Error: {details.get('error')}"
    
    event_info = details.get('event_info', {})
    markets = details.get('betting_markets', [])
    
    output = []
    output.append("=" * 60)
    output.append(f"🏆 EVENT DETAILS - {event_info.get('name', 'Unknown Match')}")
    output.append("=" * 60)
    output.append(f"🕐 Start Time: {event_info.get('start_time', 'Unknown')}")
    output.append(f"⚽ Home Team: {event_info.get('home_team', 'Unknown')}")
    output.append(f"⚽ Away Team: {event_info.get('away_team', 'Unknown')}")
    output.append(f"📊 Status: {event_info.get('status', 'Unknown')}")
    output.append(f"🎯 Event ID: {event_info.get('event_id', 'Unknown')}")
    output.append(f"📈 Total Markets: {details.get('markets_count', 0)}")
    output.append("")
    
    # Categorize markets for better display
    market_categories = {
        'main_markets': [],
        'goals_markets': [],
        'handicap_markets': [],
        'player_markets': [],
        'events_markets': [],
        'other_markets': []
    }
    
    for market in markets:
        category = market.get('market_category', 'other_markets')
        market_categories[category].append(market)
    
    # Display categorized markets with better descriptions
    category_names = {
        'main_markets': '🎯 Main Markets (Match Results)',
        'goals_markets': '⚽ Goals & Scoring Markets', 
        'handicap_markets': '⚖️ Handicap Markets',
        'player_markets': '👤 Player & Team Specific',
        'events_markets': '📊 Game Events (Cards, Corners)',
        'other_markets': '🔀 Other Markets'
    }
    
    for category, category_markets in market_categories.items():
        if category_markets:
            category_name = category_names.get(category, category.replace('_', ' ').title())
            output.append(f"{category_name} ({len(category_markets)} markets):")
            output.append("-" * 50)
            
            for market in category_markets:  # Show ALL markets in each category
                market_desc = market.get('market_description', f"Market {market.get('market_type', 'Unknown')}")
                market_id = market.get('market_id', 'N/A')
                
                output.append(f"  📈 {market_desc} (ID: {market_id})")
                
                selections = market.get('selections', [])
                for selection in selections:
                    sel_name = selection.get('name', f"Selection {selection.get('selection_no', 'N/A')}")
                    odd_value = selection.get('odd', 'N/A')
                    status = selection.get('status', '')
                    
                    # Add status indicator
                    status_icon = "🔴" if status == "0" else "🟢" if status == "1" else ""
                    output.append(f"    • {sel_name}: {odd_value} {status_icon}")
                
                output.append("")
    
    return "\n".join(output)


def format_event_statistics(stats):
    """Format comprehensive event statistics for display"""
    if not stats.get('success'):
        return f"❌ Error: {stats.get('error')}"
    
    event_info = stats.get('event_info', {})
    tournament_standings = stats.get('tournament_standings', {})
    head_to_head = stats.get('head_to_head', {})
    recent_form = stats.get('recent_form', {})
    betting_analysis = stats.get('betting_analysis', {})
    referee_info = stats.get('referee_info', {})
    
    output = []
    output.append("=" * 70)
    output.append("📊 EVENT STATISTICS & ANALYSIS")
    output.append("=" * 70)
    
    # Event Information
    if event_info:
        home_team = event_info.get('home_team', {})
        away_team = event_info.get('away_team', {})
        tournament = event_info.get('tournament', {})
        venue = event_info.get('venue', {})
        
        output.append(f"🏆 {home_team.get('name', 'Home Team')} vs {away_team.get('name', 'Away Team')}")
        output.append(f"🕐 Event Date: {event_info.get('event_date', 'Unknown')}")
        output.append(f"⚽ Tournament: {tournament.get('name', 'Unknown')}")
        output.append(f"🏟️  Stadium: {venue.get('stadium', 'Unknown')}")
        
        if venue.get('temperature'):
            output.append(f"🌡️  Temperature: {venue.get('temperature')}°C")
        if venue.get('weather'):
            output.append(f"🌤️  Weather: {venue.get('weather')}")
        
        output.append("")
    
    # Tournament Standings
    if tournament_standings and tournament_standings.get('overall_table'):
        output.append("📊 TOURNAMENT STANDINGS")
        output.append("-" * 70)
        output.append(f"🏆 {tournament_standings.get('tournament_name', 'N/A')} - {tournament_standings.get('season', 'N/A')}")
        output.append("")
        
        # Overall table (top 10)
        output.append("🔢 Overall League Table (Top 10):")
        output.append("Pos | Team                    | P  | W | D | L | GF | GA | GD | Pts")
        output.append("-" * 68)
        for team in tournament_standings['overall_table'][:10]:
            pos = team.get('position', 0)
            name = team.get('team', {}).get('name', 'N/A')[:20].ljust(20)
            played = team.get('played', 0)
            won = team.get('won', 0)
            draw = team.get('draw', 0)
            lost = team.get('lost', 0)
            scored = team.get('scored', 0)
            against = team.get('against', 0)
            average = team.get('average', 0)
            points = team.get('points', 0)
            
            output.append(f"{pos:2} | {name} | {played:2} | {won} | {draw} | {lost} | {scored:2} | {against:2} | {average:+3} | {points:3.0f}")
        output.append("")
    
    # Head-to-head records
    if head_to_head and head_to_head.get('overall_matches'):
        output.append("⚔️  HEAD-TO-HEAD RECORD")
        output.append("-" * 50)
        output.append("Recent matches between teams:")
        output.append("")
        
        for match in head_to_head['overall_matches'][:8]:  # Last 8 matches
            home_team_name = match.get('homeTeam', {}).get('name', 'N/A')
            away_team_name = match.get('awayTeam', {}).get('name', 'N/A')
            home_score = match.get('homeTeamScore', {}).get('regular', 0)
            away_score = match.get('awayTeamScore', {}).get('regular', 0)
            tournament_name = match.get('tournamentInformation', {}).get('shortName', 'N/A')
            
            # Convert timestamp to readable date
            event_date = match.get('eventDate', 0)
            if event_date:
                try:
                    import datetime
                    date_str = datetime.datetime.fromtimestamp(event_date / 1000).strftime('%Y-%m-%d')
                except:
                    date_str = 'N/A'
            else:
                date_str = 'N/A'
            
            output.append(f"📅 {date_str} | {home_team_name} {home_score}-{away_score} {away_team_name} ({tournament_name})")
        output.append("")
    
    # Recent form
    if recent_form:
        output.append("📈 RECENT FORM")
        output.append("-" * 50)
        
        # Home team recent matches
        if recent_form.get('home_team', {}).get('recent_matches'):
            home_team_name = recent_form['home_team'].get('name', 'Home Team')
            output.append(f"🏠 {home_team_name} - Last 5 matches:")
            for match in recent_form['home_team']['recent_matches'][:5]:
                home_team = match.get('homeTeam', {}).get('shortName', 'N/A')
                away_team = match.get('awayTeam', {}).get('shortName', 'N/A')
                home_score = match.get('homeTeamScore', {}).get('regular', 0)
                away_score = match.get('awayTeamScore', {}).get('regular', 0)
                
                # Determine result from perspective of the team (simplified check)
                team_short = recent_form['home_team'].get('name', '').split()[-1][:3].upper()
                if home_team == team_short or team_short in home_team:
                    # Team was playing at home
                    if home_score > away_score:
                        result = "✅ W"
                    elif home_score < away_score:
                        result = "❌ L"
                    else:
                        result = "🤝 D"
                else:
                    # Team was playing away
                    if away_score > home_score:
                        result = "✅ W"
                    elif away_score < home_score:
                        result = "❌ L"
                    else:
                        result = "🤝 D"
                
                output.append(f"   {result} {home_team} {home_score}-{away_score} {away_team}")
            output.append("")
        
        # Away team recent matches
        if recent_form.get('away_team', {}).get('recent_matches'):
            away_team_name = recent_form['away_team'].get('name', 'Away Team')
            output.append(f"✈️  {away_team_name} - Last 5 matches:")
            for match in recent_form['away_team']['recent_matches'][:5]:
                home_team = match.get('homeTeam', {}).get('shortName', 'N/A')
                away_team = match.get('awayTeam', {}).get('shortName', 'N/A')
                home_score = match.get('homeTeamScore', {}).get('regular', 0)
                away_score = match.get('awayTeamScore', {}).get('regular', 0)
                
                # Determine result from perspective of the team (simplified check)
                team_short = recent_form['away_team'].get('name', '').split()[-1][:3].upper()
                if away_team == team_short or team_short in away_team:
                    # Team was playing away
                    if away_score > home_score:
                        result = "✅ W"
                    elif away_score < home_score:
                        result = "❌ L"
                    else:
                        result = "🤝 D"
                else:
                    # Team was playing home
                    if home_score > away_score:
                        result = "✅ W"
                    elif home_score < away_score:
                        result = "❌ L"
                    else:
                        result = "🤝 D"
                
                output.append(f"   {result} {home_team} {home_score}-{away_score} {away_team}")
            output.append("")
    
    # Betting analysis
    if betting_analysis:
        output.append("💰 BETTING ANALYSIS")
        output.append("-" * 50)
        
        # General information
        if betting_analysis.get('general_info'):
            output.append("📋 General Information:")
            for info in betting_analysis['general_info']:
                if info.get('text'):
                    output.append(f"   • {info['text']}")
            output.append("")
        
        # Market analysis
        if betting_analysis.get('market_analysis'):
            output.append("📊 Market Analysis:")
            for analysis in betting_analysis['market_analysis']:
                market_name = analysis.get('marketName', 'N/A')
                text = analysis.get('text', 'N/A')
                if text and text != 'N/A':
                    output.append(f"   🎯 {market_name}:")
                    # Split long text into multiple lines
                    for line in text.split('\n'):
                        if line.strip():
                            output.append(f"      {line.strip()}")
            output.append("")
    
    # Referee information
    if referee_info and referee_info.get('id', 0) > 0:
        output.append("👨‍⚖️ REFEREE INFORMATION")
        output.append("-" * 50)
        output.append(f"🆔 Referee ID: {referee_info.get('id', 'N/A')}")
        if referee_info.get('age', 0) > 0:
            output.append(f"� Age: {referee_info['age']}")
        if referee_info.get('country', {}).get('name'):
            output.append(f"🌍 Country: {referee_info['country']['name']}")
        output.append("")
    
    return "\n".join(output)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='Sports Data Extraction CLI - Extract betting data via API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sports_cli.py                           # Get recent matches
  python sports_cli.py --limit 10                # Get 10 matches
  python sports_cli.py --live                    # Get only live matches
  python sports_cli.py --event-details 2247399   # Get detailed odds for event
  python sports_cli.py --event-stats 2247399     # Get statistics for event
  python sports_cli.py --json                    # Output in JSON format
        """
    )
    
    parser.add_argument('--limit', '-l', type=int, default=10,
                       help='Maximum number of matches to retrieve (default: 10)')
    parser.add_argument('--live', action='store_true',
                       help='Show only live matches')
    parser.add_argument('--event-details', '-d', type=str,
                       help='Get detailed betting odds for specific event ID')
    parser.add_argument('--event-stats', '-s', type=str,
                       help='Get statistics and analysis for specific event ID')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output in JSON format')
    parser.add_argument('--no-cache', action='store_true',
                       help='Disable caching for fresh data')
    parser.add_argument('--timeout', type=int, default=20,
                       help='Request timeout in seconds (default: 20)')
    
    args = parser.parse_args()
    
    try:
        # Initialize the API client
        client = SportsAPIClient()
        
        # Handle event details request
        if args.event_details:
            print_colored(f"🔍 Fetching detailed odds for event {args.event_details}...", 'cyan')
            result = client.get_event_details(args.event_details, use_cache=not args.no_cache)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_event_details(result))
            
            return
        
        # Handle event statistics request  
        if args.event_stats:
            print_colored(f"📊 Fetching statistics for event {args.event_stats}...", 'cyan')
            result = client.get_event_statistics(args.event_stats, use_cache=not args.no_cache)
            
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_event_statistics(result))
            
            return
        
        # Handle regular matches request
        print_colored(f"⚽ Fetching sports matches (limit: {args.limit}, live only: {args.live})...", 'cyan')
        result = client.get_matches(limit=args.limit, live_only=args.live)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result.get('success'):
                print_colored(f"✅ Successfully retrieved {result['total_matches']} matches", 'green')
                print_colored(f"🕐 Timestamp: {result['timestamp']}", 'yellow')
                
                if result.get('cached'):
                    print_colored("📋 Data served from cache", 'yellow')
                
                print()
                
                for i, match in enumerate(result.get('matches', []), 1):
                    print(f"{i:2d}. {format_match_summary(match)}")
                
                print()
                print_colored("💡 Use --event-details <event_id> to get detailed odds", 'blue')
                print_colored("💡 Use --event-stats <event_id> to get match statistics", 'blue')
            else:
                print_colored(f"❌ Error: {result.get('error')}", 'red')
                sys.exit(1)
    
    except KeyboardInterrupt:
        print_colored("\n⚠️  Operation cancelled by user", 'yellow')
        sys.exit(1)
    except Exception as e:
        print_colored(f"💥 Unexpected error: {str(e)}", 'red')
        sys.exit(1)


if __name__ == "__main__":
    main()
