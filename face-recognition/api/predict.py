
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from service.predict_service import predict_service

predict_router = APIRouter()

@predict_router.post(
	'/predict',
	summary="Dự đoán tuổi và giới tính từ ảnh khuôn mặt",
	description="""
	**Dự đoán tuổi và giới tính từ ảnh tải lên**
	- Nhận ảnh khuôn mặt từ người dùng
	- Trả về tuổi và giới tính dự đoán
	- Hỗ trợ JPG, PNG, JPEG
	""",
	response_description="Kết quả dự đoán tuổi và giới tính",
	tags=["🧑‍🦱 Dự đoán tuổi & giới tính"]
)
async def predict_face(
	image: UploadFile = File(
		..., 
		description="File ảnh khuôn mặt (JPG, PNG, JPEG)",
		media_type="image/*"
	)
):
	result = await predict_service(image)
	status_code = result.get("status_code", 200)
	if "status_code" in result:
		result = {k: v for k, v in result.items() if k != "status_code"}
	return JSONResponse(content=result, status_code=status_code)
