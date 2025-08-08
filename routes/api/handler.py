from io import BytesIO
from fastapi import HTTPException, UploadFile
import os
import routes.api.utils

async def upload_order_iden(order_file: UploadFile, excel_manager, pdf_manager):
    filename = order_file.filename
    ext = os.path.splitext(filename)[1].lower()
    allowed_exts = {".pdf", ".xlsx"}

    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail="File harus PDF atau XLSX")

    content = await order_file.read()
    file_bytes = BytesIO(content)

    try:
        if ext == ".xlsx":
            order_name, form_data = excel_manager.read_form(file_bytes)
        elif ext == ".pdf":
            order_name, form_data = pdf_manager.read_form(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="File type tidak didukung")

        data = routes.api.utils.upload_order_json(form_data)
        return {"order_name": order_name, "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error proses file: {str(e)}")