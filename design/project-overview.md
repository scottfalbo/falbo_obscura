# Falbo Obscura - Project Overview

## Project Structure

```txt
falbo_obscura/
├── backend/
│   ├── venv/              # Virtual environment
│   ├── requirements.txt   # Python dependencies
│   └── .gitignore        # Python gitignore
├── frontend/
│   ├── src/              # TypeScript source code
│   ├── package.json      # Node.js dependencies
│   ├── tsconfig.json     # TypeScript config
│   └── .gitignore       # Node.js gitignore
└── README.md
```

## Tech Stack

### Backend

- **Python 3.11**
- **FastAPI** - Web framework
- **Uvicorn** - Server

### Frontend

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling

## AWS Cloud Architecture

### Services
- **Lambda + API Gateway** - Serverless backend
- **DynamoDB** - Gallery metadata (NoSQL)
- **S3 + CloudFront** - Image storage + CDN
- **Cognito** - User authentication
- **SES** - Email service

### Portfolio Features
- Public gallery pages
- Admin login + content management UI
- Image upload and metadata management

## Flow

Frontend (Next.js) → API Gateway → Lambda (FastAPI) → DynamoDB/S3
                                            ↓
                                      Cognito (Auth)
