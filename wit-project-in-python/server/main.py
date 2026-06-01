from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse  # נדרש להזרמת קבצי תמונה
from server.analyzer import analyze_code_quality
from server.visualizer import generate_three_graphs_report  # ייבוא פונקציית שלושת הגרפים

app = FastAPI(title="CodeGuard - Code Analysis System")


@app.get("/")
def home():
    return {"message": "Welcome to CodeGuard CI Server! The system is running."}


@app.post("/alerts")
async def get_alerts(file: UploadFile = File(...)):
    """
    נתיב שמקבל קובץ פייתון בבקשת POST ומחזיר את רשימת האזהרות שלו
    """
    contents = await file.read()
    file_content_str = contents.decode("utf-8")

    analysis_result = analyze_code_quality(file_content_str)

    if "error" in analysis_result:
        return {
            "file_name": file.filename,
            "status": "syntax_error",
            "error": analysis_result["error"],
            "alerts": []
        }

    return {
        "file_name": file.filename,
        "status": "success",
        "alerts": analysis_result["alerts"]
    }


@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    """
    נתיב שמנתח את קובץ הפייתון ומחזיר תמונה מרוכזת של 3 גרפים ויזואליים
    """
    contents = await file.read()
    file_content_str = contents.decode("utf-8")

    analysis_result = analyze_code_quality(file_content_str)

    if "error" in analysis_result:
        return {"error": f"Cannot generate graphs due to syntax error: {analysis_result['error']}"}

    alerts_list = analysis_result["alerts"]
    issues_summary = {
        "Function Length": sum(1 for a in alerts_list if "too long" in a),
        "Missing Docstring": sum(1 for a in alerts_list if "missing a docstring" in a),
        "Unused Variable": sum(1 for a in alerts_list if "never used" in a),
    }

    image_buffer = generate_three_graphs_report(
        filename=file.filename,
        functions=analysis_result["functions"],
        issues_summary=issues_summary
    )

    return StreamingResponse(image_buffer, media_type="image/png")