import logging
from typing import Dict, List, Any, Optional
from sqlalchemy import func, case, cast, Float
from .database import (
    execute_query,
    log_connection_details,
    get_train_cleaned_data_orm,
    get_smmh_cleaned_data_orm,
    get_db,
    time_limit,
    TrainCleaned,
    SmmhCleaned
)
from sqlalchemy.sql import text
from sqlalchemy.engine import Engine
from fastapi import Depends

logger = logging.getLogger("mindful-creator.visualisation.processors")

def create_chart_response(labels: List[str], 
                         datasets: List[Dict[str, Any]], 
                         chart_type: str = 'bar',
                         operation: str = 'chart_processing') -> Dict[str, Any]:
    """
    Create a standardized chart response format
    
    Args:
        labels: List of labels for the chart's x-axis
        datasets: List of dataset objects with data, labels, and styling
        chart_type: Type of chart (bar, line, etc.)
        operation: Name of the operation for logging
        
    Returns:
        Standardized chart data structure compatible with Chart.js
    """
    if not labels or not datasets:
        error_msg = f"Cannot create chart response: labels or datasets are empty"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    # Validate each dataset has required properties
    for i, dataset in enumerate(datasets):
        if 'data' not in dataset:
            error_msg = f"Dataset at index {i} is missing 'data' property"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if 'label' not in dataset:
            logger.warning(f"Dataset at index {i} is missing 'label' property, setting default")
            dataset['label'] = f"Dataset {i+1}"
            
    chart_data = {
        "labels": labels,
        "datasets": datasets,
        "type": chart_type  # Can be used by frontend to determine chart type
    }
    
    # Verify data format for Chart.js
    logger.info(f"Chart data structure: labels={len(chart_data['labels'])}, " +
                f"datasets={len(chart_data['datasets'])}, type={chart_type}")
    log_connection_details(operation, "completed", {"status": "success"})
    
    return chart_data

def process_screen_time_emotions(db_session) -> Dict[str, Any]:
    """
    Process screen time and emotions data for the first chart using ORM
    
    Returns:
        Dict with labels and datasets for screen time vs emotions chart
    """
    log_connection_details("process_screen_time_emotions", "started", {"session_id": id(db_session)})
    
    try:
        # Get all required columns from the train_cleaned table
        columns_needed = [
            "daily_usage_time", 
            "dominant_emotion"
        ]
        data = get_train_cleaned_data_orm(db_session, columns_to_load=columns_needed)
        
        if not data or len(data) == 0:
            logger.warning("process_screen_time_emotions: No data returned from train_cleaned table.")
            raise ValueError("No data found for screen time emotions visualization (train_cleaned empty or query failed)")
        
        # Log received data structure
        logger.info(f"process_screen_time_emotions: Sample row received from get_train_cleaned_data_orm: {data[0]}")
        logger.info(f"process_screen_time_emotions: Keys in sample row: {list(data[0].keys())}")

        # Validate required columns exist
        sample_row_keys = list(data[0].keys()) if data else []
        has_usage_time = "daily_usage_time" in sample_row_keys
        has_emotion = "dominant_emotion" in sample_row_keys
        
        logger.info(f"Column availability: daily_usage_time={has_usage_time}, dominant_emotion={has_emotion}")
        
        if not has_usage_time:
            error_msg = "Required column 'daily_usage_time' not found in train_cleaned data"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if not has_emotion:
            error_msg = "Required column 'dominant_emotion' not found in train_cleaned data"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Process the data in Python to create the time groups and emotion categories
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            if row.get("daily_usage_time") is None or row.get("dominant_emotion") is None:
                skipped_rows += 1
                logger.debug(f"Skipping row with missing data: daily_usage_time={row.get('daily_usage_time')}, dominant_emotion={row.get('dominant_emotion')}")
                continue
            
            processed_rows += 1
                
            # Determine time group - convert to float and handle possible errors
            try:
                daily_usage = float(row["daily_usage_time"])
            except (ValueError, TypeError):
                logger.debug(f"Skipping row with invalid daily_usage_time: {row['daily_usage_time']}")
                skipped_rows += 1
                continue
                
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
                
            # Categorize emotion - use lower case for comparisons to handle case variations
            emotion = str(row["dominant_emotion"]).strip().lower()
            time_groups[time_group]['total_count'] += 1
            
            if emotion in ('happiness', 'joy', 'contentment'):
                time_groups[time_group]['positive_count'] += 1
            elif emotion in ('anger', 'sadness', 'fear', 'disgust'):
                time_groups[time_group]['negative_count'] += 1
            elif emotion in ('neutral', 'surprise'):
                time_groups[time_group]['neutral_count'] += 1
            else:
                # Handle unknown emotions by logging and categorizing as neutral
                logger.debug(f"Unknown emotion type: {emotion}, categorizing as neutral")
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

def process_sleep_data(db_session) -> Dict[str, Any]:
    """
    Process screen time and sleep quality data for the second chart
    
    Returns:
        Dict with labels and datasets for digital habits vs sleep chart
    """
    log_connection_details("process_sleep_data", "started", {"session_id": id(db_session)})
    
    try:
        # Specify only the columns needed from SmmhCleaned model by their attribute names
        columns_needed = [
            "usage_time_group", # ORM attribute name (maps to DB "Usage_Time_Group")
            "q20_sleep_issues_scale",  # New ORM attribute name for sleep issues
            "q8_avg_sm_time"  # Fallback column in case usage_time_group is missing
        ]
        data = get_smmh_cleaned_data_orm(db_session, columns_to_load=columns_needed)
        
        if not data or len(data) == 0:
            logger.warning("No data returned from SmmhCleaned for sleep data processing after requesting specific columns.")
            raise ValueError("No data found for sleep quality visualization (columns might be missing or table empty).")

        # Log the first few rows to debug column names actually received
        logger.info(f"Sample row from smmh_cleaned (sleep_data): {data[0] if data else 'N/A'}")
        logger.info(f"Column names received (sleep_data): {list(data[0].keys()) if data else 'N/A'}")
        
        # Check if usage_time_group is available, if not create it from avg_sm_time
        sample_row_keys = list(data[0].keys()) if data else []
        has_usage_time_group = "usage_time_group" in sample_row_keys
        has_sleep_scale = "q20_sleep_issues_scale" in sample_row_keys
        has_avg_sm_time = "q8_avg_sm_time" in sample_row_keys
        
        if not has_sleep_scale:
            logger.error("Required column 'q20_sleep_issues_scale' not found in fetched smmh_cleaned data")
            raise ValueError(f"Required column 'q20_sleep_issues_scale' not found in smmh_cleaned data")
            
        logger.info(f"Column availability: usage_time_group={has_usage_time_group}, sleep_scale={has_sleep_scale}, avg_sm_time={has_avg_sm_time}")
            
        # If usage_time_group is missing but we have avg_sm_time, create a mapping
        if not has_usage_time_group and has_avg_sm_time:
            logger.warning("Missing usage_time_group column, will create from q8_avg_sm_time")
            
            # Categorize time from text responses like "1-2 hours", "Less than 1 hour", etc.
            time_mappings = {
                "less than 1 hour": "<1h",
                "1-2 hours": "1-2h",
                "2-3 hours": "2-3h",
                "3-4 hours": "3-4h",
                "4-5 hours": "4-5h",
                "more than 5 hours": ">5h"
            }
            
            # Add usage_time_group to each row
            for row in data:
                avg_time = str(row.get("q8_avg_sm_time", "")).lower().strip()
                row["usage_time_group"] = time_mappings.get(avg_time, "unknown")
            
            logger.info(f"Created usage_time_group from q8_avg_sm_time. Sample: {data[0]['usage_time_group'] if data else 'N/A'}")
        
        # Process the data in Python to create the time groups and sleep scores
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            usage_time_group = row.get("usage_time_group")
            sleep_issue_score = row.get("q20_sleep_issues_scale")
            
            if usage_time_group is None or sleep_issue_score is None:
                skipped_rows += 1
                logger.debug(f"Skipping row with missing data: usage_time_group={usage_time_group}, sleep_issues={sleep_issue_score}")
                continue
                
            processed_rows += 1
                
            # Convert to proper types
            usage_time_group = str(usage_time_group).strip()
            try:
                sleep_issue_score = float(sleep_issue_score)
            except (ValueError, TypeError):
                skipped_rows += 1
                logger.debug(f"Skipping row with invalid sleep_issue_score: {sleep_issue_score}")
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

def process_engagement_data(db_session) -> Dict[str, Any]:
    """
    Process screen time and engagement metrics for the third chart
    
    Returns:
        Dict with labels and datasets for engagement chart
    """
    log_connection_details("process_engagement_data", "started", {"session_id": id(db_session)})
    
    try:
        # Request specific columns needed for this chart
        columns_needed = [
            "daily_usage_time",
            "posts_per_day",
            "likes_received_per_day",
            "comments_received_per_day"
        ]
        
        data = get_train_cleaned_data_orm(db_session, columns_to_load=columns_needed)
        
        if not data or len(data) == 0:
            logger.warning("process_engagement_data: No data returned from train_cleaned table.")
            raise ValueError("No data found for engagement visualization (train_cleaned empty or query failed)")

        # Log received data structure
        logger.info(f"process_engagement_data: Sample row received from get_train_cleaned_data_orm: {data[0]}")
        logger.info(f"process_engagement_data: Keys in sample row: {list(data[0].keys())}")
            
        # Validate required columns exist
        sample_row_keys = list(data[0].keys()) if data else []
        has_usage_time = "daily_usage_time" in sample_row_keys
        has_posts = "posts_per_day" in sample_row_keys
        has_likes = "likes_received_per_day" in sample_row_keys
        has_comments = "comments_received_per_day" in sample_row_keys
        
        logger.info(f"Column availability: daily_usage_time={has_usage_time}, posts={has_posts}, likes={has_likes}, comments={has_comments}")
        
        missing_columns = []
        if not has_usage_time:
            missing_columns.append("daily_usage_time")
        if not has_posts:
            missing_columns.append("posts_per_day")
        if not has_likes:
            missing_columns.append("likes_received_per_day")
        if not has_comments:
            missing_columns.append("comments_received_per_day")
            
        if missing_columns:
            error_msg = f"Missing required columns in train_cleaned data for engagement chart: {', '.join(missing_columns)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Process the data in Python to create the time groups and engagement scores
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            # Check if all required values are present
            daily_usage = row.get("daily_usage_time")
            posts = row.get("posts_per_day")
            likes = row.get("likes_received_per_day")
            comments = row.get("comments_received_per_day")
            
            if any(x is None for x in [daily_usage, posts, likes, comments]):
                skipped_rows += 1
                logger.debug(f"Skipping row with missing data: daily_usage={daily_usage}, posts={posts}, likes={likes}, comments={comments}")
                continue
                
            # Convert values to proper types and handle potential errors
            try:
                daily_usage = float(daily_usage)
                posts = float(posts)
                likes = float(likes)
                comments = float(comments)
            except (ValueError, TypeError) as e:
                skipped_rows += 1
                logger.debug(f"Skipping row with invalid data type: {e}")
                continue
                
            processed_rows += 1
                
            # Determine time group based on daily usage
            if daily_usage < 60:
                time_group = 'Below 1h'
            elif 60 <= daily_usage <= 180:
                time_group = '1-3h'
            else:
                time_group = '3-5h'
                
            # Calculate engagement score - customizable formula
            engagement_score = (posts * 5) + (likes * 0.2) + (comments * 0.5)
                
            # Initialize time group if not exists
            if time_group not in time_groups:
                time_groups[time_group] = {
                    'total_score': 0,
                    'count': 0
                }
                
            time_groups[time_group]['total_score'] += engagement_score
            time_groups[time_group]['count'] += 1
        
        logger.info(f"Processed {processed_rows} rows, skipped {skipped_rows} rows for engagement")
        
        if processed_rows == 0:
            logger.warning("No valid rows found for engagement data processing")
            raise ValueError("No valid data rows for engagement visualization")
            
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

def process_anxiety_data(db_session) -> Dict[str, Any]:
    """
    Process screen time and anxiety levels for the fourth chart
    
    Returns:
        Dict with labels and datasets for anxiety chart
    """
    log_connection_details("process_anxiety_data", "started", {"session_id": id(db_session)})
    
    try:
        # Specify only the columns needed from SmmhCleaned model by their attribute names
        columns_needed = [
            "usage_time_group",        # ORM attribute name
            "q12_easily_distracted_scale", 
            "q13_bothered_by_worries_scale",
            "q14_difficulty_concentrating_scale",
            "q8_avg_sm_time"  # Fallback column in case usage_time_group is missing
        ]
        data = get_smmh_cleaned_data_orm(db_session, columns_to_load=columns_needed)

        if not data or len(data) == 0:
            logger.warning("No data returned from SmmhCleaned for anxiety data processing after requesting specific columns.")
            raise ValueError("No data found for anxiety visualization (columns might be missing or table empty).")

        logger.info(f"Sample row from smmh_cleaned (anxiety_data): {data[0] if data else 'N/A'}")
        logger.info(f"Column names received (anxiety_data): {list(data[0].keys()) if data else 'N/A'}")

        # Check if all required columns are available
        sample_row_keys = list(data[0].keys()) if data else []
        has_usage_time_group = "usage_time_group" in sample_row_keys
        has_distracted_scale = "q12_easily_distracted_scale" in sample_row_keys
        has_worries_scale = "q13_bothered_by_worries_scale" in sample_row_keys
        has_concentration_scale = "q14_difficulty_concentrating_scale" in sample_row_keys
        has_avg_sm_time = "q8_avg_sm_time" in sample_row_keys
        
        logger.info(f"Column availability: usage_time_group={has_usage_time_group}, distracted={has_distracted_scale}, " +
                   f"worries={has_worries_scale}, concentration={has_concentration_scale}, avg_sm_time={has_avg_sm_time}")
        
        missing_columns = []
        if not has_distracted_scale:
            missing_columns.append("q12_easily_distracted_scale")
        if not has_worries_scale:
            missing_columns.append("q13_bothered_by_worries_scale")
        if not has_concentration_scale:
            missing_columns.append("q14_difficulty_concentrating_scale")
            
        if missing_columns:
            error_msg = f"Missing required columns in smmh_cleaned data for anxiety chart: {', '.join(missing_columns)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        # If usage_time_group is missing but we have avg_sm_time, create a mapping
        if not has_usage_time_group and has_avg_sm_time:
            logger.warning("Missing usage_time_group column, will create from q8_avg_sm_time")
            
            # Categorize time from text responses like "1-2 hours", "Less than 1 hour", etc.
            time_mappings = {
                "less than 1 hour": "<1h",
                "1-2 hours": "1-2h",
                "2-3 hours": "2-3h",
                "3-4 hours": "3-4h",
                "4-5 hours": "4-5h",
                "more than 5 hours": ">5h"
            }
            
            # Add usage_time_group to each row
            for row in data:
                avg_time = str(row.get("q8_avg_sm_time", "")).lower().strip()
                row["usage_time_group"] = time_mappings.get(avg_time, "unknown")
            
            logger.info(f"Created usage_time_group from q8_avg_sm_time for anxiety chart. Sample: {data[0]['usage_time_group'] if data else 'N/A'}")
        
        # Process the data in Python to calculate anxiety levels
        time_groups = {}
        processed_rows = 0
        skipped_rows = 0
        
        for row in data:
            usage_time_group = row.get("usage_time_group")
            distraction_score = row.get("q12_easily_distracted_scale")
            worry_score = row.get("q13_bothered_by_worries_scale")
            concentration_score = row.get("q14_difficulty_concentrating_scale")
            
            if usage_time_group is None or distraction_score is None or worry_score is None or concentration_score is None:
                skipped_rows += 1
                logger.debug(f"Skipping row with missing data: usage_time_group={usage_time_group}")
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
                logger.debug(f"Skipping row with invalid anxiety scores")
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
        
        # Use the helper function to generate standardized chart response
        dataset = {
            "label": "Average Anxiety",
            "data": anxiety_data,
            "borderColor": "#66bb6a",
            "backgroundColor": "#66bb6a",
            "fill": False,
            "tension": 0.3
        }
        
        return create_chart_response(
            labels=labels,
            datasets=[dataset],
            chart_type='line',
            operation="process_anxiety_data"
        )
    except Exception as e:
        logger.error(f"Error processing anxiety data: {e}")
        log_connection_details("process_anxiety_data", "failed", {"error": str(e)})
        raise

def test_database_connection():
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
                
                # Check for required columns in each table
                if table == 'train_cleaned':
                    required_columns = ['daily_usage_time', 'dominant_emotion', 'posts_per_day', 
                                        'likes_received_per_day', 'comments_received_per_day']
                elif table == 'smmh_cleaned':
                    required_columns = ['Usage_Time_Group', 'q12_easily_distracted_scale',
                                        'q13_bothered_by_worries_scale', 'q14_difficulty_concentrating_scale',
                                        'q20_sleep_issues_scale', 'q8_avg_sm_time']
                else:
                    required_columns = []
                
                # Check columns
                if required_columns:
                    column_status = {}
                    for column in required_columns:
                        column_check_query = f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns
                            WHERE table_schema = 'public'
                            AND table_name = '{table}'
                            AND column_name = '{column}'
                        );
                        """
                        try:
                            column_result = execute_query(column_check_query, timeout=10)
                            column_status[column] = column_result[0]['exists'] if column_result else False
                        except Exception as e:
                            logger.error(f"Error checking column {column} in {table}: {e}")
                            column_status[column] = f"ERROR: {str(e)}"
                    
                    table_status[f"{table}_columns"] = column_status
                    
                    # Additional check: if the table has any records, get a sample row
                    if table_status.get(f"{table}_count", 0) > 0:
                        try:
                            sample_query = f"SELECT * FROM {table} LIMIT 1"
                            sample_result = execute_query(sample_query, timeout=10)
                            if sample_result and len(sample_result) > 0:
                                # Just log column names, not values, to avoid exposing sensitive data
                                table_status[f"{table}_available_columns"] = list(sample_result[0].keys())
                        except Exception as e:
                            logger.error(f"Error getting sample row from {table}: {e}")
                            table_status[f"{table}_sample_error"] = str(e)
                    
        # Additional diagnostics: check database backend and version
        try:
            version_query = "SELECT version();"
            version_result = execute_query(version_query, timeout=10)
            db_version = version_result[0]['version'] if version_result else "Unknown"
        except Exception as e:
            logger.error(f"Error getting database version: {e}")
            db_version = f"ERROR: {str(e)}"
        
        # Check if the Usage_Time_Group or daily_usage_time columns exist
        usage_time_recommendations = []
        if table_status.get('smmh_cleaned', False) and table_status.get('smmh_cleaned_columns', {}).get('Usage_Time_Group', False) is False:
            usage_time_recommendations.append("The 'Usage_Time_Group' column is missing from smmh_cleaned table. " +
                                             "Fallback to q8_avg_sm_time will be used if available.")
            
        if table_status.get('train_cleaned', False) and table_status.get('train_cleaned_columns', {}).get('daily_usage_time', False) is False:
            usage_time_recommendations.append("The 'daily_usage_time' column is missing from train_cleaned table. " +
                                             "This will affect all charts that use time-based data.")
        
        response = {
            "connection": "successful",
            "available_tables": [t['table_name'] for t in tables] if tables else [],
            "required_tables_status": table_status,
            "database_version": db_version,
            "recommendations": usage_time_recommendations if usage_time_recommendations else None
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

def get_train_cleaned_data(filters=None, group_by=None):
    """
    Use ORM to query the train_cleaned table with the given filters
    
    Args:
        filters: Dictionary of column:value pairs to filter on
        group_by: List of columns to group by
    
    Returns:
        List of dictionaries with the query results
    """
    if TrainCleaned is None:
        logger.error("TrainCleaned table not found in database schema")
        raise Exception("Train cleaned table not available")
    
    operation = "get_train_cleaned_data"
    log_connection_details(operation, "attempted")
    
    try:
        with time_limit(30):
            with engine.connect() as conn:
                # Use a direct SQL query as a fallback
                result = conn.execute(text("SELECT * FROM train_cleaned LIMIT 1000"))
                rows = result.fetchall()
                
                # Get column names from result
                columns = result.keys()
                
                # Convert to dictionaries
                data = []
                for row in rows:
                    # Convert any Row objects to plain dictionaries
                    if hasattr(row, '_asdict'):
                        data.append(row._asdict())
                    elif hasattr(row, 'items'):
                        data.append(dict(row))
                    else:
                        # Handle tuple-like row
                        data.append(dict(zip(columns, row)))
                
                log_connection_details(operation, "success", {"rows_returned": len(data)})
                return data
    except Exception as e:
        log_connection_details(operation, "failed", {"error": str(e)})
        logger.error(f"Error in get_train_cleaned_data: {e}")
        raise

def get_smmh_cleaned_data(filters=None, group_by=None):
    """
    Use ORM to query the smmh_cleaned table with the given filters
    
    Args:
        filters: Dictionary of column:value pairs to filter on
        group_by: List of columns to group by
    
    Returns:
        List of dictionaries with the query results
    """
    if SmmhCleaned is None:
        logger.error("SmmhCleaned table not found in database schema")
        raise Exception("SMMH cleaned table not available")
    
    operation = "get_smmh_cleaned_data"
    log_connection_details(operation, "attempted")
    
    try:
        with time_limit(30):
            with engine.connect() as conn:
                # Use a direct SQL query as a fallback
                result = conn.execute(text("SELECT * FROM smmh_cleaned LIMIT 1000"))
                rows = result.fetchall()
                
                # Get column names from result
                columns = result.keys()
                
                # Convert to dictionaries
                data = []
                for row in rows:
                    # Convert any Row objects to plain dictionaries
                    if hasattr(row, '_asdict'):
                        data.append(row._asdict())
                    elif hasattr(row, 'items'):
                        data.append(dict(row))
                    else:
                        # Handle tuple-like row
                        data.append(dict(zip(columns, row)))
                
                log_connection_details(operation, "success", {"rows_returned": len(data)})
                return data
    except Exception as e:
        log_connection_details(operation, "failed", {"error": str(e)})
        logger.error(f"Error in get_smmh_cleaned_data: {e}")
        raise 