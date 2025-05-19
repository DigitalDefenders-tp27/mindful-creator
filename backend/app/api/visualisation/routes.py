from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import logging
import time
import sys
import os

from . import data_processors
from .database import ALLOW_DB_FAILURE

# Setup logging
logger = logging.getLogger("visualisation.routes")

router = APIRouter(
    prefix="/api/visualisation",
    tags=["visualisation"],
    responses={404: {"description": "Not found"}},
)

@router.get("/screen-time-emotions")
async def get_screen_time_emotions() -> Dict[str, Any]:
    """
    Get data for screen time vs emotions chart
    """
    logger.info("API request: screen-time-emotions")
    try:
        data = data_processors.process_screen_time_emotions()
        logger.info("Successfully processed screen time emotions data")
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error processing screen time emotions: {e}")
        if ALLOW_DB_FAILURE:
            # Return an informative error response but still return 200 status
            return JSONResponse(
                content={
                    "error": f"Database error: {str(e)}",
                    "message": "Unable to load visualization data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve screen time emotions data: {str(e)}"
            )

@router.get("/sleep-quality")
async def get_sleep_quality() -> Dict[str, Any]:
    """
    Get data for digital habits vs sleep quality chart
    """
    logger.info("API request: sleep-quality")
    try:
        data = data_processors.process_sleep_data()
        logger.info("Successfully processed sleep data")
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error processing sleep data: {e}")
        if ALLOW_DB_FAILURE:
            # Return an informative error response but still return 200 status
            return JSONResponse(
                content={
                    "error": f"Database error: {str(e)}",
                    "message": "Unable to load sleep quality data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve sleep quality data: {str(e)}"
            )

@router.get("/engagement")
async def get_engagement() -> Dict[str, Any]:
    """
    Get data for engagement metrics chart
    """
    logger.info("API request: engagement")
    try:
        data = data_processors.process_engagement_data()
        logger.info("Successfully processed engagement data")
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error processing engagement data: {e}")
        if ALLOW_DB_FAILURE:
            # Return an informative error response but still return 200 status
            return JSONResponse(
                content={
                    "error": f"Database error: {str(e)}",
                    "message": "Unable to load engagement data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve engagement data: {str(e)}"
            )

@router.get("/anxiety")
async def get_anxiety() -> Dict[str, Any]:
    """
    Get data for screen time vs anxiety chart
    """
    logger.info("API request: anxiety")
    try:
        data = data_processors.process_anxiety_data()
        logger.info("Successfully processed anxiety data")
        return JSONResponse(content=data)
    except Exception as e:
        logger.error(f"Error processing anxiety data: {e}")
        if ALLOW_DB_FAILURE:
            # Return an informative error response but still return 200 status
            return JSONResponse(
                content={
                    "error": f"Database error: {str(e)}",
                    "message": "Unable to load anxiety data due to database connection issues."
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve anxiety data: {str(e)}"
            )

@router.get("/all-chart-data")
async def get_all_chart_data() -> Dict[str, Any]:
    """
    Get data for all charts in a single request
    """
    logger.info("API request: all-chart-data")
    
    results = {}
    errors = []
    
    # Try to get each dataset separately, so one failure doesn't break all
    try:
        results["screenTimeEmotions"] = data_processors.process_screen_time_emotions()
    except Exception as e:
        logger.error(f"Error getting screen time emotions data: {e}")
        errors.append(f"Screen time emotions: {str(e)}")
        results["screenTimeEmotions"] = {"error": str(e)}
    
    try:
        results["sleepQuality"] = data_processors.process_sleep_data()
    except Exception as e:
        logger.error(f"Error getting sleep data: {e}")
        errors.append(f"Sleep quality: {str(e)}")
        results["sleepQuality"] = {"error": str(e)}
    
    try:
        results["engagement"] = data_processors.process_engagement_data()
    except Exception as e:
        logger.error(f"Error getting engagement data: {e}")
        errors.append(f"Engagement: {str(e)}")
        results["engagement"] = {"error": str(e)}
    
    try:
        results["anxiety"] = data_processors.process_anxiety_data()
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
async def test_database() -> Dict[str, Any]:
    """
    Test endpoint to verify database connectivity
    """
    logger.info("API request: database test")
    return data_processors.test_database_connection()

@router.get("/connection-test")
async def connection_test() -> Dict[str, Any]:
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