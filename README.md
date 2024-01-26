# Course Recommendation System

## Overview
This repository contains the source code for a course recommendation system that utilizes data from CSV files sourced from Coursera, edX, Skillshare, and Udemy. The system employs a TF-IDF (Term Frequency-Inverse Document Frequency) model for Natural Language Processing (NLP) to analyze course content and predict recommendations based on similarity.

## How it Works
- The system utilizes CSV files from Coursera, edX, Skillshare, and Udemy to gather course data.
- TF-IDF (Term Frequency-Inverse Document Frequency) model is employed for NLP to analyze course content.
- TF-IDF evaluates the importance of words in documents within a corpus. In this context, it helps understand and compare the content of courses across different platforms.
- Flask, a Python web framework, facilitates the integration of the system.
- The user interface is developed using HTML, CSS, and JavaScript.
- Users interact with the system through a frontend interface where they can enter preferences or queries.
- The backend processes this information, computes similarities using TF-IDF, and provides personalized course recommendations from the diverse dataset.

## Usage
1. Clone the repository: `git clone https://github.com/your-username/repo-name.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Flask application: `python app.py`
4. Access the application through a web browser.

## Contributors
- Siddhanth Sridhar
- JShreya Chaurasia
- -Yahwanth Reddy


Feel free to contribute and improve the system!

For any questions or issues, please contact [siddhanth2305@gmail.com](mailto:siddhanth2305@gmail.com).
