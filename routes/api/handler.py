from io import BytesIO
from fastapi import HTTPException, UploadFile
import os
import json

def upload_order_json(form_data):
    results = []
    for row_info in form_data:
        result = {}
        for key, value in row_info.items():
            parsed_key = json.loads(key)
            field_type = parsed_key.get("type")
            field_id = parsed_key.get("id")
            
            if field_type == "text":
                result[field_id] = value
            elif field_type == "checkbox":
                result.setdefault("checkbox", []).append(field_id)

        results.append(result)
    return results

async def upload_order_iden(order_file: UploadFile, excel_order_manager, pdf_order_manager):
    filename = order_file.filename
    ext = os.path.splitext(filename)[1].lower()
    allowed_exts = {".pdf", ".xlsx"}

    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail="File harus PDF atau XLSX")

    content = await order_file.read()
    file_bytes = BytesIO(content)

    try:
        if ext == ".xlsx":
            order_name, form_data = excel_order_manager.read_form(file_bytes)
        elif ext == ".pdf":
            order_name, form_data = pdf_order_manager.read_form(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="File type tidak didukung")

        data = upload_order_json(form_data)
        return {"order_name": order_name, "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error proses file: {str(e)}")