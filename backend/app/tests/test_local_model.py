import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the parent directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def test_local_model():
    """Test the local model to analyze comments."""
    try:
        # Import the analyse_batch function from the cloned model
        from app.nlp.app import analyse_batch
        
        # Test comments
        test_comments = [
            "This video is amazing! I love it so much.",
            "This is the worst thing I've ever seen, absolutely terrible.",
            "Not bad but could be better.",
            "You are an idiot for making this content.",
            "Just a neutral comment about the weather."
        ]
        
        # Join comments with newlines as expected by the function
        comments_text = "\n".join(test_comments)
        
        logger.info("Analyzing test comments with the local model...")
        result = analyse_batch(comments_text)
        
        logger.info("Analysis completed successfully!")
        logger.info(f"Result: {result}")
        
        # Check if we have sentiment counts in the result
        if "sentiment_counts" in result:
            logger.info("Local model is working correctly!")
            return True
        else:
            logger.error("Result doesn't contain expected fields")
            return False
            
    except Exception as e:
        logger.error(f"Error testing local model: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_local_model()
    if success:
        print("\n✅ Local model test successful!")
    else:
        print("\n❌ Local model test failed!") 