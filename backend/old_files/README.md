# Old Files Directory

This directory contains files that were part of the original backend structure but have been identified as redundant, deprecated, or no longer in use.

## Redundant Files

The following files in the `redundant` subdirectory have been identified as redundant or no longer in use:

- `database.py` - Redundant with `app/database.py` which is the primary database connection file
- `serve_memes.py` - Standalone meme server that has been superseded by the integrated FastAPI implementation
- `test_db_connection.py` - Utility script for testing database connections, no longer needed in production
- `upload_data.py` - One-time script for data upload, no longer used in the main application flow
- `run.py` - Simplified version of `run_server.py` which is the main entry point
- `run_meme_server.py` - Standalone meme server that has been integrated into the main app

## Moved Directories

- `routes/` - Contains Flask-based routes that have been migrated to FastAPI in `app/routes` and `app/routers`

## Removed Files

- `meme_game.py` - Broken symlink (pointing to non-existent `kaggle_memes/meme_dataset_manager.py`)

These files are kept for reference purposes but are not part of the active application flow. 