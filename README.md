# Student Performance & Weakness Analyzer

A complete academic MVP built with **Python + Streamlit + MongoDB Atlas + PyMongo + Pandas + Plotly**.

The app focuses on student quiz performance analytics. It stores quiz attempts in MongoDB, analyzes accuracy by topic, detects weak and repeatedly incorrect areas, and recommends what the student should study next using a simple rule-based Python system.

No paid APIs, no external AI API, no HTML/CSS/JavaScript required.

---

## Core MVP Flow

```text
Student Profile → Select Quiz → Answer Questions → Submit Quiz → Calculate Score
→ Save Results to MongoDB → Analyze Performance → Detect Weak Topics
→ Detect Repeated Mistakes → Recommend What to Study Next
```

---

## Features

### Student Profiles
- Create a student profile
- Select an existing profile
- View performance only for the selected student
- Simple profile system with no password complexity

### Quiz System
- Select subject, topic, and number of questions
- Answer multiple-choice questions
- Submit quiz and instantly calculate score
- Show correct and incorrect answers
- Store quiz attempt and individual answer records in MongoDB

### MongoDB Collections Used
- `students`
- `subjects`
- `topics`
- `questions`
- `quiz_attempts`
- `answers`

### Performance Analytics
For every attempted topic, the app calculates:
- Total questions attempted
- Correct answers
- Incorrect answers
- Accuracy percentage
- Recent mistakes
- Performance classification

### Required Classification Thresholds
| Accuracy | Classification |
|---:|---|
| Below 65% | 🔴 Weak |
| 65% to 84% | 🟡 Needs Practice |
| 85% or above | 🟢 Strong |

These classifications are calculated automatically from stored MongoDB quiz data.

### Repeated Mistake Detection
The app reviews recent attempts for each topic and identifies repeated poor performance. It explains the issue safely, for example:

> You have repeatedly struggled with Probability across your recent attempts.

It does not claim a specific conceptual misunderstanding unless the data supports it.

### Rule-Based Recommendations
The recommendation engine uses:
- Topic accuracy
- Incorrect answer count
- Recent mistakes
- Recent performance
- Difficulty of missed questions

No AI API is used.

### Progress Charts
Built with Plotly from actual MongoDB data:
- Subject performance
- Topic performance
- Performance over time
- Weak / Practice / Strong distribution

### Management Page
Simple CRUD-style tools for:
- Adding and editing students
- Adding and editing topics
- Adding and editing questions
- Seeding sample data

---

## Sample Educational Data

The project includes 10 topics and 50 sample questions.

### Mathematics
- Algebra
- Trigonometry
- Probability
- Geometry

### Physics
- Motion
- Force and Laws of Motion
- Electricity

### Chemistry
- Atomic Structure
- Chemical Bonding
- Acids and Bases

Each topic has 5 multiple-choice questions with four options, one correct answer, subject, topic, and Easy / Medium / Hard difficulty.

---

## Project Structure

```text
student-performance-analyzer/
│
├── app.py
├── database.py
├── analytics.py
├── recommendations.py
├── quiz.py
├── models.py
├── seed_data.py
├── requirements.txt
├── README.md
│
└── data/
```

---

## Setup Instructions

### 1. Create a MongoDB Atlas Database

1. Go to https://www.mongodb.com/atlas
2. Create a free cluster.
3. Create a database user.
4. Add your current IP address in **Network Access**.
5. Copy your connection string.

It will look similar to this:

```text
mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

Do **not** paste this connection string into the source code.

---

### 2. Install Python Dependencies

From the project folder:

```bash
pip install -r requirements.txt
```

---

### 3. Set the MongoDB Environment Variable

#### macOS / Linux

```bash
export MONGODB_URI="mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

#### Windows PowerShell

```powershell
$env:MONGODB_URI="mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

Optional: set a custom database name.

```bash
export MONGODB_DB_NAME="student_performance_analyzer"
```

If `MONGODB_DB_NAME` is not set, the app uses `student_performance_analyzer`.

---

### 4. Run the App

```bash
streamlit run app.py
```

When the app starts, it automatically creates indexes and seeds sample subjects, topics, and questions if questions are not already present.

You can also seed manually:

```bash
python seed_data.py
```

---

## How to Demonstrate the MVP

Use this acceptance-test flow:

1. Start the app with `streamlit run app.py`.
2. Create a student profile.
3. Go to **📝 Take Quiz**.
4. Select **Mathematics**.
5. Select **Probability** or another topic.
6. Answer and submit the quiz.
7. Confirm the score and answer review are shown.
8. Take another quiz for the same topic.
9. Go to **🏠 Dashboard**.
10. Confirm overall accuracy, quizzes completed, strongest subject, weakest subject, weak topics, recommendation, and recent quiz results are loaded from MongoDB.
11. Go to **⚠️ Weak Topics**.
12. Confirm topic classification uses:
    - Below 65% = Weak
    - 65–84% = Needs Practice
    - 85%+ = Strong
13. Confirm repeated poor performance is detected after multiple low-scoring attempts.
14. Go to **📊 Progress**.
15. Confirm Plotly charts display actual stored data.
16. Go to **📚 Quiz History**.
17. Confirm previous attempts and answer details are visible.

---

## Important Notes

- The dashboard and analytics do not use hardcoded results.
- Quiz attempts and answers are stored in MongoDB.
- The recommendation system is rule-based Python logic.
- The app handles missing MongoDB connection, no attempts, no performance data, insufficient data, and missing questions with friendly messages.
- This MVP is intentionally small enough for a single student to understand, build, and present within 2–3 days.
