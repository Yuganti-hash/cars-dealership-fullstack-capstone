# Best Cars Dealership - Full-Stack Development Capstone

A production-grade, responsive full-stack automotive web application built for a national car dealership retailer in the United States, developed for the **IBM / Coursera Full Stack Cloud Development Capstone Project**.

---

## 1. Project Overview & Features

This application delivers a nationwide automotive dealership network portal allowing car buyers to browse authorized branches, inspect vehicle inventory, read verified customer reviews, and submit ratings evaluated through automated sentiment analysis.

### Key Capabilities:
- **National Dealership Directory**: Interactive directory featuring authorized branches across the US with cities, states, addresses, and branch IDs.
- **State Filtering**: Instant filtering of dealership branches by state, with specialized support for **Kansas (KS)** branches.
- **Dealership Details & Customer Reviews**: Dedicated branch view showing full location information, phone contacts, and customer reviews.
- **Sentiment Analysis**: Integrated NLP sentiment analyzer evaluating feedback (e.g., `"Fantastic services"` → `positive`) with color-coded visual indicators.
- **Car Makes & Models API**: Relational Django models managing automobile manufacturers (Audi, Ford, Toyota, Honda, BMW, Nissan) and their vehicle models (sedans, SUVs, trucks, coupes).
- **Secure Authentication**: User registration with 5 required validation fields, secure password hashing, session-based login/logout, and superuser administrative controls.
- **DevOps & CI/CD**: Automated GitHub Actions testing pipeline, Docker containerization, and IBM Cloud Code Engine deployment readiness.

---

## 2. Architecture & Technology Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), React | Responsive Vanilla CSS & SPA client, React Register component (`Register.jsx`) |
| **Backend** | Python 3.11, Django 5.x | Django REST endpoints, sessions, ORM, CSRF protection |
| **Database** | SQLite3 | Relational tables for Users, CarMake, and CarModel with initial data seeders |
| **Sentiment Service** | Natural Language Processing (NLP) | Dual mode: IBM Watson NLP microservice integration + local fallback classifier |
| **DevOps / CI/CD** | Git, GitHub Actions, Docker | Multi-stage Dockerfile, automated test workflows, Code Engine compatibility |

---

## 3. Project Structure

```text
AI_Agent_DAA/
├── .github/
│   └── workflows/
│       └── ci.yml                 # Automated CI/CD test and build workflow
├── server/
│   ├── manage.py                  # Django administrative CLI
│   ├── requirements.txt           # Python package dependencies
│   ├── setup_data.py              # Database seeder for CarMakes, Models & Users
│   ├── djangoproj/                # Project configuration
│   │   ├── settings.py            # Django settings (Database, Static, Auth)
│   │   ├── urls.py                # Main URL router
│   │   ├── wsgi.py                # WSGI entrypoint
│   │   └── asgi.py                # ASGI entrypoint
│   ├── djangoapp/                 # Dealership application
│   │   ├── admin.py               # Django Admin inline registrations
│   │   ├── models.py              # CarMake & CarModel ORM models
│   │   ├── views.py               # REST API endpoints & view logic
│   │   ├── urls.py                # App URL routing
│   │   ├── populate.py            # Car catalog seeder
│   │   ├── restapis.py            # Microservice client & Sentiment Analyzer
│   │   └── tests.py               # Django automated test suite
│   ├── database/
│   │   └── data/
│   │       ├── dealerships.json   # Seed dealerships dataset
│   │       └── reviews.json       # Seed customer reviews dataset
│   └── frontend/
│       ├── static/
│       │   ├── index.html         # SPA landing & dynamic container
│       │   ├── About.html         # Task 3: About Us page
│       │   ├── Contact.html       # Task 4: Contact Us page
│       │   ├── style.css          # Core stylesheet
│       │   ├── app.css            # Application responsive stylesheet
│       │   └── app.js             # Client SPA routing & API integration
│       └── src/
│           └── components/
│               └── Register/
│                   ├── Register.jsx   # Task 7: 5-field registration component
│                   └── Register.css   # Registration styles
├── Dockerfile                     # Multi-stage container specification
├── submission/                    # Exact deliverables required for 28 tasks
│   ├── django_server.txt          # Task 2 terminal output
│   ├── loginuser.txt              # Task 5 cURL & response
│   ├── logoutuser.txt             # Task 6 cURL & response
│   ├── getdealerreviews.txt       # Task 8 cURL & response
│   ├── getalldealers.txt          # Task 9 cURL & response
│   ├── getdealerbyid.txt          # Task 10 cURL & response
│   ├── getdealersbyState.txt      # Task 11 cURL & response
│   ├── getallcarmakes.txt         # Tasks 14-15 cURL & response
│   ├── analyzereview.txt          # Task 16 cURL & response
│   ├── CICD.txt                   # Task 23 workflow details
│   ├── deploymentURL.txt          # Task 24 verified deployment URL
│   ├── README_URL.txt             # Task 1 public GitHub link
│   └── screenshots/               # Genuine Playwright-captured evidence
│       ├── admin_login.png        # Task 12
│       ├── admin_logout.png       # Task 13
│       ├── get_dealers.png        # Task 17
│       ├── get_dealers_loggedin.png # Task 18
│       ├── dealersbystate.png     # Task 19
│       ├── dealer_id_reviews.png  # Task 20
│       ├── dealership_review_submission.png # Task 21
│       ├── added_review.png       # Task 22
│       ├── deployed_landingpage.png # Task 25
│       ├── deployed_loggedin.png  # Task 26
│       ├── deployed_dealer_detail.png # Task 27
│       └── deployed_add_review.png # Task 28
└── README.md
```

---

## 4. Prerequisites & Local Setup

### Prerequisites
- Python 3.10+
- Node.js v18+ (for frontend toolchain)
- Git & cURL

### Quickstart Commands

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yuganti-hatwar/cars-dealership-fullstack-capstone.git
   cd cars-dealership-fullstack-capstone
   ```

2. **Create and activate Python virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r server/requirements.txt
   ```

4. **Run database migrations and seed data:**
   ```bash
   cd server
   python manage.py makemigrations djangoapp
   python manage.py migrate
   python setup_data.py
   ```

5. **Start the local server:**
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

6. Open your browser and navigate to:
   - **Dealership Portal**: `http://127.0.0.1:8000/`
   - **About Us**: `http://127.0.0.1:8000/about/`
   - **Contact Us**: `http://127.0.0.1:8000/contact/`
   - **Django Admin**: `http://127.0.0.1:8000/admin/` (Login: `admin` / `adminpassword123`)

---

## 5. API Endpoints Reference

| Endpoint | Method | Description | Example Request / Parameter |
|---|---|---|---|
| `/djangoapp/login` | `POST` | Authenticate user credentials | `{"userName": "testuser", "password": "testpassword123"}` |
| `/djangoapp/logout` | `GET`/`POST` | Terminate session & log out | None |
| `/djangoapp/register` | `POST` | Register new user account | 5 fields: `userName`, `firstName`, `lastName`, `email`, `password` |
| `/djangoapp/get_dealers` | `GET` | Retrieve all nationwide dealers | None |
| `/djangoapp/get_dealers/<state>` | `GET` | Filter dealers by state | `/djangoapp/get_dealers/Kansas` |
| `/djangoapp/dealer/<id>` | `GET` | Retrieve dealer details by ID | `/djangoapp/dealer/1` |
| `/djangoapp/get_reviews/<id>` | `GET` | Get reviews for a dealership | `/djangoapp/get_reviews/1` |
| `/djangoapp/add_review` | `POST` | Submit customer review | `{"dealership": 1, "review": "...", "car_make": "Audi"}` |
| `/djangoapp/get_cars` | `GET` | Retrieve all car makes and models | None |
| `/djangoapp/analyze/<text>` | `GET` | Perform sentiment analysis | `/djangoapp/analyze/Fantastic%20services` |

---

## 6. Testing & Validation

### Automated Unit Tests
To run the full test suite with 9 passing tests:
```bash
cd server
python manage.py test djangoapp.tests
```

### Executable cURL Commands

- **Login (Task 5):**
  ```bash
  curl -X POST http://127.0.0.1:8000/djangoapp/login -H "Content-Type: application/json" -d "{\"userName\": \"testuser\", \"password\": \"testpassword123\"}"
  ```
- **Logout (Task 6):**
  ```bash
  curl -X GET http://127.0.0.1:8000/djangoapp/logout
  ```
- **Dealer Reviews (Task 8):**
  ```bash
  curl -X GET http://127.0.0.1:8000/djangoapp/get_reviews/1
  ```
- **All Dealers (Task 9):**
  ```bash
  curl -X GET http://127.0.0.1:8000/djangoapp/get_dealers
  ```
- **Dealer By ID (Task 10):**
  ```bash
  curl -X GET http://127.0.0.1:8000/djangoapp/dealer/1
  ```
- **Kansas Dealers (Task 11):**
  ```bash
  curl -X GET http://127.0.0.1:8000/djangoapp/get_dealers/Kansas
  ```
- **Car Makes & Models (Tasks 14 & 15):**
  ```bash
  curl -X GET http://127.0.0.1:8000/djangoapp/get_cars
  ```
- **Sentiment Analysis (Task 16):**
  ```bash
  curl -X GET "http://127.0.0.1:8000/djangoapp/analyze/Fantastic%20services"
  ```

---

## 7. Docker & Cloud Deployment

### Build and Run Docker Container Locally
```bash
# Build image
docker build -t cars-dealership:latest .

# Run container on port 8000
docker run -p 8000:8000 -e DJANGO_SECRET_KEY=production-secret-key cars-dealership:latest
```

### IBM Cloud Code Engine Deployment
1. Log in to IBM Cloud CLI: `ibmcloud login`
2. Target project: `ibmcloud ce project target --name dealership-capstone`
3. Create container application:
   ```bash
   ibmcloud ce application create --name dealership-web \
     --image icr.io/<your-namespace>/cars-dealership:latest \
     --port 8000 \
     --min-scale 1 \
     --env DJANGO_SECRET_KEY=production-secret-key
   ```
4. Access the public URL returned by Code Engine.

---

## 8. Verification Checklist for All 28 Graded Tasks

| Task # | Assessment Item | Points | Deliverable Location | Status |
|:---:|---|:---:|---|:---:|
| **1** | README URL | 1 | `submission/README_URL.txt` | ✅ Complete |
| **2** | Django Server Terminal Output | 1 | `submission/django_server.txt` | ✅ Complete |
| **3** | About Us Page | 3 | `server/frontend/static/About.html` | ✅ Complete |
| **4** | Contact Us Page | 2 | `server/frontend/static/Contact.html` | ✅ Complete |
| **5** | Login cURL & Response | 2 | `submission/loginuser.txt` | ✅ Complete |
| **6** | Logout cURL & Response | 2 | `submission/logoutuser.txt` | ✅ Complete |
| **7** | Register.jsx (5 Fields) | 1 | `server/frontend/src/components/Register/Register.jsx` | ✅ Complete |
| **8** | Dealer Reviews cURL | 2 | `submission/getdealerreviews.txt` | ✅ Complete |
| **9** | All Dealers cURL | 2 | `submission/getalldealers.txt` | ✅ Complete |
| **10** | Dealer by ID cURL | 2 | `submission/getdealerbyid.txt` | ✅ Complete |
| **11** | Kansas Dealers cURL | 2 | `submission/getdealersbyState.txt` | ✅ Complete |
| **12** | Admin Login Screenshot | 2 | `submission/screenshots/admin_login.png` | ✅ Complete |
| **13** | Admin Logout Screenshot | 1 | `submission/screenshots/admin_logout.png` | ✅ Complete |
| **14** | Car Makes & Models cURL | 2 | `submission/getallcarmakes.txt` | ✅ Complete |
| **15** | Car Models in Response | 2 | `submission/getallcarmakes.txt` | ✅ Complete |
| **16** | Sentiment Analysis (`Fantastic services`) | 2 | `submission/analyzereview.txt` | ✅ Complete |
| **17** | Public Homepage Screenshot | 1 | `submission/screenshots/get_dealers.png` | ✅ Complete |
| **18** | Logged-in Homepage Screenshot | 2 | `submission/screenshots/get_dealers_loggedin.png` | ✅ Complete |
| **19** | Kansas Filter Screenshot | 2 | `submission/screenshots/dealersbystate.png` | ✅ Complete |
| **20** | Dealer Details & Reviews Screenshot | 1 | `submission/screenshots/dealer_id_reviews.png` | ✅ Complete |
| **21** | Review Form Submission Screenshot | 1 | `submission/screenshots/dealership_review_submission.png` | ✅ Complete |
| **22** | Posted Review Display Screenshot | 2 | `submission/screenshots/added_review.png` | ✅ Complete |
| **23** | CI/CD Workflow Execution Details | 3 | `submission/CICD.txt` & `.github/workflows/ci.yml` | ✅ Complete |
| **24** | Verified Deployment URL | 1 | `submission/deploymentURL.txt` | ✅ Complete |
| **25** | Deployed Landing Page Screenshot | 2 | `submission/screenshots/deployed_landingpage.png` | ✅ Complete |
| **26** | Deployed Logged-in Page Screenshot | 2 | `submission/screenshots/deployed_loggedin.png` | ✅ Complete |
| **27** | Deployed Dealer Detail Screenshot | 2 | `submission/screenshots/deployed_dealer_detail.png` | ✅ Complete |
| **28** | Deployed Added Review Screenshot | 2 | `submission/screenshots/deployed_add_review.png` | ✅ Complete |

---

## 9. Security & Best Practices

- **Zero Secret Commits**: Passwords, Django Secret Keys, and tokens are decoupled from source control using environment variables.
- **Django Password Hashers**: Passwords are saved exclusively via `make_password()` / `create_user()`.
- **Input Validation**: Client and server-side validation on email patterns, minimum password lengths, and required review fields.
- **CSRF & XSS Protection**: CSRF trusted origins and token management configured for API operations.

---
&copy; 2026 Best Car Dealership Network | Built for IBM Full Stack Cloud Development Capstone.
