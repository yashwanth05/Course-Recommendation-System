from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import re
from flask_cors import CORS 
from googlesearch import search
import random
app = Flask(__name__)
CORS(app)  


def extract_duration(duration_str):
    match = re.search(r'\d+', str(duration_str))
    return int(match.group()) if match else 0

# Function to get Udemy course link from the title (constructed manually)
def get_udemy_link(title):
    title_for_url = title.replace(' ', '-')
    return f'https://www.udemy.com/course/{title_for_url}/'

def convert_duration(duration_str):
    parts = duration_str.split('h')
    if len(parts) == 1:
        return int(parts[0].strip('m'))
    else:
        return int(parts[0].strip()) * 60 + int(parts[1].strip('m'))

def get_course_link(course_title):
    query = f"{course_title} Skillshare course site:skillshare.com"
    for j in search(query, num=1, stop=1, pause=2):
        return j

def get_coursera_link(course_name):
    query = f"{course_name} site:coursera.org"
    try:
        for url in search(query, stop=1, pause=2):
            if 'coursera.org' in url:
                return url
    except Exception as e:
        print(f"Error: {e}")
    return None

# Function to get course recommendations with links
def get_recommendations_udemy(prompt):
    df = pd.read_csv(r"CSV\Udemy.csv")


    df['description'] = df['description'].fillna('')  # Handle missing descriptions

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the description data
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'])

    # Calculate the cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Transform the prompt using the TF-IDF vectorizer
    prompt_vector = tfidf_vectorizer.transform([prompt])

    # Calculate the cosine similarity between the prompt and all courses
    cosine_similarities = linear_kernel(prompt_vector, tfidf_matrix).flatten()

    # Get indices of courses sorted by similarity
    course_indices = cosine_similarities.argsort()[::-1]

    # Return top 5 course recommendations with details and links
    recommended_courses = df.iloc[course_indices[:5]][['title', 'instructor', 'rating', 'duration', 'level']]

    # Extract numeric values from duration for correct sorting
    recommended_courses['duration_numeric'] = recommended_courses['duration'].apply(extract_duration)

    # Sort recommended courses by duration in ascending order
    recommended_courses = recommended_courses.sort_values(by='rating', ascending=False)

    return recommended_courses

def get_recommendations_Coursera(user_input):
    df = pd.read_csv(r"CSV\Coursera.csv")

    df['skills'] = df['skills'].fillna('')  # Handle missing skills information

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the skills data
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['skills'])

    # Calculate the cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Transform the user input using the TF-IDF vectorizer
    user_input_vector = tfidf_vectorizer.transform([user_input])

    # Calculate the cosine similarity between the user input and all courses
    cosine_similarities = linear_kernel(user_input_vector, tfidf_matrix).flatten()

    # Get indices of courses sorted by similarity
    course_indices = cosine_similarities.argsort()[::-1]

    # Return top 5 course recommendations with specific columns
    recommended_courses = df.iloc[course_indices[:5]][['partner', 'course', 'skills', 'rating', 'reviewcount', 'level', 'certificatetype', 'duration', 'crediteligibility']]
    recommended_courses = recommended_courses.sort_values(by='rating', ascending=False)
    # recommended_courses['link'] = recommended_courses['course'].apply(get_coursera_link)
    # Convert the recommendations to a dictionary for easy JSON serialization
    recommendations_dict = recommended_courses.to_dict(orient='records')

    return recommendations_dict

def get_recommendations_skillshare(user_input):
    df = pd.read_csv(r"CSV\skillshare.csv")

# Preprocess the data
    df['title'] = df['title'].fillna('') 
    df['duration_minutes'] = df['duration'].apply(convert_duration)

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the skills data
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'])

    # Calculate the cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Transform the user input using the TF-IDF vectorizer
    user_input_vector = tfidf_vectorizer.transform([user_input])

    # Calculate the cosine similarity between the user input and all courses
    cosine_similarities = linear_kernel(user_input_vector, tfidf_matrix).flatten()

    # Get indices of courses sorted by similarity
    course_indices = cosine_similarities.argsort()[::-1]

    # Return top 5 course recommendations with specific columns
    recommended_courses = df.iloc[course_indices[:5]][['title', 'duration', 'instructor', 'students']]

    # Convert duration to total minutes for sorting
    recommended_courses['duration_minutes'] = recommended_courses['duration'].apply(convert_duration)

    # Sort recommended courses by duration in descending order
    recommended_courses = recommended_courses.sort_values(by='duration_minutes', ascending=True)

    # Add course links
    # recommended_courses['link'] = recommended_courses['title'].apply(get_course_link)

    return recommended_courses.to_dict(orient='records')

def get_recommendations_edx(user_input):
    # Load the dataset
    df = pd.read_csv(r"CSV\edx.csv")

# Preprocess the data
    df['title'] = df['title'].fillna('')  # Handle missing title information

# Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the title data
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'])

# Calculate the cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Transform the user input using the TF-IDF vectorizer
    user_input_vector = tfidf_vectorizer.transform([user_input])

    # Calculate the cosine similarity between the user input and all courses
    cosine_similarities = linear_kernel(user_input_vector, tfidf_matrix).flatten()

    # Get indices of courses sorted by similarity
    course_indices = cosine_similarities.argsort()[::-1]

    # Return top 5 course recommendations with specific columns
    recommended_courses = df.iloc[course_indices[:5]][['title', 'link', 'institution', 'subject', 'level']]
    recommended_courses = recommended_courses.sort_values(by='level', ascending=False)

    return recommended_courses.to_dict(orient='records')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')


@app.route('/get_recommendations', methods=['POST'])
def get_recommendations_route():
    data = request.get_json()
    dic = []
    if 'skills' in data:
        user_prompt = data['skills']
        selected_platforms = data.get('platforms', [])
        print("User Prompt:", user_prompt)
        print("Selected Platforms:", selected_platforms)
    # recommendations = get_recommendations_udemy(user_prompt)
    # recommendations_list = recommendations.to_dict(orient='records')
    for i in selected_platforms:
        if i == "udemy":
            recommendations = get_recommendations_udemy(user_prompt)
            recommendations_list = recommendations.to_dict(orient='records')
            print(recommendations_list)
            dic.extend(recommendations_list)
        if i=="coursera":
            recommendations = get_recommendations_Coursera(user_prompt)
            print("hi")
            # recommendations_list = recommendations.to_dict(orient='records')
            print(recommendations)
            dic.extend(recommendations)
        if i == "skillshare":
            recommendations = get_recommendations_skillshare(user_prompt)
            print("hi1")
            # recommendations_list = recommendations.to_dict(orient='records')
            print(recommendations)
            dic.extend(recommendations)
        if i=="edx":
            recommendations = get_recommendations_edx(user_prompt)
            print("hi1")
            # recommendations_list = recommendations.to_dict(orient='records')
            print(recommendations)
            dic.extend(recommendations)
    print(dic)
    print(len(dic))
    random_sample = random.sample(dic, 5)
    return jsonify(recommendations= random_sample)



if __name__ == '__main__':
    app.run(debug=True)
