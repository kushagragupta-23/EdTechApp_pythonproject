#!/usr/bin/env python3
"""
Seed script for EduVerse — populates every table with realistic sample data
via the running FastAPI backend.  Run while the server is up on localhost:8000.

Usage:
    python3 seed_data.py          # default http://localhost:8000
    python3 seed_data.py http://myhost:9000  # custom base URL
"""

import sys, json, time
import urllib.request
import urllib.error

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
API  = f"{BASE}/api/v1"

def post(path: str, body: dict):
    """POST JSON to the API and return the response dict."""
    data = json.dumps(body).encode()
    req  = urllib.request.Request(
        f"{API}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        print(f"  ⚠  POST {path} → {e.code}: {detail}")
        return None

def get(path: str):
    """GET from the API."""
    with urllib.request.urlopen(f"{API}{path}") as resp:
        return json.loads(resp.read())

# ─────────────────────────────────────────
# 1. USERS  (3 instructors + 7 students)
# ─────────────────────────────────────────
print("\n━━━ Seeding Users ━━━")
users = [
    # Instructors
    {
        "name": "Dr. Priya Sharma",
        "email": "priya.sharma@eduverse.in",
        "phone": "+91-9876543210",
        "role": "instructor",
        "age": 38,
        "gender": "female",
        "bio": "Ph.D. in Computer Science from IIT Bombay. 12 years of teaching experience in Data Structures, Algorithms, and Machine Learning. Published 20+ research papers in top-tier conferences (NeurIPS, ICML). Passionate about making complex topics accessible to beginners.",
    },
    {
        "name": "Prof. Rajesh Kumar",
        "email": "rajesh.kumar@eduverse.in",
        "phone": "+91-9812345678",
        "role": "instructor",
        "age": 45,
        "gender": "male",
        "bio": "M.Tech from IISc Bangalore with 18 years of industry and academic experience. Former Senior Engineer at TCS and Infosys. Specialises in Database Management Systems, Cloud Computing, and Software Engineering. Known for hands-on, project-based teaching methodology.",
    },
    {
        "name": "Dr. Ananya Patel",
        "email": "ananya.patel@eduverse.in",
        "phone": "+91-9900112233",
        "role": "instructor",
        "age": 34,
        "gender": "female",
        "bio": "Ph.D. in Mathematics from ISI Kolkata. Expert in Linear Algebra, Probability, and Statistical Learning. Conducts workshops on mathematical foundations for AI/ML across India. Author of the textbook 'Mathematical Thinking for Engineers'.",
    },
    # Students
    {
        "name": "Kushagra Gupta",
        "email": "kushagra.gupta@student.eduverse.in",
        "phone": "+91-7890123456",
        "role": "student",
        "age": 20,
        "gender": "male",
        "bio": "Second-year B.Tech student in Computer Science. Interested in full-stack web development, competitive programming, and open-source contributions. Active member of the college coding club and a Codeforces Specialist (1500+ rating).",
    },
    {
        "name": "Aishwarya Nevrekar",
        "email": "aishwarya.nevrekar@student.eduverse.in",
        "phone": "+91-8901234567",
        "role": "student",
        "age": 20,
        "gender": "male",
        "bio": "Second-year B.Tech student passionate about backend development, databases, and system design. Built multiple Python and FastAPI projects. Enjoys solving algorithmic puzzles and contributing to campus hackathons.",
    },
    {
        "name": "Sampad Kar",
        "email": "sampad.kar@student.eduverse.in",
        "phone": "+91-9988776655",
        "role": "student",
        "age": 21,
        "gender": "female",
        "bio": "Third-year B.Tech student with a keen interest in Machine Learning and Data Science. Completed internships at ZS Associates and Mu Sigma. Kaggle Competitions Expert with two silver medals. Aspires to pursue an M.S. in AI.",
    },
    {
        "name": "Niladri Ghosh",
        "email": "niladri.ghosh@student.eduverse.in",
        "phone": "+91-7766554433",
        "role": "student",
        "age": 22,
        "gender": "male",
        "bio": "Final-year B.Tech student specialising in Cloud Computing and DevOps. AWS Certified Cloud Practitioner. Interned at Amazon India. Loves automating workflows, building CI/CD pipelines, and exploring Kubernetes.",
    },
    {
        "name": "Jayanth Vukkisa",
        "email": "jayanth.vukkisa@student.eduverse.in",
        "phone": "+91-9090909090",
        "role": "student",
        "age": 20,
        "gender": "male",
        "bio": "Third-year B.Tech student, passionate about cloud computing and back-end development. Currently learning Python and building highly scalable web applications.",
    },
    {
        "name": "Rohit Deshmukh",
        "email": "rohit.deshmukh@student.eduverse.in",
        "phone": "+91-8080808080",
        "role": "student",
        "age": 21,
        "gender": "male",
        "bio": "Third-year Information Technology student. Active open-source contributor (50+ GitHub stars). Built a college ERP prototype used by 200+ students. Proficient in React, Node.js, and PostgreSQL.",
    },
    {
        "name": "Aisha Khan",
        "email": "aisha.khan@student.eduverse.in",
        "phone": "+91-7070707070",
        "role": "student",
        "age": 20,
        "gender": "female",
        "bio": "Second-year B.Tech student with a focus on cybersecurity and ethical hacking. Completed the Google Cybersecurity Certificate. Participates in CTF competitions and ranked in top 100 nationally. Also interested in blockchain technology.",
    },
]

user_ids = []
for u in users:
    r = post("/users", u)
    if r:
        user_ids.append(r["id"])
        print(f"  ✓ User #{r['id']} — {r['name']} ({r['role']})")
    else:
        user_ids.append(None)

# Map by role for convenience
instructor_ids = [user_ids[i] for i in range(3) if user_ids[i]]
student_ids    = [user_ids[i] for i in range(3, 10) if user_ids[i]]

# ─────────────────────────────────────────
# 2. COURSES  (6 courses with full details)
# ─────────────────────────────────────────
print("\n━━━ Seeding Courses ━━━")
courses = [
    {
        "name": "CS201",
        "title": "Data Structures & Algorithms",
        "description": "A comprehensive course covering fundamental and advanced data structures — arrays, linked lists, stacks, queues, trees (BST, AVL, Red-Black), heaps, hash tables, and graphs. Includes algorithm design paradigms: divide-and-conquer, greedy, dynamic programming, and backtracking. Weekly coding contests and LeetCode problem sets are integral parts of the coursework.",
        "category": "Computer Science",
        "duration": "16 weeks",
        "prerequisites": "Basic programming in C/C++ or Python, Introduction to Computer Science",
        "instructor_id": instructor_ids[0] if instructor_ids else None,
        "video_link": "https://youtube.com/playlist?list=PLDSAcomp-science-dsa",
    },
    {
        "name": "CS301",
        "title": "Database Management Systems",
        "description": "In-depth study of relational databases covering the ER model, normalisation (1NF–BCNF), SQL (DDL, DML, DCL), transactions (ACID properties), concurrency control, indexing (B-trees, hash indices), query optimisation, and NoSQL paradigms (MongoDB, Redis). Students build a full-scale database application as a capstone project.",
        "category": "Computer Science",
        "duration": "14 weeks",
        "prerequisites": "Data Structures & Algorithms, Basic SQL knowledge",
        "instructor_id": instructor_ids[1] if len(instructor_ids) > 1 else None,
        "video_link": "https://youtube.com/playlist?list=PLDSAcomp-science-dbms",
    },
    {
        "name": "MA201",
        "title": "Linear Algebra for Engineers",
        "description": "Covers vector spaces, linear transformations, matrices, determinants, eigenvalues and eigenvectors, singular value decomposition (SVD), principal component analysis (PCA), and applications in computer graphics, machine learning, and signal processing. Emphasis on geometric intuition and computational tools (NumPy, MATLAB).",
        "category": "Mathematics",
        "duration": "12 weeks",
        "prerequisites": "Calculus I, Basic matrix operations",
        "instructor_id": instructor_ids[2] if len(instructor_ids) > 2 else None,
        "video_link": "https://youtube.com/playlist?list=PLmath-linear-algebra",
    },
    {
        "name": "CS401",
        "title": "Machine Learning Fundamentals",
        "description": "Introduction to supervised and unsupervised learning: linear and logistic regression, decision trees, random forests, SVMs, k-means clustering, PCA, neural network basics, and evaluation metrics (precision, recall, F1, ROC-AUC). Hands-on labs using scikit-learn, pandas, and Jupyter Notebooks. Final project involves deploying a model using Flask/FastAPI.",
        "category": "Artificial Intelligence",
        "duration": "16 weeks",
        "prerequisites": "Linear Algebra, Probability & Statistics, Python programming",
        "instructor_id": instructor_ids[0] if instructor_ids else None,
        "video_link": "https://youtube.com/playlist?list=PLai-ml-fundamentals",
    },
    {
        "name": "CS202",
        "title": "Web Development Full Stack",
        "description": "End-to-end web development covering HTML5, CSS3 (Flexbox, Grid), JavaScript (ES6+), React.js, Node.js, Express.js, REST API design, authentication (JWT, OAuth), database integration (PostgreSQL, MongoDB), deployment (Docker, Heroku, Vercel), and CI/CD pipelines. Students build and deploy a production-grade web application.",
        "category": "Web Development",
        "duration": "18 weeks",
        "prerequisites": "Basic programming, HTML/CSS fundamentals",
        "instructor_id": instructor_ids[1] if len(instructor_ids) > 1 else None,
        "video_link": "https://youtube.com/playlist?list=PLweb-fullstack-dev",
    },
    {
        "name": "CS501",
        "title": "Cloud Computing & DevOps",
        "description": "Covers cloud service models (IaaS, PaaS, SaaS), virtualisation, containerisation (Docker), orchestration (Kubernetes), AWS core services (EC2, S3, Lambda, RDS), infrastructure as code (Terraform), CI/CD (GitHub Actions, Jenkins), monitoring (Prometheus, Grafana), and security best practices. Includes hands-on labs with real AWS resources.",
        "category": "Cloud & Infrastructure",
        "duration": "14 weeks",
        "prerequisites": "Operating Systems, Networking basics, Linux command line",
        "instructor_id": instructor_ids[1] if len(instructor_ids) > 1 else None,
        "video_link": "https://youtube.com/playlist?list=PLcloud-devops",
    },
]

course_ids = []
for c in courses:
    r = post("/courses", c)
    if r:
        course_ids.append(r["id"])
        print(f"  ✓ Course #{r['id']} — {r['name']}: {r['title']}")
    else:
        course_ids.append(None)

# ─────────────────────────────────────────
# 3. PAYMENTS  (one per enrollment below)
# ─────────────────────────────────────────
print("\n━━━ Seeding Payments ━━━")

# Enrollment plan: each student → 2–3 courses
# student_ids[0] = Kushagra  → CS201, CS202, CS301
# student_ids[1] = Aishwarya    → CS201, CS301, CS501
# student_ids[2] = Sampad     → CS401, MA201, CS201
# student_ids[3] = Niladri     → CS501, CS202, CS401
# student_ids[4] = Kavya     → CS202, MA201
# student_ids[5] = Rohit     → CS201, CS202, CS501
# student_ids[6] = Aisha     → CS301, CS501, CS401

enrollment_plan = []
if len(student_ids) >= 7 and len(course_ids) >= 6:
    enrollment_plan = [
        (student_ids[0], course_ids[0]),  # Kushagra → DSA
        (student_ids[0], course_ids[4]),  # Kushagra → Web Dev
        (student_ids[0], course_ids[1]),  # Kushagra → DBMS
        (student_ids[1], course_ids[0]),  # Aishwarya → DSA
        (student_ids[1], course_ids[1]),  # Aishwarya → DBMS
        (student_ids[1], course_ids[5]),  # Aishwarya → Cloud
        (student_ids[2], course_ids[3]),  # Sampad → ML
        (student_ids[2], course_ids[2]),  # Sampad → Linear Algebra
        (student_ids[2], course_ids[0]),  # Sampad → DSA
        (student_ids[3], course_ids[5]),  # Niladri → Cloud
        (student_ids[3], course_ids[4]),  # Niladri → Web Dev
        (student_ids[3], course_ids[3]),  # Niladri → ML
        (student_ids[4], course_ids[4]),  # Kavya → Web Dev
        (student_ids[4], course_ids[2]),  # Kavya → Linear Algebra
        (student_ids[5], course_ids[0]),  # Rohit → DSA
        (student_ids[5], course_ids[4]),  # Rohit → Web Dev
        (student_ids[5], course_ids[5]),  # Rohit → Cloud
        (student_ids[6], course_ids[1]),  # Aisha → DBMS
        (student_ids[6], course_ids[5]),  # Aisha → Cloud
        (student_ids[6], course_ids[3]),  # Aisha → ML
    ]

payment_ids = []
for idx, (sid, cid) in enumerate(enrollment_plan, start=1):
    txn_id = f"TXN-2026-{idx:05d}"
    r = post("/payments", {"student_id": sid, "course_id": cid, "transaction_id": txn_id})
    if r:
        payment_ids.append(r["id"])
        print(f"  ✓ Payment #{r['id']} — Student {sid} → Course {cid}  ({txn_id})")
    else:
        payment_ids.append(None)

# ─────────────────────────────────────────
# 4. ENROLLMENTS
# ─────────────────────────────────────────
print("\n━━━ Seeding Enrollments ━━━")
enrollment_ids = []
for idx, (sid, cid) in enumerate(enrollment_plan):
    pid = payment_ids[idx] if idx < len(payment_ids) else None
    r = post("/enrollments", {"student_id": sid, "course_id": cid, "payment_id": pid})
    if r:
        enrollment_ids.append(r["id"])
        print(f"  ✓ Enrollment #{r['id']} — Student {sid} → Course {cid}")
    else:
        enrollment_ids.append(None)

# ─────────────────────────────────────────
# 5. ASSIGNMENTS  (2–3 per course)
# ─────────────────────────────────────────
print("\n━━━ Seeding Assignments ━━━")
assignments_data = [
    # CS201 — DSA
    {"course_id": course_ids[0], "title": "Array & String Manipulation Lab", "description": "Implement solutions for 10 problems covering two-pointer technique, sliding window, and prefix sums. Problems sourced from LeetCode Medium difficulty. Submit via GitHub repository link.", "max_score": 100.0},
    {"course_id": course_ids[0], "title": "Binary Tree Operations Project", "description": "Build a Binary Search Tree library in Python with insert, delete, search, in-order/pre-order/post-order traversal, height computation, and balance checking. Include unit tests (pytest) with 90%+ coverage.", "max_score": 100.0},
    {"course_id": course_ids[0], "title": "Graph Algorithms Challenge", "description": "Implement BFS, DFS, Dijkstra's shortest path, and Kruskal's MST. Apply them to solve a real-world routing problem (campus navigation system). Present a working demo.", "max_score": 150.0},
    # CS301 — DBMS
    {"course_id": course_ids[1], "title": "ER Modelling & Normalisation", "description": "Design an Entity-Relationship diagram for a hospital management system with at least 8 entities. Normalise the schema to BCNF. Submit the ER diagram (draw.io), SQL DDL scripts, and a written report explaining each normalisation step.", "max_score": 100.0},
    {"course_id": course_ids[1], "title": "SQL Query Mastery Assignment", "description": "Write 25 SQL queries of increasing complexity (joins, subqueries, window functions, CTEs, recursive queries) against the provided Northwind dataset. Include query execution plans and optimisation notes.", "max_score": 100.0},
    # MA201 — Linear Algebra
    {"course_id": course_ids[2], "title": "SVD & PCA Mini-Project", "description": "Apply Singular Value Decomposition for image compression (reduce a 1024×1024 image to rank-50 approximation). Then apply PCA on the Iris dataset for dimensionality reduction. Submit a Jupyter Notebook with visualisations and mathematical explanations.", "max_score": 100.0},
    {"course_id": course_ids[2], "title": "Eigenvalue Problem Set", "description": "Solve 15 problems on eigenvalues, eigenvectors, diagonalisation, and the Cayley-Hamilton theorem. Problems range from computational exercises to proof-based questions. Handwritten or LaTeX submissions accepted.", "max_score": 80.0},
    # CS401 — ML
    {"course_id": course_ids[3], "title": "Regression & Classification Lab", "description": "Build a housing price predictor (linear regression) and a spam classifier (logistic regression) using scikit-learn. Compare performance with decision trees and random forests. Submit a Jupyter Notebook with EDA, feature engineering, model training, and evaluation (RMSE, accuracy, confusion matrix).", "max_score": 100.0},
    {"course_id": course_ids[3], "title": "End-to-End ML Pipeline Project", "description": "Choose a real-world dataset from Kaggle, perform complete ML pipeline: data cleaning, EDA, feature engineering, model selection (try 3+ algorithms), hyperparameter tuning (GridSearch/RandomSearch), and deploy via FastAPI with a simple web interface. Present a 10-minute demo.", "max_score": 200.0},
    # CS202 — Web Dev
    {"course_id": course_ids[4], "title": "Responsive Portfolio Website", "description": "Create a personal portfolio website using HTML5, CSS3 (Flexbox/Grid), and vanilla JavaScript. Must include: hero section, about, projects showcase (at least 3), skills, contact form (with validation), dark mode toggle, and smooth scroll. Fully responsive (mobile-first design). Deploy on Vercel or Netlify.", "max_score": 100.0},
    {"course_id": course_ids[4], "title": "Full-Stack CRUD Application", "description": "Build a task management application with React frontend and Node.js/Express backend. Features: user registration/login (JWT), CRUD for tasks, drag-and-drop priority ordering, filtering/search, and PostgreSQL persistence. Dockerise the application and provide a docker-compose.yml.", "max_score": 150.0},
    # CS501 — Cloud
    {"course_id": course_ids[5], "title": "Docker & Kubernetes Lab", "description": "Containerise a multi-service application (frontend + backend + database) using Docker. Write Dockerfiles, docker-compose.yml, and Kubernetes manifests (Deployment, Service, Ingress, ConfigMap, Secret). Deploy on a local Minikube cluster and document the process.", "max_score": 100.0},
    {"course_id": course_ids[5], "title": "AWS Infrastructure as Code", "description": "Use Terraform to provision AWS infrastructure: VPC with public/private subnets, EC2 instances behind an ALB, RDS PostgreSQL, S3 bucket for static assets, and CloudFront CDN. Set up a CI/CD pipeline using GitHub Actions to deploy a sample application on each push to main.", "max_score": 150.0},
]

assignment_ids = []
for a in assignments_data:
    r = post("/assignments", a)
    if r:
        assignment_ids.append(r["id"])
        print(f"  ✓ Assignment #{r['id']} — {a['title']} (Course {a['course_id']})")
    else:
        assignment_ids.append(None)

# ─────────────────────────────────────────
# 6. REVIEWS  (2–3 per course, from enrolled students)
# ─────────────────────────────────────────
print("\n━━━ Seeding Reviews ━━━")
reviews_data = [
    # CS201 (DSA) — reviewed by Kushagra, Aishwarya, Sampad
    {"student_id": student_ids[0], "course_id": course_ids[0], "description": "Excellent course! Dr. Priya explains complex topics like dynamic programming and graph algorithms with incredible clarity. The weekly LeetCode contests pushed me to practice consistently. I went from barely solving Easy problems to comfortably tackling Mediums. Highly recommended for anyone serious about placements."},
    {"student_id": student_ids[1], "course_id": course_ids[0], "description": "One of the best DSA courses I've taken. The progression from basics to advanced topics is very well structured. The Binary Tree project was challenging but rewarding — I learnt so much about recursion and tree balancing. Only wish there were more practice problems on graph theory."},
    {"student_id": student_ids[2], "course_id": course_ids[0], "description": "Very thorough coverage of data structures. The teaching style is engaging and the coding assignments are practical. As someone preparing for ML, understanding algorithmic complexity from this course has been invaluable. The sliding window technique lesson was a game-changer."},
    # CS301 (DBMS) — reviewed by Kushagra, Aishwarya, Aisha
    {"student_id": student_ids[0], "course_id": course_ids[1], "description": "Prof. Rajesh makes database concepts feel intuitive. The normalisation chapter was especially well-taught — I finally understood why BCNF matters. The hands-on SQL assignments with the Northwind dataset gave me real confidence for internship interviews. Great course!"},
    {"student_id": student_ids[1], "course_id": course_ids[1], "description": "Fantastic course that covers both theory and practice. I appreciated the emphasis on query optimisation and execution plans — something most courses skip. The ER modelling project for the hospital system was complex but realistic. Prof. Rajesh's industry experience really shows."},
    # MA201 (Linear Algebra) — reviewed by Sampad, Kavya
    {"student_id": student_ids[2], "course_id": course_ids[2], "description": "Dr. Ananya's geometric intuition for linear algebra concepts is outstanding. The way she connects SVD to image compression and PCA to real ML applications makes the math feel purposeful rather than abstract. The NumPy labs complemented the theory perfectly."},
    {"student_id": student_ids[4], "course_id": course_ids[2], "description": "As a first-year student, this was challenging but incredibly rewarding. Dr. Ananya is patient and explains concepts multiple times from different angles. The eigenvalue problem set was tough, but the office hours and peer study groups helped a lot. Solid foundation for future AI/ML courses."},
    # CS401 (ML) — reviewed by Sampad, Niladri, Aisha
    {"student_id": student_ids[2], "course_id": course_ids[3], "description": "Perfect course for ML beginners with a math background. The Kaggle project was the highlight — I built a complete pipeline from data cleaning to deployment. Dr. Priya's explanations of bias-variance tradeoff and regularisation were crystal clear. My Kaggle ranking improved significantly after this course."},
    {"student_id": student_ids[3], "course_id": course_ids[3], "description": "Good introduction to Machine Learning. The hands-on labs using scikit-learn were very practical. I especially enjoyed the comparison between different classifiers. The final project of deploying a model via FastAPI was relevant and fun. Would have liked more coverage on deep learning though."},
    # CS202 (Web Dev) — reviewed by Kushagra, Niladri, Rohit
    {"student_id": student_ids[0], "course_id": course_ids[4], "description": "This course transformed me from someone who knew basic HTML to a full-stack developer. The progression from vanilla JS to React and then Node.js was smooth. The portfolio project helped me land a freelance gig! Prof. Rajesh's Docker lesson was a bonus I didn't expect. 10/10 would recommend."},
    {"student_id": student_ids[3], "course_id": course_ids[4], "description": "Comprehensive coverage of the modern web stack. The full-stack CRUD project was intense but incredibly educational — I learnt JWT auth, React hooks, and PostgreSQL in one go. The deployment section (Docker + Vercel) was practical and industry-relevant. Excellent course."},
    {"student_id": student_ids[5], "course_id": course_ids[4], "description": "As someone who already knew React, I still found immense value in this course. The backend sections (Node.js, Express, REST API design) filled gaps in my knowledge. The emphasis on code quality, testing, and deployment practices set this apart from typical web dev courses."},
    # CS501 (Cloud) — reviewed by Aishwarya, Niladri, Aisha
    {"student_id": student_ids[1], "course_id": course_ids[5], "description": "Incredible course for understanding cloud infrastructure. The AWS hands-on labs were eye-opening — I set up my first production-grade infrastructure with load balancers, auto-scaling, and RDS. The Terraform section was particularly valuable. Prof. Rajesh's industry anecdotes make lectures entertaining."},
    {"student_id": student_ids[3], "course_id": course_ids[5], "description": "This course solidified my career direction toward DevOps. The Kubernetes section was challenging but Prof. Rajesh breaks it down into manageable pieces. Setting up a full CI/CD pipeline with GitHub Actions and deploying to AWS felt like real work experience. Already applying these skills at my internship."},
    {"student_id": student_ids[6], "course_id": course_ids[5], "description": "Great blend of theory and practice. The security best practices section was especially relevant for me given my cybersecurity background. Learning IaC with Terraform was a highlight — the idea of version-controlling infrastructure is powerful. Well-paced and well-taught."},
]

for rv in reviews_data:
    r = post("/reviews", rv)
    if r:
        print(f"  ✓ Review #{r['id']} — Student {rv['student_id']} reviewed Course {rv['course_id']}")

# ─────────────────────────────────────────
# 7. PROGRESS  (for each enrollment)
# ─────────────────────────────────────────
print("\n━━━ Seeding Progress ━━━")
progress_data = [
    # Kushagra: DSA 85%, Web Dev 60%, DBMS 45%
    {"student_id": student_ids[0], "course_id": course_ids[0], "completion_percentage": 85.0, "status": "in_progress"},
    {"student_id": student_ids[0], "course_id": course_ids[4], "completion_percentage": 60.0, "status": "in_progress"},
    {"student_id": student_ids[0], "course_id": course_ids[1], "completion_percentage": 45.0, "status": "in_progress"},
    # Aishwarya: DSA 92%, DBMS 78%, Cloud 30%
    {"student_id": student_ids[1], "course_id": course_ids[0], "completion_percentage": 92.0, "status": "in_progress"},
    {"student_id": student_ids[1], "course_id": course_ids[1], "completion_percentage": 78.0, "status": "in_progress"},
    {"student_id": student_ids[1], "course_id": course_ids[5], "completion_percentage": 30.0, "status": "in_progress"},
    # Sampad: ML 100%, Linear Algebra 100%, DSA 70%
    {"student_id": student_ids[2], "course_id": course_ids[3], "completion_percentage": 100.0, "status": "completed"},
    {"student_id": student_ids[2], "course_id": course_ids[2], "completion_percentage": 100.0, "status": "completed"},
    {"student_id": student_ids[2], "course_id": course_ids[0], "completion_percentage": 70.0, "status": "in_progress"},
    # Niladri: Cloud 100%, Web Dev 88%, ML 55%
    {"student_id": student_ids[3], "course_id": course_ids[5], "completion_percentage": 100.0, "status": "completed"},
    {"student_id": student_ids[3], "course_id": course_ids[4], "completion_percentage": 88.0, "status": "in_progress"},
    {"student_id": student_ids[3], "course_id": course_ids[3], "completion_percentage": 55.0, "status": "in_progress"},
    # Kavya: Web Dev 25%, Linear Algebra 40%
    {"student_id": student_ids[4], "course_id": course_ids[4], "completion_percentage": 25.0, "status": "in_progress"},
    {"student_id": student_ids[4], "course_id": course_ids[2], "completion_percentage": 40.0, "status": "in_progress"},
    # Rohit: DSA 100%, Web Dev 95%, Cloud 15%
    {"student_id": student_ids[5], "course_id": course_ids[0], "completion_percentage": 100.0, "status": "completed"},
    {"student_id": student_ids[5], "course_id": course_ids[4], "completion_percentage": 95.0, "status": "in_progress"},
    {"student_id": student_ids[5], "course_id": course_ids[5], "completion_percentage": 15.0, "status": "not_started"},
    # Aisha: DBMS 65%, Cloud 50%, ML 35%
    {"student_id": student_ids[6], "course_id": course_ids[1], "completion_percentage": 65.0, "status": "in_progress"},
    {"student_id": student_ids[6], "course_id": course_ids[5], "completion_percentage": 50.0, "status": "in_progress"},
    {"student_id": student_ids[6], "course_id": course_ids[3], "completion_percentage": 35.0, "status": "in_progress"},
]

for p in progress_data:
    r = post("/progress", p)
    if r:
        print(f"  ✓ Progress #{r['id']} — Student {p['student_id']} → Course {p['course_id']} ({p['completion_percentage']}%, {p['status']})")

# ─────────────────────────────────────────
# 8. CERTIFICATIONS  (for completed courses)
# ─────────────────────────────────────────
print("\n━━━ Seeding Certifications ━━━")
certs_data = [
    {"student_id": student_ids[2], "course_id": course_ids[3], "certificate_url": "https://eduverse.in/certificates/CERT-ML-SAMPAD-2026"},
    {"student_id": student_ids[2], "course_id": course_ids[2], "certificate_url": "https://eduverse.in/certificates/CERT-LA-SAMPAD-2026"},
    {"student_id": student_ids[3], "course_id": course_ids[5], "certificate_url": "https://eduverse.in/certificates/CERT-CLOUD-NILADRI-2026"},
    {"student_id": student_ids[5], "course_id": course_ids[0], "certificate_url": "https://eduverse.in/certificates/CERT-DSA-ROHIT-2026"},
]

for ct in certs_data:
    r = post("/certifications", ct)
    if r:
        print(f"  ✓ Certificate #{r['id']} — Student {ct['student_id']} for Course {ct['course_id']}")

# ─────────────────────────────────────────
# 9. ANNOUNCEMENTS  (2–3 per course)
# ─────────────────────────────────────────
print("\n━━━ Seeding Announcements ━━━")
announcements_data = [
    {"course_id": course_ids[0], "author_id": instructor_ids[0], "title": "Mid-Semester Coding Contest — This Saturday", "content": "Dear students, the mid-semester coding contest will be held this Saturday from 10 AM to 1 PM on HackerRank. Topics covered: Arrays, Strings, Linked Lists, Stacks, and Queues. The contest will count for 15% of your grade. Practice well and good luck!"},
    {"course_id": course_ids[0], "author_id": instructor_ids[0], "title": "Office Hours Extended for Graph Week", "content": "Given the complexity of this week's graph algorithms material (BFS, DFS, Dijkstra, Bellman-Ford), I'm extending office hours to Tuesday and Thursday 4–6 PM in addition to the regular Wednesday slot. Feel free to drop by with questions."},
    {"course_id": course_ids[1], "author_id": instructor_ids[1], "title": "Guest Lecture: Database Internals at Scale", "content": "We have a guest lecture next Wednesday by Mr. Vikram Singh, Senior Database Architect at Flipkart, on 'How We Scale PostgreSQL for 10 Million Daily Transactions'. Attendance is mandatory and counts toward participation marks. Venue: Seminar Hall B."},
    {"course_id": course_ids[1], "author_id": instructor_ids[1], "title": "ER Diagram Submission Deadline Extended", "content": "Due to the Diwali break, the ER Modelling assignment deadline has been extended by one week to November 15th. Please use this extra time to refine your normalisation steps and add proper documentation. Late submissions beyond the new deadline will incur a 10% penalty per day."},
    {"course_id": course_ids[2], "author_id": instructor_ids[2], "title": "SVD Project Guidelines Posted", "content": "The SVD & PCA Mini-Project guidelines have been posted on the course page. You may work in pairs. Submission format: Jupyter Notebook (.ipynb) + a 2-page report (PDF). Focus on visual explanations — show the image compression at different rank approximations. Due date: December 1st."},
    {"course_id": course_ids[3], "author_id": instructor_ids[0], "title": "Kaggle Competition Registration Open", "content": "The course Kaggle competition 'EduVerse Housing Price Challenge' is now live. Register with your university email. Top 3 performers get bonus marks (10, 7, 5 respectively). The competition closes on December 15th. Start exploring the dataset early!"},
    {"course_id": course_ids[3], "author_id": instructor_ids[0], "title": "End-Semester Project Demo Schedule", "content": "Project demos will be held during the last week of classes (Dec 18–22). Each team gets a 10-minute slot followed by 5 minutes of Q&A. Ensure your FastAPI deployment is live and accessible. Sign up for your preferred time slot on the shared Google Sheet."},
    {"course_id": course_ids[4], "author_id": instructor_ids[1], "title": "React.js Workshop — Extra Session", "content": "I'm organising an extra 3-hour React.js workshop this Sunday (10 AM – 1 PM) for students who want additional practice with hooks (useState, useEffect, useContext) and React Router. Bring your laptops with Node.js pre-installed. Location: Computer Lab 3."},
    {"course_id": course_ids[4], "author_id": instructor_ids[1], "title": "Portfolio Website Showcase Event", "content": "We'll be hosting a Portfolio Showcase Event on November 25th where each student presents their portfolio website to the class. Best designs will be featured on the department website. This is also great practice for interview presentations!"},
    {"course_id": course_ids[5], "author_id": instructor_ids[1], "title": "AWS Free Tier Credits Available", "content": "Good news! I've arranged AWS Educate credits ($100 per student) for hands-on labs. Claim your credits via the link shared on email before November 10th. Remember to stop/terminate resources after each lab to avoid burning through credits."},
    {"course_id": course_ids[5], "author_id": instructor_ids[1], "title": "Kubernetes Lab Rescheduled", "content": "The Kubernetes hands-on lab originally scheduled for Thursday has been moved to next Monday due to a campus power maintenance. Please complete the Docker pre-requisite lab before attending. Minikube and kubectl should be installed on your machines."},
]

for an in announcements_data:
    r = post("/announcements", an)
    if r:
        print(f"  ✓ Announcement #{r['id']} — '{an['title']}' (Course {an['course_id']})")

# ─────────────────────────────────────────
# Summary
# ─────────────────────────────────────────
print("\n" + "═" * 50)
print("  ✅  Seeding complete!")
print("═" * 50)

# Print summary counts
try:
    for ep in ["users", "courses", "enrollments", "payments", "reviews",
               "certifications", "assignments", "progress", "announcements"]:
        data = get(f"/{ep}?limit=1")
        print(f"  {ep:20s} → {data['total']} records")
except:
    pass

print("\n  Open http://localhost:3000 to see the data in the frontend.\n")
