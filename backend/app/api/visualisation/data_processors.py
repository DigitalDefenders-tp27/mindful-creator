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
    
    try:
        # Get all data from the train_cleaned table
        data = get_train_cleaned_data()
        
        # Log the first few rows to debug column names
        if data and len(data) > 0:
            logger.info(f"Sample row from train_cleaned: {data[0]}")
            logger.info(f"Column names: {list(data[0].keys())}")
        else:
            logger.warning("No data returned from train_cleaned table")
        
        # Determine correct column names (could be daily_usage_time or daily_usage_time_minutes)
        usage_time_column = None
        emotion_column = None
        
        # Check what columns are actually in the data
        if data and len(data) > 0:
            sample_row = data[0]
            if 'daily_usage_time' in sample_row:
                usage_time_column = 'daily_usage_time'
            elif 'daily_usage_time_minutes' in sample_row:
                usage_time_column = 'daily_usage_time_minutes'
            
            if 'dominant_emotion' in sample_row:
                emotion_column = 'dominant_emotion'
            
            logger.info(f"Using columns: usage_time={usage_time_column}, emotion={emotion_column}")
        
        if not usage_time_column or not emotion_column:
            logger.error("Required columns not found in train_cleaned data")
            raise ValueError("Required columns missing in database")
        
        # Process the data in Python to create the time groups and emotion categories
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            if row.get(usage_time_column) is None or row.get(emotion_column) is None:
                skipped_rows += 1
                continue
            
            processed_rows += 1
                
            # Determine time group
            daily_usage = float(row[usage_time_column])
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
            emotion = str(row[emotion_column]).strip()
            time_groups[time_group]['total_count'] += 1
            
            if emotion in ('Happiness', 'Joy', 'Contentment'):
                time_groups[time_group]['positive_count'] += 1
            elif emotion in ('Anger', 'Sadness', 'Fear', 'Disgust'):
                time_groups[time_group]['negative_count'] += 1
            elif emotion in ('Neutral', 'Surprise'):
                time_groups[time_group]['neutral_count'] += 1
        
        logger.info(f"Processed {processed_rows} rows, skipped {skipped_rows} rows")
        logger.info(f"Time groups: {time_groups}")
                
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
        
        # Verify data format for Chart.js
        logger.info(f"Chart data structure: labels={len(chart_data['labels'])}, datasets={len(chart_data['datasets'])}")
        log_connection_details("process_screen_time_emotions", "completed", {"status": "success"})
        return chart_data
    except Exception as e:
        logger.error(f"Error processing screen time emotions: {e}")
        log_connection_details("process_screen_time_emotions", "failed", {"error": str(e)})
        raise

def process_sleep_data() -> Dict[str, Any]:
    """
    Process screen time and sleep quality data for the second chart
    
    Returns:
        Dict with labels and datasets for digital habits vs sleep chart
    """
    log_connection_details("process_sleep_data", "started")
    
    try:
        # Get all data from the smmh_cleaned table
        data = get_smmh_cleaned_data()
        
        # Log the first few rows to debug column names
        if data and len(data) > 0:
            logger.info(f"Sample row from smmh_cleaned: {data[0]}")
            logger.info(f"Column names: {list(data[0].keys())}")
        else:
            logger.warning("No data returned from smmh_cleaned table")
            
        # Determine the correct column names
        usage_group_column = None
        sleep_score_column = None
        
        # Common variations of the usage time group column
        usage_group_candidates = [
            'Usage_Time_Group', 
            'average_time_spent', 
            'usage_time_group'
        ]
        
        # Common variations of the sleep issue score column
        sleep_score_candidates = [
            '20. On a scale of 1 to 5, how often do you face issues regardin',
            'sleep_issue_score',
            'sleep_issues',
            'sleep_problems_score'
        ]
        
        # Find correct column names
        if data and len(data) > 0:
            sample_row = data[0]
            
            # Check for usage group column
            for col in usage_group_candidates:
                if col in sample_row:
                    usage_group_column = col
                    break
                    
            # Check for sleep score column
            for col in sleep_score_candidates:
                if col in sample_row:
                    sleep_score_column = col
                    break
                    
            logger.info(f"Using columns: usage_group={usage_group_column}, sleep_score={sleep_score_column}")
        
        if not usage_group_column or not sleep_score_column:
            logger.error("Required columns not found in smmh_cleaned data")
            raise ValueError("Required columns missing in database")
        
        # Process the data in Python to create the time groups and sleep scores
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            usage_time_group = row.get(usage_group_column)
            sleep_issue_score = row.get(sleep_score_column)
            
            if usage_time_group is None or sleep_issue_score is None:
                skipped_rows += 1
                continue
                
            processed_rows += 1
                
            # Convert to proper types
            usage_time_group = str(usage_time_group).strip()
            try:
                sleep_issue_score = float(sleep_issue_score)
            except (ValueError, TypeError):
                skipped_rows += 1
                continue
                
            # Initialize time group if not exists
            if usage_time_group not in time_groups:
                time_groups[usage_time_group] = {
                    'total_score': 0,
                    'count': 0
                }
                
            time_groups[usage_time_group]['total_score'] += sleep_issue_score
            time_groups[usage_time_group]['count'] += 1
        
        logger.info(f"Processed {processed_rows} rows, skipped {skipped_rows} rows")
        logger.info(f"Time groups: {time_groups}")
        
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
        
        # Verify data format for Chart.js
        logger.info(f"Chart data structure: labels={len(chart_data['labels'])}, datasets={len(chart_data['datasets'])}")
        log_connection_details("process_sleep_data", "completed", {"status": "success"})
        return chart_data
    except Exception as e:
        logger.error(f"Error processing sleep data: {e}")
        log_connection_details("process_sleep_data", "failed", {"error": str(e)})
        raise

def process_engagement_data() -> Dict[str, Any]:
    """
    Process screen time and engagement metrics for the third chart
    
    Returns:
        Dict with labels and datasets for engagement chart
    """
    log_connection_details("process_engagement_data", "started")
    
    try:
        # Get all data from the train_cleaned table
        data = get_train_cleaned_data()
        
        # Log the first few rows to debug column names
        if data and len(data) > 0:
            logger.info(f"Sample row from train_cleaned for engagement: {data[0]}")
            logger.info(f"Column names for engagement: {list(data[0].keys())}")
        else:
            logger.warning("No data returned from train_cleaned table for engagement")
            
        # Determine correct column names
        usage_time_column = None
        posts_column = None
        likes_column = None
        comments_column = None
        
        # Check what columns are actually in the data
        if data and len(data) > 0:
            sample_row = data[0]
            
            # Daily usage column
            if 'daily_usage_time' in sample_row:
                usage_time_column = 'daily_usage_time'
            elif 'daily_usage_time_minutes' in sample_row:
                usage_time_column = 'daily_usage_time_minutes'
                
            # Posts column
            if 'posts_per_day' in sample_row:
                posts_column = 'posts_per_day'
                
            # Likes column
            if 'likes_received_per_day' in sample_row:
                likes_column = 'likes_received_per_day'
                
            # Comments column
            if 'comments_received_per_day' in sample_row:
                comments_column = 'comments_received_per_day'
                
            logger.info(f"Using columns: usage={usage_time_column}, posts={posts_column}, likes={likes_column}, comments={comments_column}")
        
        if not usage_time_column or not posts_column or not likes_column or not comments_column:
            logger.error("Required columns not found in train_cleaned data for engagement")
            raise ValueError("Required columns missing in database for engagement metrics")
        
        # Process the data in Python to create the time groups and engagement scores
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            daily_usage = row.get(usage_time_column)
            posts = row.get(posts_column)
            likes = row.get(likes_column)
            comments = row.get(comments_column)
            
            if any(x is None for x in [daily_usage, posts, likes, comments]):
                skipped_rows += 1
                continue
                
            processed_rows += 1
                
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
                skipped_rows += 1
                continue
                
            # Initialize time group if not exists
            if time_group not in time_groups:
                time_groups[time_group] = {
                    'total_score': 0,
                    'count': 0
                }
                
            time_groups[time_group]['total_score'] += engagement_score
            time_groups[time_group]['count'] += 1
        
        logger.info(f"Processed {processed_rows} rows, skipped {skipped_rows} rows for engagement")
        logger.info(f"Engagement time groups: {time_groups}")
        
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
        
        # Verify data format for Chart.js
        logger.info(f"Engagement chart data structure: labels={len(chart_data['labels'])}, datasets={len(chart_data['datasets'])}")
        log_connection_details("process_engagement_data", "completed", {"status": "success"})
        return chart_data
    except Exception as e:
        logger.error(f"Error processing engagement data: {e}")
        log_connection_details("process_engagement_data", "failed", {"error": str(e)})
        raise

def process_anxiety_data() -> Dict[str, Any]:
    """
    Process screen time and anxiety levels for the fourth chart
    
    Returns:
        Dict with labels and datasets for anxiety chart
    """
    log_connection_details("process_anxiety_data", "started")
    
    try:
        # Get all data from the smmh_cleaned table
        data = get_smmh_cleaned_data()
        
        # Log the first few rows to debug column names
        if data and len(data) > 0:
            logger.info(f"Sample row from smmh_cleaned for anxiety: {data[0]}")
            logger.info(f"Column names for anxiety: {list(data[0].keys())}")
        else:
            logger.warning("No data returned from smmh_cleaned table for anxiety")
        
        # Determine the correct column names
        usage_group_column = None
        distraction_column = None
        worry_column = None
        concentration_column = None
        
        # Common variations of column names
        usage_group_candidates = [
            'Usage_Time_Group', 
            'average_time_spent', 
            'usage_time_group'
        ]
        
        distraction_candidates = [
            '12. On a scale of 1 to 5, how easily distracted are you?',
            'distraction_score',
            'distractibility_score'
        ]
        
        worry_candidates = [
            '13. On a scale of 1 to 5, how much are you bothered by worries?',
            'worry_score',
            'worries_score'
        ]
        
        concentration_candidates = [
            '14. Do you find it difficult to concentrate on things?',
            'concentration_difficulty_score',
            'concentration_score'
        ]
        
        # Find correct column names
        if data and len(data) > 0:
            sample_row = data[0]
            
            # Check for usage group column
            for col in usage_group_candidates:
                if col in sample_row:
                    usage_group_column = col
                    break
            
            # Check for distraction column
            for col in distraction_candidates:
                if col in sample_row:
                    distraction_column = col
                    break
                    
            # Check for worry column
            for col in worry_candidates:
                if col in sample_row:
                    worry_column = col
                    break
                    
            # Check for concentration column
            for col in concentration_candidates:
                if col in sample_row:
                    concentration_column = col
                    break
            
            logger.info(f"Using columns: usage={usage_group_column}, distraction={distraction_column}, worry={worry_column}, concentration={concentration_column}")
            
        if not usage_group_column or not distraction_column or not worry_column or not concentration_column:
            logger.error("Required columns not found in smmh_cleaned data for anxiety")
            raise ValueError("Required columns missing in database for anxiety metrics")
        
        # Process the data in Python to calculate anxiety levels
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            usage_time_group = row.get(usage_group_column)
            distraction_score = row.get(distraction_column)
            worry_score = row.get(worry_column)
            concentration_score = row.get(concentration_column)
            
            if usage_time_group is None or distraction_score is None or worry_score is None or concentration_score is None:
                skipped_rows += 1
                continue
                
            processed_rows += 1
                
            # Convert to proper types
            usage_time_group = str(usage_time_group).strip()
            try:
                distraction_score = float(distraction_score)
                worry_score = float(worry_score)
                concentration_score = float(concentration_score)
                anxiety_level = (distraction_score + worry_score + concentration_score) / 3.0
            except (ValueError, TypeError):
                skipped_rows += 1
                continue
                
            # Initialize time group if not exists
            if usage_time_group not in time_groups:
                time_groups[usage_time_group] = {
                    'total_score': 0,
                    'count': 0
                }
                
            time_groups[usage_time_group]['total_score'] += anxiety_level
            time_groups[usage_time_group]['count'] += 1
        
        logger.info(f"Processed {processed_rows} rows, skipped {skipped_rows} rows for anxiety")
        logger.info(f"Anxiety time groups: {time_groups}")
        
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
        
        # Verify data format for Chart.js
        logger.info(f"Anxiety chart data structure: labels={len(chart_data['labels'])}, datasets={len(chart_data['datasets'])}")
        log_connection_details("process_anxiety_data", "completed", {"status": "success"})
        return chart_data
    except Exception as e:
        logger.error(f"Error processing anxiety data: {e}")
        log_connection_details("process_anxiety_data", "failed", {"error": str(e)})
        raise

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
        
        tables = execute_query(query, timeout=30)
        
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
            result = execute_query(check_query, timeout=20)
            table_status[table] = result[0]['exists'] if result else False
            
            # If table exists, check record count
            if table_status[table]:
                count_query = f"SELECT COUNT(*) as count FROM {table}"
                count_result = execute_query(count_query, timeout=20)
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