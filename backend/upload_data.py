# upload_data.py
import pandas as pd
import psycopg2
from database import get_connection

def upload_train_cleaned():
    conn = get_connection()
    cur = conn.cursor()
    df = pd.read_csv('datasets/train_cleaned.csv')

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO train_cleaned (User_ID, Age, Gender, Platform, Daily_Usage_Time_minutes,
                                       Posts_Per_Day, Likes_Received_Per_Day, Comments_Received_Per_Day,
                                       Messages_Sent_Per_Day, Dominant_Emotion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Uploaded train_cleaned successfully.")

def upload_smmh_cleaned():
    conn = get_connection()
    cur = conn.cursor()
    df = pd.read_csv('datasets/smmh_cleaned.csv')

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO smmh_cleaned (
                Timestamp, Age, Gender, Relationship_Status, Occupation_Status,
                Organization_Affiliation, Uses_Social_Media, Common_Platforms, Average_Time_Spent,
                Purposeful_Usage_Score, Distraction_Score, Restlessness_Score, Distractibility_Score,
                Worry_Score, Concentration_Difficulty_Score, Comparison_Frequency_Score,
                Comparison_Feelings_Score, Validation_Seeking_Score, Depression_Score,
                Interest_Fluctuation_Score, Sleep_Issue_Score
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            row['Timestamp'], row['1. What is your age?'], row['2. Gender'], row['3. Relationship Status'],
            row['4. Occupation Status'], row['5. What type of organizations are you affiliated with?'],
            row['6. Do you use social media?'], row['7. What social media platforms do you commonly use?'],
            row['8. What is the average time you spend on social media every day?'],
            row['9. How often do you find yourself using Social media without a specific purpose?'],
            row['10. How often do you get distracted by Social media when you are busy doing something?'],
            row["11. Do you feel restless if you haven't used Social media in a while?"],
            row['12. On a scale of 1 to 5, how easily distracted are you?'],
            row['13. On a scale of 1 to 5, how much are you bothered by worries?'],
            row['14. Do you find it difficult to concentrate on things?'],
            row['15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?'],
            row['16. Following the previous question, how do you feel about these comparisons, generally speaking?'],
            row['17. How often do you look to seek validation from features of social media?'],
            row['18. How often do you feel depressed or down?'],
            row['19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?'],
            row['20. On a scale of 1 to 5, how often do you face issues regarding sleep?']
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Uploaded smmh_cleaned successfully.")

# NEW upload: Screen Time Data
def upload_screen_time_data():
    conn = get_connection()
    cur = conn.cursor()
    df = pd.read_csv('datasets/screen_time_cleaned.csv')

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO screen_time_data (
                date, weekday, total_screen_time, social_networking,
                reading_reference, other, productivity, health_fitness,
                entertainment, creativity, yoga
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Date'], row['Week Day'], row['Total Screen Time '], row['Social Networking'],
            row['Reading and Reference'], row['Other'], row['Productivity'],
            row['Health and Fitness'], row['Entertainment'], row['Creativity'], row['Yoga']
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Uploaded screen_time_cleaned successfully.")


# NEW upload: Music Mental Health Data
def upload_music_mental_health_data():
    conn = get_connection()
    cur = conn.cursor()
    df = pd.read_csv('datasets/music_mental_health_cleaned.csv')

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO music_mental_health_data (
                age, primary_streaming_service, hours_per_day, while_working,
                instrumentalist, composer, fav_genre, exploratory,
                foreign_languages, bpm, anxiety, depression, insomnia, ocd, music_effects
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Age'], row['Primary streaming service'], row['Hours per day'], row['While working'],
            row['Instrumentalist'], row['Composer'], row['Fav genre'], row['Exploratory'],
            row['Foreign languages'], row['BPM'], row['Anxiety'], row['Depression'],
            row['Insomnia'], row['OCD'], row['Music effects']
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Uploaded music_mental_health_cleaned successfully.")


if __name__ == "__main__":
    upload_train_cleaned()
    upload_smmh_cleaned()
    upload_screen_time_data()
    upload_music_mental_health_data()