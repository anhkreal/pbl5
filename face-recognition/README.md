# Face Recognition API - Backend System

A production-ready FastAPI backend for face recognition with MySQL authentication, InsightFace integration, and FAISS vector search.

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture) 
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [InsightFace Integration](#insightface-integration)
- [Age/Gender Models](#agegender-models)
- [Anti-Spoofing](#anti-spoofing)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

This backend system provides face recognition capabilities through a RESTful API, featuring:

- **Face Recognition**: ArcFace-based face embedding and similarity search
- **Vector Database**: FAISS for efficient similarity search across face embeddings
- **Authentication**: MySQL-based user authentication system
- **Anti-Spoofing**: DeepFace integration for liveness detection
- **Age/Gender Prediction**: Optional demographic analysis
- **Scalable Architecture**: FastAPI with async support

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐      ┌─────────────────┐
│   Client Apps   │───▶│  FastAPI Backend │───▶│  MySQL Database │
└─────────────────┘    └─────────────────┘      └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ FAISS Vector DB │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ InsightFace     │
                       │ (ArcFace Model) │
                       └─────────────────┘
```

**Data Flow:**
1. **Authentication**: User login via MySQL authentication
2. **Image Processing**: Face detection and embedding extraction using InsightFace
3. **Vector Storage**: Face embeddings stored in FAISS index
4. **Similarity Search**: Query faces against stored embeddings
5. **Results**: Return matched faces with similarity scores

## Features

### Core Features
- **Face Recognition**: High-accuracy face matching using ArcFace embeddings
- **User Management**: Registration, login, and profile management
- **Face Database**: Add, edit, delete face embeddings per person
- **Similarity Search**: Find top-N similar faces with confidence scores
- **Real-time Query**: Fast face queries with optimized FAISS search

### Advanced Features  
- **Anti-Spoofing**: Optional liveness detection using DeepFace
- **Age/Gender Prediction**: Demographic analysis of detected faces
- **Batch Processing**: Multiple face processing in single request
- **Index Management**: Reset, rebuild, and optimize FAISS index
- **Monitoring**: System status and performance metrics

## Directory Structure

```
face_api/
├── app.py                    # FastAPI application entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
│
├── api/                      # API endpoint handlers
│   ├── login.py             # User authentication
│   ├── register.py          # User registration  
│   ├── face_query.py        # Face recognition queries
│   ├── add_embedding.py     # Add face embeddings
│   ├── edit_embedding.py    # Modify face data
│   ├── delete_image.py      # Remove face images
│   └── ...                  # Other API endpoints
│
├── service/                  # Business logic layer
│   ├── face_query_service.py      # Face recognition logic
│   ├── add_embedding_service.py   # Embedding management
│   ├── mysql_service.py           # Database operations
│   └── ...                        # Other services
│
├── db/                       # Database layer
│   ├── mysql_conn.py        # MySQL connection setup
│   ├── models.py            # Database models
│   ├── nguoi_repository.py  # Person data access
│   └── taikhoan_repository.py # Account data access
│
├── model/                    # AI models
│   ├── arcface_model.py     # ArcFace model wrapper
│   ├── *.pth                # Pre-trained model weights
│   └── ...
│
├── index/                    # FAISS vector database
│   ├── faiss.py             # FAISS operations
│   ├── *.index              # FAISS index files
│   └── *.npz                # Metadata storage
│
└── insightface/             # InsightFace source code
    ├── recognition/         # Face recognition models
    ├── detection/           # Face detection
    └── ...                  # Other InsightFace modules
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Git

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd face_api
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure MySQL Database
```sql
CREATE DATABASE face_recognition;
CREATE USER 'face_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON face_recognition.* TO 'face_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 4: Update Configuration
Edit `config.py`:
```python
# MySQL Configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "face_user" 
MYSQL_PASSWORD = "your_password"
MYSQL_DATABASE = "face_recognition"

# Model Configuration
MODEL_PATH = "model/ms1mv3_arcface_r18_fp16.pth"
FAISS_INDEX_PATH = "index/faiss_db_r18.index"
```

### Step 5: Initialize Database
```bash
python db/import_class_info_to_mysql.py
```

### Step 6: Start Server
```bash
cd face_api
python app.py
```

Server will start at `http://localhost:8000`
## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration

### Face Recognition
- `POST /api/face_query` - Query face against database
- `POST /api/face_query_top5` - Get top 5 similar faces
- `POST /api/add_embedding` - Add new face embedding
- `PUT /api/edit_embedding` - Update face data
- `DELETE /api/delete_image` - Remove face image

### Person Management  
- `GET /api/list_nguoi` - List all persons
- `GET /api/get_image_ids_by_class/{class_id}` - Get images for person
- `DELETE /api/delete_class/{class_id}` - Delete person

### System Management
- `GET /api/index_status` - FAISS index status
- `POST /api/reset_index` - Reset FAISS index
- `GET /api/vector_info` - Vector database info

### Example Request
```bash
# Face Query
curl -X POST "http://localhost:8000/api/face_query" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg" \
  -F "threshold=0.5"
```

### Example Response
```json
{
  "similarity": 0.89,
  "person_info": {
    "class_id": "PERSON_001",
    "name": "John Doe",
    "info": "Employee ID: 12345"
  },
  "processing_time": 0.15
}
```

## InsightFace Integration

This system uses InsightFace source code from the `insightface/` directory:

### ArcFace Model
- **Location**: `insightface/recognition/arcface_torch/`
- **Model**: `ms1mv3_arcface_r18_fp16.pth` 
- **Embedding Size**: 512-dimensional vectors
- **Accuracy**: 99.5%+ on standard benchmarks

### Face Detection
- **Detector**: RetinaFace from `insightface/detection/`
- **Features**: Multi-scale detection, face alignment
- **Output**: Face bounding boxes and 5-point landmarks

### Key Components
```python
# Face embedding extraction
from model.arcface_model import ArcFaceModel
model = ArcFaceModel("model/ms1mv3_arcface_r18_fp16.pth")
embedding = model.get_embedding(face_image)
```

## Age/Gender Models

Optional demographic analysis using pre-trained models:

### Age Prediction
- **Model**: `insightface/attribute/age_gender/`
- **Range**: 0-100 years
- **Accuracy**: ±3 years average error

### Gender Classification  
- **Model**: Binary classification (Male/Female)
- **Accuracy**: 95%+ on diverse datasets

### Usage
```python
# Enable age/gender prediction
POST /api/face_query
{
  "include_demographics": true
}
```

## Anti-Spoofing

Liveness detection using DeepFace integration:

### Features
- **Real Face Detection**: Distinguishes live faces from photos/videos
- **Multiple Models**: Support for different anti-spoofing algorithms
- **Graceful Fallback**: System continues working if anti-spoofing fails

### Configuration
```python
# config.py
ENABLE_ANTI_SPOOFING = True
ANTI_SPOOFING_THRESHOLD = 0.7
```

### Implementation
- **Library**: DeepFace with TensorFlow backend
- **Fallback**: If DeepFace unavailable, system warns but continues
- **Performance**: ~100ms additional processing time

## Configuration

### config.py Settings
```python
# Server Configuration
DEBUG = False
HOST = "0.0.0.0"
PORT = 8000

# Model Configuration  
MODEL_NAME = "arcface_r18"
EMBEDDING_SIZE = 512
FACE_SIZE = (112, 112)

# FAISS Configuration
FAISS_INDEX_TYPE = "IndexFlatIP"  # Inner Product
SEARCH_K = 100
MAX_VECTORS = 1000000

# Performance Tuning
BATCH_SIZE = 32
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ASYNC_WORKERS = 4
```

## Troubleshooting

### Common Issues

**1. MySQL Connection Failed**
```bash
# Check MySQL service
net start mysql

# Verify credentials
mysql -u face_user -p face_recognition
```

**2. Model Loading Error**
```bash
# Check model file exists
ls -la model/*.pth

# Verify model path in config.py
```

**3. FAISS Index Issues**
```bash
# Reset index
curl -X POST "http://localhost:8000/api/reset_index"

# Check index status  
curl "http://localhost:8000/api/index_status"
```

**4. DeepFace Import Error**
```bash
# Install TensorFlow
pip install tensorflow>=2.13.0

# Disable anti-spoofing if needed
# Set ENABLE_ANTI_SPOOFING = False in config.py
```

### Performance Optimization

**1. FAISS Configuration**
- Use GPU version: `pip install faiss-gpu`
- Optimize index type for your use case
- Tune search parameters

**2. Model Optimization**
- Use quantized models for faster inference
- Batch processing for multiple faces
- GPU acceleration when available

**3. Database Optimization**
- Index frequently queried columns
- Use connection pooling
- Optimize query patterns

### Logs and Monitoring
```bash
# Check application logs
tail -f logs/app.log

# Monitor system resources
htop

# Check API performance
curl "http://localhost:8000/api/index_status"
```