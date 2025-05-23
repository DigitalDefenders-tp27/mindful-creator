from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import logging
import time
import sys
import os

from . import data_processors
from .database import ALLOW_DB_FAILURE, get_db, get_db_session
from sqlalchemy.orm import Session

# Setup logging
# logging.basicConfig(level=logging.INFO) # Basic config might be handled in main.py
logger = logging.getLogger("mindful-creator.visualisation.routes") # Changed logger name

router = APIRouter(
    prefix="/api/visualisation",
    tags=["visualisation"],
    responses={404: {"description": "Not found"}},
)

# Helper to create a safe error string
def _safe_error_str(e: Exception) -> str:
    try:
        return str(e)
    except Exception as ie:
        logger.error(f"Failed to convert exception to string: {type(e)} caused {type(ie)}", exc_info=True)
        return "An undescribable error occurred in the data processing module."

# Lightweight health check endpoint for the visualization module
@router.get("/health")
async def visualisation_health() -> Dict[str, Any]:
    """
    A lightweight health check endpoint for the visualization module
    This endpoint deliberately avoids any database operations
    """
    logger.info("VISUALISATION HEALTH CHECK ENDPOINT ACCESSED")
    return {
        "status": "ok",
        "module": "visualisation",
        "timestamp": time.time()
    }

@router.get("/screen-time-emotions")
async def get_screen_time_emotions(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Get data for screen time vs emotions chart
    """
    logger.info("API request: screen-time-emotions")
    try:
        # Using get_db_session - this now yields a proper session directly
        data = data_processors.process_screen_time_emotions(db)
            
        logger.info("Successfully processed screen time emotions data")
        return JSONResponse(content=data)
    except Exception as e:
        error_message = _safe_error_str(e)
        logger.error(f"Error processing screen time emotions: {error_message}", exc_info=True)
        if ALLOW_DB_FAILURE:
            return JSONResponse(
                content={
                    "error": f"Database error: {error_message}",
                    "message": "Unable to load visualization data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve screen time emotions data: {error_message}"
            )

@router.get("/sleep-quality")
async def get_sleep_quality(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Get data for digital habits vs sleep quality chart
    """
    logger.info("API request: sleep-quality")
    try:
        # Using get_db_session
        data = data_processors.process_sleep_data(db)
            
        logger.info("Successfully processed sleep data")
        return JSONResponse(content=data)
    except Exception as e:
        error_message = _safe_error_str(e)
        logger.error(f"Error processing sleep data: {error_message}", exc_info=True)
        if ALLOW_DB_FAILURE:
            return JSONResponse(
                content={
                    "error": f"Database error: {error_message}",
                    "message": "Unable to load sleep quality data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve sleep quality data: {error_message}"
            )

@router.get("/engagement")
async def get_engagement(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Get data for engagement metrics chart
    """
    logger.info("API request: engagement")
    try:
        # Using get_db_session
        data = data_processors.process_engagement_data(db)
            
        logger.info("Successfully processed engagement data")
        return JSONResponse(content=data)
    except Exception as e:
        error_message = _safe_error_str(e)
        logger.error(f"Error processing engagement data: {error_message}", exc_info=True)
        if ALLOW_DB_FAILURE:
            return JSONResponse(
                content={
                    "error": f"Database error: {error_message}",
                    "message": "Unable to load engagement data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve engagement data: {error_message}"
            )

@router.get("/anxiety")
async def get_anxiety(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Get data for screen time vs anxiety chart
    """
    logger.info("API request: anxiety")
    try:
        # Using get_db_session
        data = data_processors.process_anxiety_data(db)
            
        logger.info("Successfully processed anxiety data")
        return JSONResponse(content=data)
    except Exception as e:
        error_message = _safe_error_str(e)
        logger.error(f"Error processing anxiety data: {error_message}", exc_info=True)
        if ALLOW_DB_FAILURE:
            return JSONResponse(
                content={
                    "error": f"Database error: {error_message}",
                    "message": "Unable to load anxiety data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve anxiety data: {error_message}"
            )

@router.get("/all-chart-data")
async def get_all_chart_data(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Get data for all charts in a single request
    """
    logger.info("API request: all-chart-data")
    
    results = {}
    errors = []
    
    # Using get_db_session directly provides a session, no need for context manager handling
    # Try to get each dataset separately, so one failure doesn't break all
    try:
        results["screenTimeEmotions"] = data_processors.process_screen_time_emotions(db)
    except Exception as e:
        logger.error(f"Error getting screen time emotions data: {e}")
        errors.append(f"Screen time emotions: {str(e)}")
        results["screenTimeEmotions"] = {"error": str(e)}
    
    try:
        results["sleepQuality"] = data_processors.process_sleep_data(db)
    except Exception as e:
        logger.error(f"Error getting sleep data: {e}")
        errors.append(f"Sleep quality: {str(e)}")
        results["sleepQuality"] = {"error": str(e)}
    
    try:
        results["engagement"] = data_processors.process_engagement_data(db)
    except Exception as e:
        logger.error(f"Error getting engagement data: {e}")
        errors.append(f"Engagement: {str(e)}")
        results["engagement"] = {"error": str(e)}
    
    try:
        results["anxiety"] = data_processors.process_anxiety_data(db)
    except Exception as e:
        logger.error(f"Error getting anxiety data: {e}")
        errors.append(f"Anxiety: {str(e)}")
        results["anxiety"] = {"error": str(e)}
    
    # If we have any data, return it along with errors
    if errors:
        results["_errors"] = errors
        
    # If all failed and we don't allow DB failures, raise exception
    if len(errors) == 4 and not ALLOW_DB_FAILURE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve any chart data: {'; '.join(errors)}"
        )
    
    return results

@router.get("/test")
async def test_endpoint() -> Dict[str, Any]:
    """
    Test endpoint to verify router is accessible
    """
    logger.info("API request: test endpoint")
    return {"status": "ok", "message": "Visualisation API is working correctly"}

@router.get("/db-test")
async def test_database(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Test endpoint to verify database connectivity
    """
    logger.info("API request: database test")
    return data_processors.test_database_connection()

@router.get("/connection-test")
async def connection_test(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Comprehensive connection test endpoint that logs detailed information
    """
    from .database import log_connection_details
    
    logger.info("API request: connection-test")
    log_connection_details("api_connection_test", "running")
    
    try:
        # First test the database connection
        db_status = data_processors.test_database_connection()
        
        # Check if we can query a specific table
        table_test_results = {}
        
        # Test each table needed for visualization
        for table in ["train_cleaned", "smmh_cleaned"]:
            try:
                # Try a very simple query on each table
                from .database import execute_query
                logger.info(f"Testing simple query on '{table}'")
                
                query = f"""
                SELECT COUNT(*) as record_count FROM {table} LIMIT 1;
                """
                
                results = execute_query(query)
                record_count = results[0]["record_count"] if results else 0
                
                table_test_results[table] = {
                    "status": "success",
                    "record_count": record_count
                }
            except Exception as e:
                logger.error(f"Error testing table {table}: {e}")
                table_test_results[table] = {
                    "status": "error",
                    "message": str(e)
                }
        
        # Log the overall test results
        log_connection_details("api_connection_test", "completed", {
            "db_connection": db_status["connection"],
            "table_tests": table_test_results
        })
        
        # Return comprehensive result
        return {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "db_connection": db_status,
            "table_tests": table_test_results,
            "environment": {
                "python_version": sys.version,
                "platform": sys.platform,
                "environment": os.environ.get("ENVIRONMENT", "unknown")
            }
        }
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        log_connection_details("api_connection_test", "failed", str(e))
        return {
            "status": "error",
            "message": str(e),
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }

@router.get("/debug-data-schema")
async def debug_data_schema(db: Session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Debug endpoint to examine data schemas for all charts
    """
    logger.info("API request: debug-data-schema")
    logger.info(f"debug-data-schema: Received db_session of type: {type(db)}")

    try:
        train_data_sample = None
        train_columns = []
        smmh_data_sample = None
        smmh_columns = []
        
        # Define all ORM attribute names for fetching full sample for debug
        # These should match the attribute names in your ORM models (TrainCleaned, SmmhCleaned)
        train_cleaned_all_orm_attrs = [
            "user_id", "age", "gender", "platform", "daily_usage_time", "posts_per_day",
            "likes_received_per_day", "comments_received_per_day", "messages_sent_per_day", "dominant_emotion"
        ]
        
        # Updated list of all SmmhCleaned ORM attribute names based on the new schema
        # ISSUE: We only requested one column (timestamp_val) which isn't enough for the charts
        smmh_cleaned_all_orm_attrs = [
            "timestamp_val", 
            "q1_age", "q2_gender", "q3_relationship_status", "q4_occupation_status",
            "q5_org_affiliation", "q6_use_social_media", "q7_platforms", "q8_avg_sm_time",
            "q9_unintentional_use", "q10_distracted_by_sm", "q11_restless_no_sm",
            "q12_easily_distracted_scale", "q13_bothered_by_worries_scale", 
            "q14_difficulty_concentrating_scale", "q15_compare_to_others_scale", 
            "q16_feel_about_comparisons", "q17_seek_validation_scale",
            "q18_feel_depressed_scale", "q19_interest_fluctuation_scale", 
            "q20_sleep_issues_scale", "usage_time_group"
        ]
        
        try:
            train_data_list = data_processors.get_train_cleaned_data_orm(db, limit=1, columns_to_load=train_cleaned_all_orm_attrs)
            logger.info(f"debug-data-schema: train_data_list from ORM: {train_data_list}")
            if train_data_list and len(train_data_list) > 0:
                train_data_sample = train_data_list[0]
                logger.info(f"debug-data-schema: train_data_sample type: {type(train_data_sample)}, value: {train_data_sample}") # DETAILED LOGGING
                if isinstance(train_data_sample, dict): # Ensure it's a dict before getting keys
                    train_columns = list(train_data_sample.keys())
                    logger.info(f"Successfully fetched sample and columns for train_cleaned using ORM. Columns: {train_columns}")
                else:
                    logger.warning(f"debug-data-schema: train_data_sample is not a dict. Type: {type(train_data_sample)}")
            else:
                logger.warning("get_train_cleaned_data_orm returned no data or empty list for debug-data-schema.")
        except Exception as e:
            logger.error(f"Error getting train_cleaned sample using ORM: {e}", exc_info=True)
            
        try:
            # FIX: Request all required columns from smmh_cleaned table instead of just timestamp_val
            # These columns are needed for the sleep quality and anxiety charts
            smmh_required_columns = [
                "timestamp_val", 
                "usage_time_group",
                "q12_easily_distracted_scale", 
                "q13_bothered_by_worries_scale",
                "q14_difficulty_concentrating_scale", 
                "q20_sleep_issues_scale"
            ]
            
            logger.info(f"debug-data-schema: Requesting columns for SMMH: {smmh_required_columns}")

            smmh_data_list = data_processors.get_smmh_cleaned_data_orm(db, limit=1, columns_to_load=smmh_required_columns)
            logger.info(f"debug-data-schema: smmh_data_list from ORM: {smmh_data_list}")
            if smmh_data_list and len(smmh_data_list) > 0:
                smmh_data_sample = smmh_data_list[0]
                logger.info(f"debug-data-schema: smmh_data_sample type: {type(smmh_data_sample)}, value: {smmh_data_sample}") # DETAILED LOGGING
                if isinstance(smmh_data_sample, dict): # Ensure it's a dict
                    smmh_columns = list(smmh_data_sample.keys())
                    logger.info(f"Successfully fetched sample and columns for smmh_cleaned using ORM. Columns: {smmh_columns}")
                else:
                    logger.warning(f"debug-data-schema: smmh_data_sample is not a dict. Type: {type(smmh_data_sample)}")
            else:
                logger.warning("get_smmh_cleaned_data_orm returned no data or empty list for debug-data-schema.")
        except Exception as e:
            logger.error(f"Error getting smmh_cleaned sample using ORM: {e}", exc_info=True)
            
        # Try to generate sample chart data for each chart
        chart_shapes = {}
        
        try:
            screen_time_emotions_data = data_processors.process_screen_time_emotions(db)
            chart_shapes["screen_time_emotions"] = {
                "labels_count": len(screen_time_emotions_data.get("labels", [])),
                "datasets_count": len(screen_time_emotions_data.get("datasets", [])),
                "has_valid_structure": "labels" in screen_time_emotions_data and "datasets" in screen_time_emotions_data
            }
        except Exception as e:
            chart_shapes["screen_time_emotions"] = {"error": str(e)}
            
        try:
            sleep_data = data_processors.process_sleep_data(db)
            chart_shapes["sleep_quality"] = {
                "labels_count": len(sleep_data.get("labels", [])),
                "datasets_count": len(sleep_data.get("datasets", [])),
                "has_valid_structure": "labels" in sleep_data and "datasets" in sleep_data
            }
        except Exception as e:
            chart_shapes["sleep_quality"] = {"error": str(e)}
            
        try:
            engagement_data = data_processors.process_engagement_data(db)
            chart_shapes["engagement"] = {
                "labels_count": len(engagement_data.get("labels", [])),
                "datasets_count": len(engagement_data.get("datasets", [])),
                "has_valid_structure": "labels" in engagement_data and "datasets" in engagement_data
            }
        except Exception as e:
            chart_shapes["engagement"] = {"error": str(e)}
            
        try:
            anxiety_data = data_processors.process_anxiety_data(db)
            chart_shapes["anxiety"] = {
                "labels_count": len(anxiety_data.get("labels", [])),
                "datasets_count": len(anxiety_data.get("datasets", [])),
                "has_valid_structure": "labels" in anxiety_data and "datasets" in anxiety_data
            }
        except Exception as e:
            chart_shapes["anxiety"] = {"error": str(e)}
        
        return {
            "train_cleaned_columns": train_columns,
            "smmh_cleaned_columns": smmh_columns,
            "chart_data_shapes": chart_shapes,
            "train_cleaned_sample": train_data_sample,
            "smmh_cleaned_sample": smmh_data_sample
        }
    except Exception as e:
        logger.error(f"Error in debug_data_schema: {e}", exc_info=True)
        return {
            "error": str(e),
            "message": "An error occurred while examining data schema"
        } 