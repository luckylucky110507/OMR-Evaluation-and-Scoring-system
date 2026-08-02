from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from pathlib import Path
import shutil
import itertools

from backend.schemas import ExamSession, OMRUploadResponse, ProcessingStatusResponse, OMRResultResponse
from config import get_config_dict, create_directories, UPLOAD_DIR

app = FastAPI(title="OMR Evaluation Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_directories()

UPLOAD_DB: Dict[int, Dict[str, Any]] = {}
_id_counter = itertools.count(1)

STATIC_EXAM_SESSIONS = [
    ExamSession(id=1, session_name="Default Session", sheet_version="v1"),
]


def create_demo_result() -> Dict[str, Any]:
    return {
        "score": 78,
        "total_score": 78,
        "total_percentage": 78.0,
        "max_possible_score": 100,
        "subject_scores": [
            {
                "subject_name": "Mathematics",
                "correct_answers": 18,
                "total_questions": 20,
                "score": 18,
                "percentage": 90.0,
            },
            {
                "subject_name": "Physics",
                "correct_answers": 16,
                "total_questions": 20,
                "score": 16,
                "percentage": 80.0,
            },
            {
                "subject_name": "Chemistry",
                "correct_answers": 15,
                "total_questions": 20,
                "score": 15,
                "percentage": 75.0,
            },
            {
                "subject_name": "Biology",
                "correct_answers": 14,
                "total_questions": 20,
                "score": 14,
                "percentage": 70.0,
            },
            {
                "subject_name": "General Knowledge",
                "correct_answers": 13,
                "total_questions": 20,
                "score": 15,
                "percentage": 65.0,
            },
        ],
        "answers": {
            "Q1": "A",
            "Q2": "C",
            "Q3": "B",
            "Q4": "D",
        },
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/config")
def config() -> Dict[str, Any]:
    return get_config_dict()


@app.get("/exam-sessions")
def exam_sessions() -> Any:
    return [session.dict() for session in STATIC_EXAM_SESSIONS]


@app.get("/results/exam-session/{exam_session_id}")
def exam_session_results(exam_session_id: int) -> Any:
    """Return all OMR results for the given exam session."""
    results = []
    for record_id, record in UPLOAD_DB.items():
        if record.get("exam_session_id") == exam_session_id:
            results.append({
                "omr_sheet_id": record_id,
                "student_id": record.get("student_id", ""),
                "status": record.get("status", ""),
                "score": record.get("score", 0),
                "total_score": record.get("total_score", record.get("score", 0)),
                "total_percentage": record.get("total_percentage", 0.0),
                "max_possible_score": record.get("max_possible_score", 0),
                "subject_scores": record.get("subject_scores", []),
            })
    return results


@app.post("/omr/upload")
def omr_upload(
    student_id: str = Form(...),
    exam_session_id: int = Form(...),
    sheet_version: str = Form(...),
    file: UploadFile = File(...),
) -> OMRUploadResponse:
    omr_sheet_id = next(_id_counter)
    filename = f"omr_{omr_sheet_id}_{file.filename}"
    upload_path = Path(UPLOAD_DIR) / filename
    with upload_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    demo_result = create_demo_result()

    UPLOAD_DB[omr_sheet_id] = {
        "student_id": student_id,
        "exam_session_id": exam_session_id,
        "sheet_version": sheet_version,
        "filename": str(upload_path),
        "status": "completed",
        "score": demo_result["score"],
        "total_score": demo_result["total_score"],
        "total_percentage": demo_result["total_percentage"],
        "max_possible_score": demo_result["max_possible_score"],
        "subject_scores": demo_result["subject_scores"],
        "answers": demo_result["answers"],
    }

    return OMRUploadResponse(omr_sheet_id=omr_sheet_id, status="completed")


@app.post("/omr/batch-process")
def omr_batch_process(
    student_ids: List[str] = Form(...),
    exam_session_id: int = Form(...),
    sheet_version: str = Form(...),
    files: List[UploadFile] = File(...),
) -> Dict[str, Any]:
    if len(student_ids) != len(files):
        raise HTTPException(status_code=400, detail="student_ids length must match number of uploaded files")

    omr_sheet_ids: List[int] = []
    for student_id, upload_file in zip(student_ids, files):
        omr_sheet_id = next(_id_counter)
        filename = f"omr_{omr_sheet_id}_{upload_file.filename}"
        upload_path = Path(UPLOAD_DIR) / filename
        with upload_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        demo_result = create_demo_result()
        UPLOAD_DB[omr_sheet_id] = {
            "student_id": student_id,
            "exam_session_id": exam_session_id,
            "sheet_version": sheet_version,
            "filename": str(upload_path),
            "status": "completed",
            "score": demo_result["score"],
            "total_score": demo_result["total_score"],
            "total_percentage": demo_result["total_percentage"],
            "max_possible_score": demo_result["max_possible_score"],
            "subject_scores": demo_result["subject_scores"],
            "answers": demo_result["answers"],
        }
        omr_sheet_ids.append(omr_sheet_id)

    return {"omr_sheet_ids": omr_sheet_ids, "status": "completed"}


@app.get("/omr/{omr_sheet_id}/status")
def omr_status(omr_sheet_id: int) -> ProcessingStatusResponse:
    record = UPLOAD_DB.get(omr_sheet_id)
    if not record:
        return ProcessingStatusResponse(omr_sheet_id=omr_sheet_id, status="not_found")
    return ProcessingStatusResponse(omr_sheet_id=omr_sheet_id, status=record["status"])


@app.get("/omr/{omr_sheet_id}/result")
def omr_result(omr_sheet_id: int) -> OMRResultResponse:
    record = UPLOAD_DB.get(omr_sheet_id)
    if not record:
        return OMRResultResponse(
            omr_sheet_id=omr_sheet_id,
            student_id="",
            status="not_found",
            score=0,
            total_score=0,
            total_percentage=0.0,
            max_possible_score=0,
            subject_scores=[],
            answers={},
        )
    return OMRResultResponse(
        omr_sheet_id=omr_sheet_id,
        student_id=record["student_id"],
        status=record["status"],
        score=record["score"],
        total_score=record.get("total_score", record.get("score", 0)),
        total_percentage=record.get("total_percentage", 0.0),
        max_possible_score=record.get("max_possible_score", 0),
        subject_scores=record.get("subject_scores", []),
        answers=record["answers"],
    )
