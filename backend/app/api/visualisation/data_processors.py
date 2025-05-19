import logging
from typing import Dict, List, Any, Optional
from sqlalchemy import func, case, cast, Float
from .database import execute_query, log_connection_details, get_train_cleaned_data, get_smmh_cleaned_data

logger = logging.getLogger("visualisation.processors")

def process_screen_time_emotions() -> Dict[str, Any]:
    """
    Process screen time and emotions data for the first chart using ORM
    
    Returns:
        Dict with labels and datasets for screen time vs emotions chart
    """
    log_connection_details("process_screen_time_emotions", "started")
    
    # Get all data from the train_cleaned table
    data = get_train_cleaned_data()
    
    # Process the data in Python to create the time groups and emotion categories
    time_groups = {}
    for row in data:
        if row.get('daily_usage_time') is None or row.get('dominant_emotion') is None:
            continue
            
        # Determine time group
        daily_usage = float(row['daily_usage_time'])
        if daily_usage < 60:
            time_group = 'Below 1h'
        elif 60 <= daily_usage <= 180:
            time_group = '1-3h'
        else:
            time_group = '3-5h'
            
        # Initialize time group if not exists
        if time_group not in time_groups:
            time_groups[time_group] = {
                'total_count': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0
            }
            
        # Categorize emotion
        emotion = str(row['dominant_emotion']).strip()
        time_groups[time_group]['total_count'] += 1
        
        if emotion in ('Happiness', 'Joy', 'Contentment'):
            time_groups[time_group]['positive_count'] += 1
        elif emotion in ('Anger', 'Sadness', 'Fear', 'Disgust'):
            time_groups[time_group]['negative_count'] += 1
        elif emotion in ('Neutral', 'Surprise'):
            time_groups[time_group]['neutral_count'] += 1
            
    # Calculate percentages
    results = []
    for time_group, counts in time_groups.items():
        total = counts['total_count']
        if total > 0:
            positive_pct = round((counts['positive_count'] * 100.0) / total, 1)
            negative_pct = round((counts['negative_count'] * 100.0) / total, 1)
            neutral_pct = round((counts['neutral_count'] * 100.0) / total, 1)
            
            results.append({
                'time_group': time_group,
                'positive_percentage': positive_pct,
                'negative_percentage': negative_pct,
                'neutral_percentage': neutral_pct
            })
            
    # Sort the results
    results.sort(key=lambda x: {
        'Below 1h': 1,
        '1-3h': 2,
        '3-5h': 3
    }.get(x['time_group'], 999))
    
    if not results:
        logger.warning("No screen time emotions data found in database")
        log_connection_details("process_screen_time_emotions", "completed", {"status": "no_data"})
        raise ValueError("No data found for screen time emotions visualization")
    
    # Format data for chart.js
    labels = [r['time_group'] for r in results]
    positive_data = [float(r['positive_percentage']) for r in results]
    negative_data = [float(r['negative_percentage']) for r in results]
    neutral_data = [float(r['neutral_percentage']) for r in results]
    
    chart_data = {
        "labels": labels,
        "datasets": [
            {"label": "Positive", "backgroundColor": "#4bc0c0", "data": positive_data},
            {"label": "Negative", "backgroundColor": "#ff6384", "data": negative_data},
            {"label": "Neutral", "backgroundColor": "#ffcd56", "data": neutral_data},
        ]
    }
    
    log_connection_details("process_screen_time_emotions", "completed", {"status": "success"})
    return chart_data

def process_sleep_data() -> Dict[str, Any]:
    """
    Process screen time and sleep quality data for the second chart
    
    Returns:
        Dict with labels and datasets for digital habits vs sleep chart
    """
    log_connection_details("process_sleep_data", "started")
    
    # Get all data from the smmh_cleaned table
    data = get_smmh_cleaned_data()
    
    # Process the data in Python to create the time groups and sleep scores
    time_groups = {}
    for row in data:
        usage_time_group = row.get('Usage_Time_Group')
        sleep_issue_score = row.get('20. On a scale of 1 to 5, how often do you face issues regardin')
        
        if usage_time_group is None or sleep_issue_score is None:
            continue
            
        # Convert to proper types
        usage_time_group = str(usage_time_group).strip()
        try:
            sleep_issue_score = float(sleep_issue_score)
        except (ValueError, TypeError):
            continue
            
        # Initialize time group if not exists
        if usage_time_group not in time_groups:
            time_groups[usage_time_group] = {
                'total_score': 0,
                'count': 0
            }
            
        time_groups[usage_time_group]['total_score'] += sleep_issue_score
        time_groups[usage_time_group]['count'] += 1
    
    # Calculate average scores
    results = []
    for time_group, data in time_groups.items():
        if data['count'] > 0:
            avg_score = round(data['total_score'] / data['count'], 2)
            results.append({
                'time_group': time_group,
                'sleep_problems_score': avg_score
            })
    
    # Sort the results by time group
    time_group_order = {
        '<1h': 1, '1-2h': 2, '2-3h': 3, '3-4h': 4, '4-5h': 5, '>5h': 6
    }
    results.sort(key=lambda x: time_group_order.get(x['time_group'], 999))
    
    if not results:
        logger.warning("No sleep data found in database")
        log_connection_details("process_sleep_data", "completed", {"status": "no_data"})
        raise ValueError("No data found for sleep quality visualization")
    
    # Format data for chart.js
    labels = [r['time_group'] for r in results]
    sleep_data = [float(r['sleep_problems_score']) for r in results]
    
    chart_data = {
        "labels": labels,
        "datasets": [{
            "label": "Sleep Problems (1-5)",
            "data": sleep_data,
            "borderColor": "#7e57c2",
            "backgroundColor": "#7e57c2",
            "fill": False,
            "tension": 0.3
        }]
    }
    
    log_connection_details("process_sleep_data", "completed", {"status": "success"})
    return chart_data

def process_engagement_data() -> Dict[str, Any]:
    """
    Process screen time and engagement metrics for the third chart
    
    Returns:
        Dict with labels and datasets for engagement chart
    """
    log_connection_details("process_engagement_data", "started")
    
    # Get all data from the train_cleaned table
    data = get_train_cleaned_data()
    
    # Process the data in Python to create the time groups and engagement scores
    time_groups = {}
    for row in data:
        daily_usage = row.get('daily_usage_time')
        posts = row.get('posts_per_day')
        likes = row.get('likes_received_per_day')
        comments = row.get('comments_received_per_day')
        
        if any(x is None for x in [daily_usage, posts, likes, comments]):
            continue
            
        # Determine time group
        daily_usage = float(daily_usage)
        if daily_usage < 60:
            time_group = 'Below 1h'
        elif 60 <= daily_usage <= 180:
            time_group = '1-3h'
        else:
            time_group = '3-5h'
            
        # Calculate engagement score
        try:
            posts = float(posts)
            likes = float(likes)
            comments = float(comments)
            engagement_score = (posts * 5) + (likes * 0.2) + (comments * 0.5)
        except (ValueError, TypeError):
            continue
            
        # Initialize time group if not exists
        if time_group not in time_groups:
            time_groups[time_group] = {
                'total_score': 0,
                'count': 0
            }
            
        time_groups[time_group]['total_score'] += engagement_score
        time_groups[time_group]['count'] += 1
    
    # Calculate average engagement scores
    results = []
    for time_group, data in time_groups.items():
        if data['count'] > 0:
            avg_score = round(data['total_score'] / data['count'], 1)
            results.append({
                'time_group': time_group,
                'avg_engagement': avg_score
            })
    
    # Sort the results
    results.sort(key=lambda x: {
        'Below 1h': 1,
        '1-3h': 2,
        '3-5h': 3
    }.get(x['time_group'], 999))
    
    if not results:
        logger.warning("No engagement data found in database")
        log_connection_details("process_engagement_data", "completed", {"status": "no_data"})
        raise ValueError("No data found for engagement visualization")
    
    # Format data for chart.js
    labels = [r['time_group'] for r in results]
    engagement_data = [float(r['avg_engagement']) for r in results]
    
    chart_data = {
        "labels": labels,
        "datasets": [{
            "label": "Engagement",
            "data": engagement_data,
            "backgroundColor": "#42a5f5"
        }]
    }
    
    log_connection_details("process_engagement_data", "completed", {"status": "success"})
    return chart_data

def process_anxiety_data() -> Dict[str, Any]:
    """
    Process screen time and anxiety levels for the fourth chart
    
    Returns:
        Dict with labels and datasets for anxiety chart
    """
    log_connection_details("process_anxiety_data", "started")
    
    # Get all data from the smmh_cleaned table
    data = get_smmh_cleaned_data()
    
    # Process the data in Python to calculate anxiety levels
    time_groups = {}
    for row in data:
        usage_time_group = row.get('Usage_Time_Group')
        distraction_score = row.get('12. On a scale of 1 to 5, how easily distracted are you?')
        worry_score = row.get('13. On a scale of 1 to 5, how much are you bothered by worries?')
        concentration_score = row.get('14. Do you find it difficult to concentrate on things?')
        
        if usage_time_group is None or distraction_score is None or worry_score is None or concentration_score is None:
            continue
            
        # Convert to proper types
        usage_time_group = str(usage_time_group).strip()
        try:
            distraction_score = float(distraction_score)
            worry_score = float(worry_score)
            concentration_score = float(concentration_score)
            anxiety_level = (distraction_score + worry_score + concentration_score) / 3.0
        except (ValueError, TypeError):
            continue
            
        # Initialize time group if not exists
        if usage_time_group not in time_groups:
            time_groups[usage_time_group] = {
                'total_score': 0,
                'count': 0
            }
            
        time_groups[usage_time_group]['total_score'] += anxiety_level
        time_groups[usage_time_group]['count'] += 1
    
    # Calculate average anxiety levels
    results = []
    for time_group, data in time_groups.items():
        if data['count'] > 0:
            avg_score = round(data['total_score'] / data['count'], 2)
            results.append({
                'time_group': time_group,
                'anxiety_level': avg_score
            })
    
    # Sort the results by time group
    time_group_order = {
        '<1h': 1, '1-2h': 2, '2-3h': 3, '3-4h': 4, '4-5h': 5, '>5h': 6
    }
    results.sort(key=lambda x: time_group_order.get(x['time_group'], 999))
    
    if not results:
        logger.warning("No anxiety data found in database")
        log_connection_details("process_anxiety_data", "completed", {"status": "no_data"})
        raise ValueError("No data found for anxiety visualization")
    
    # Format data for chart.js
    labels = [r['time_group'] for r in results]
    anxiety_data = [float(r['anxiety_level']) for r in results]
    
    chart_data = {
        "labels": labels,
        "datasets": [{
            "label": "Average Anxiety",
            "data": anxiety_data,
            "borderColor": "#66bb6a",
            "backgroundColor": "#66bb6a",
            "fill": False,
            "tension": 0.3
        }]
    }
    
    log_connection_details("process_anxiety_data", "completed", {"status": "success"})
    return chart_data

def test_database_connection() -> Dict[str, Any]:
    """
    Test function to verify database connectivity
    
    Returns:
        Dict with connection status and available tables
    """
    log_connection_details("test_database_connection", "started")
    try:
        # Test query to list all tables
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        
        tables = execute_query(query, timeout=10)
        
        # Test query to check if our specific tables exist
        required_tables = ['train_cleaned', 'smmh_cleaned']
        table_status = {}
        
        for table in required_tables:
            check_query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = '{table}'
            );
            """
            result = execute_query(check_query, timeout=5)
            table_status[table] = result[0]['exists'] if result else False
            
            # If table exists, check record count
            if table_status[table]:
                count_query = f"SELECT COUNT(*) as count FROM {table}"
                count_result = execute_query(count_query, timeout=5)
                table_status[f"{table}_count"] = count_result[0]['count'] if count_result else 0
        
        response = {
            "connection": "successful",
            "available_tables": [t['table_name'] for t in tables] if tables else [],
            "required_tables_status": table_status
        }
        
        log_connection_details("test_database_connection", "completed", response)
        return response
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        log_connection_details("test_database_connection", "failed", {"error": str(e)})
        return {
            "connection": "failed",
            "error": str(e)
        } 