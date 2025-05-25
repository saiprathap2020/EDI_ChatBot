# fastapi_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import importlib # To dynamically import modules
import traceback # For detailed error logging

app = FastAPI(
    title="EDI Segment Explanation API",
    description="Provides explanations for EDI segments based on standard, message type, and version.",
    version="1.0.0"
)

# --- Pydantic Model for Request Body ---
class SegmentRequest(BaseModel):
    segment: str      # e.g., "BGM", "NAD+SE"
    standard: str     # e.g., "EDIFACT", "X12"
    message_type: str # e.g., "DELFOR", "830"
    version: str      # e.g., "D04A", "" (can be empty for X12)

# --- Helper function to get the correct module and call explain_segment ---
def get_explanation_from_module(standard: str, message_type: str, version: str, segment_code: str) -> str:
    """
    Dynamically loads the appropriate EDI explainer module and calls its
    explain_segment function.
    """
    module_name_base = ""
    explanation_not_found_message = f"No explanation found for segment '{segment_code}' in {standard} {message_type} {version}."

    # Construct module name based on standard, message_type, and version
    if standard == "EDIFACT":
        # Assuming filenames like: delfor_d04a.py, desadv_d96a.py
        module_name_base = f"{message_type.lower()}_{version.lower()}" if version else message_type.lower()
    elif standard == "X12":
        # Assuming filenames like: 830.py (or _830.py if that's your convention)
        module_name_base = f"{message_type.lower()}" 
        # If your X12 files are named like _830.py, adjust here:
        # module_name_base = f"_{message_type.lower()}" 
    else:
        return "Unsupported EDI standard."

    if not module_name_base:
        return "Could not determine module name base from input."

    try:
        # Ensure this path matches your directory structure: edi_explainers/edifacts/your_module.py
        module_path = f"edi_explainers.edifact.{module_name_base}"
        
        # --- DEBUGGING PRINTS ---
        print(f"DEBUG: Standard='{standard}', MessageType='{message_type}', Version='{version}'")
        print(f"DEBUG: Constructed module_name_base: '{module_name_base}'")
        print(f"DEBUG: Attempting to import module_path: '{module_path}'")
        # --- END DEBUGGING PRINTS ---

        edi_module = importlib.import_module(module_path)

        if hasattr(edi_module, 'explain_segment') and callable(getattr(edi_module, 'explain_segment')):
            print(f"Calling explain_segment in {module_path} for segment '{segment_code}'")
            explanation = edi_module.explain_segment(segment_code)
            return explanation if explanation else explanation_not_found_message
        else:
            error_msg = f"Module '{module_path}' does not have a callable 'explain_segment' function."
            print(error_msg)
            return error_msg

    except ImportError as e:
        error_msg = (f"Could not import EDI explainer module: '{module_path}'. "
                     f"Ensure the file exists and is correctly named (e.g., '{module_name_base}.py'). "
                     f"Also check that 'edi_explainers' and 'edifacts' are valid packages "
                     f"(i.e., they contain an __init__.py file). Import error: {e}")
        print(error_msg)
        traceback.print_exc() # Print full traceback for ImportError
        return error_msg
    except Exception as e:
        error_msg = f"An error occurred while processing segment '{segment_code}' with module '{module_path}': {e}"
        print(error_msg)
        traceback.print_exc()
        return "An internal error occurred while fetching the explanation."


# --- API Endpoint ---
@app.post("/explain_segment/", summary="Explain an EDI Segment")
async def explain_edi_segment(request: SegmentRequest):
    """
    Receives an EDI segment, standard, message type, and version,
    then returns an explanation for that segment based on local data modules.
    """
    print(f"Received request: {request.dict()}")
    segment_code = request.segment.upper() 
    standard = request.standard.upper()
    message_type = request.message_type.upper()
    version = request.version.upper() if request.version else ""

    explanation = get_explanation_from_module(standard, message_type, version, segment_code)

    return {"segment": request.segment, "explanation": explanation}


if __name__ == "__main__":
    import uvicorn
    # This allows running the FastAPI app directly for testing:
    # In your terminal, navigate to the directory containing this file and run:
    # uvicorn fastapi_app:app --reload 
    # (Replace fastapi_app with the actual name of this Python file if different)
    uvicorn.run(app, host="0.0.0.0", port=8000)
