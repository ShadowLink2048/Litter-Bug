
# 🪰 Litter-Bug: Clean the World, One Piece at a Time 🌍

**Litter-Bug** is an interactive, geolocation-based environmental cleanup game that encourages users to collect and properly dispose of litter in real life. Designed as part of the **UW 2025 Hackathon "Save the World"** project, Litter-Bug combines the excitement of gaming with social good, offering leaderboards, achievements, and real-time communication to foster community-driven cleanup efforts.

## 📖 Table of Contents

1. [Project Overview](#project-overview)  
2. [Project Structure](#project-structure)  
3. [Frontend Overview](#frontend-overview)  
4. [Backend Overview](#backend-overview)  
5. [Setup Instructions](#setup-instructions)  
6. [API Documentation](#api-documentation)  
7. [Roadmap and Future Plans](#roadmap-and-future-plans)  
8. [License](#license)  
9. [Authors](#authors)

## 🏗️ Project Overview

Litter-Bug is structured as a **multi-service full-stack application**, including:

- **React Frontend (SPA)** with interactive maps and user profiles  
- **Python Flask REST APIs** for account management, trash/bin reporting, and real-time chat services  
- **MongoDB Backend** for geospatial data storage and user progress tracking  

The game rewards users with coins for proper waste disposal and allows social engagement through chat and leaderboards.

## 📂 Project Structure

```
Litter-Bug/
├── litter-bug-react/        # React frontend (game UI)
│   ├── public/              # Static assets
│   ├── src/                 # Main React source code
├── account-api/             # User account management API (Flask)
├── chatserver-api/          # Real-time chat functionality API (Flask)
├── garbage-api/             # Trash and bin management API (Flask)
├── database_py_files/       # MongoDB setup and shared utilities
├── testing/                 # Scripts for generating test data (users, scores)
├── requirements.txt         # Python backend dependencies
├── .gitignore               # Ignored files for Git version control
├── LICENSE                  # MIT License
└── README.md                # Full project documentation (this file)
```

## 🎨 Frontend Overview

### Technologies:
- **React**
- **React Router**
- **Axios**
- **Leaflet**

### Core Features:
- User Authentication
- Interactive Map
- Trash Collection Reporting
- Leaderboard
- Real-Time Chat

### Frontend Setup Instructions:

```bash
cd litter-bug-react
npm install
npm start
```

## 🧩 Backend Overview

### Technologies:
- **Python 3**
- **Flask**
- **MongoDB**
- **bcrypt**

### Backend Components:
1. **account-api/**
2. **chatserver-api/**
3. **garbage-api/**
4. **database_py_files/**

## 🚀 Setup Instructions (Full Stack)

### 1. Clone the Repository:
```bash
git clone https://github.com/WaaaaayTwoManyHats/Litter-Bug.git
cd Litter-Bug
```

### 2. Backend Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Ensure MongoDB is running and start each service:
```bash
python server.py
```

### 3. Frontend Setup
```bash
cd litter-bug-react
npm install
npm start
```

## 📡 API Documentation

### Authentication (Account API)
| Endpoint               | Method | Description                   |
|------------------------|--------|-------------------------------|
| `/api/signup`          | POST   | Create a new user             |
| `/api/login`           | POST   | Login and receive token       |
| `/api/user/<username>` | GET    | Fetch user profile (token)    |

### Trash and Bin Reporting (Garbage API)
| Endpoint                   | Method | Description                           |
|----------------------------|--------|---------------------------------------|
| `/api/bins/add`             | POST   | Add a new bin                        |
| `/api/trash/add`            | POST   | Report trash                         |
| `/api/bins/nearby`          | GET    | Get bins within a radius             |
| `/api/trash/nearby`         | GET    | Get trash within a radius            |

### Chat Server API
| Endpoint            | Method | Description                |
|---------------------|--------|----------------------------|
| `/api/chat/send`    | POST   | Send a message             |
| `/api/chat/history` | GET    | Retrieve chat history      |

## 🏆 Roadmap and Future Plans

- ✅ Basic account signup/login
- ✅ Trash and bin reporting
- ✅ Interactive map
- 🟡 WebSockets for chat
- 🟡 Gamification (avatars, badges)
- 🟡 Photo metadata integration
- 🟡 Mobile app development

## 📄 License

MIT License

```
MIT License

Permission is hereby granted, free of charge...
(license text omitted here for brevity)
```

## 👥 Authors

- Katherine Rodli  
- Jack Gardner  
- Dominic H-T  
- Morgan  
- Bryan Harris  

Special thanks to the team for their contributions to the **UW 2025 Hackathon "Save the World"** project.
