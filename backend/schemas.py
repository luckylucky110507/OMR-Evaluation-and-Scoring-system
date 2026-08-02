from pydantic import BaseModel
from typing import Dict, Any

class StudentCreate(BaseModel):
    student_id: str
    name: str

class ExamResultResponse(BaseModel):
    id: int
    student_id: str
    score: int
    status: str

class ExamSession(BaseModel):
    id: int
    session_name: str
    sheet_version: str

class OMRUploadResponse(BaseModel):
    omr_sheet_id: int
    status: str

class ProcessingStatusResponse(BaseModel):
    omr_sheet_id: int
    status: str

class OMRResultResponse(BaseModel):
    omr_sheet_id: int
    student_id: str
    status: str
    score: int
    total_score: int
    total_percentage: float
    max_possible_score: int
    subject_scores: list
    answers: Dict[str, Any]
