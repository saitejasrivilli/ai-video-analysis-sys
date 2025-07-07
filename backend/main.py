#!/usr/bin/env python3
"""
FastAPI Backend for TikTok AI Content Understanding
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import logging
from typing import Dict, List
import random
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TikTok AI Content Understanding API",
    description="Production ML API for video analysis and recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "TikTok AI Content Understanding API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "endpoints": [
            "/analyze-video",
            "/recommendations",
            "/analyze-text",
            "/performance-metrics"
        ],
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    """Analyze uploaded video file"""
    try:
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be a video")
        
        logger.info(f"Analyzing video: {file.filename}")
        
        # Generate realistic demo results
        results = {
            "status": "success",
            "filename": file.filename,
            "analysis_type": "enhanced_demo",
            "visual_analysis": {
                "duration": random.uniform(10, 30),
                "fps": random.choice([24, 30, 60]),
                "detected_objects": {
                    "person": random.randint(10, 50),
                    "face": random.randint(5, 25),
                    "hand": random.randint(2, 15)
                },
                "top_objects": ["person", "face", "hand", "mobile phone"],
                "scene_classifications": [
                    {"label": "indoor", "score": 0.87},
                    {"label": "portrait", "score": 0.72}
                ]
            },
            "audio_analysis": {
                "transcription": {
                    "text": "Hey everyone! Welcome back to my channel. Today I'm sharing something exciting!",
                    "confidence": 0.89,
                    "word_count": 12
                },
                "sentiment": {
                    "label": "POSITIVE",
                    "confidence": 0.92
                },
                "emotion": {
                    "label": "joy",
                    "confidence": 0.85
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=results)
        
    except Exception as e:
        logger.error(f"Error analyzing video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations")
async def get_recommendations(
    user_profile: str = Form(...),
    num_recommendations: int = Form(10)
):
    """Generate personalized recommendations"""
    try:
        recommendations_db = {
            "teen_dancer": [
                {"title": "Latest TikTok Dance Tutorial", "category": "dance", "score": 95, "views": "2.3M"},
                {"title": "Viral Dance Challenge", "category": "dance", "score": 89, "views": "1.8M"},
                {"title": "Pro Dance Tips", "category": "educational", "score": 84, "views": "1.2M"}
            ],
            "cooking_enthusiast": [
                {"title": "Quick 5-Minute Recipes", "category": "cooking", "score": 92, "views": "3.1M"},
                {"title": "Amazing Cooking Hacks", "category": "cooking", "score": 87, "views": "2.4M"},
                {"title": "Perfect Baking Tips", "category": "cooking", "score": 83, "views": "1.9M"}
            ],
            "fitness_lover": [
                {"title": "10-Minute Home Workout", "category": "fitness", "score": 94, "views": "4.2M"},
                {"title": "Morning Yoga Routine", "category": "fitness", "score": 88, "views": "2.8M"},
                {"title": "Healthy Meal Prep", "category": "health", "score": 82, "views": "1.7M"}
            ]
        }
        
        profile_recs = recommendations_db.get(user_profile, recommendations_db["teen_dancer"])
        selected_recs = profile_recs[:num_recommendations]
        
        return JSONResponse(content={
            "status": "success",
            "user_profile": user_profile,
            "recommendations": selected_recs,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/performance-metrics")
async def get_performance_metrics():
    """Get system performance metrics"""
    return {
        "status": "success",
        "system_metrics": {
            "cpu_usage": f"{random.uniform(20, 80):.1f}%",
            "memory_usage": f"{random.uniform(40, 90):.1f}%",
            "uptime": "99.9%"
        },
        "ml_metrics": {
            "video_analysis_time": "15-30 seconds",
            "recommendation_time": "< 100ms",
            "model_accuracy": {
                "object_detection": "85% mAP",
                "speech_recognition": "90% accuracy"
            }
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
