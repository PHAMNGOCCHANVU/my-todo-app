# api.py - Đóng vai trò là Web Server (thay thế cho main.py)
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
import data # Tái sử dụng module data cũ
# Chúng ta tạm thời goi thẳng data để đơn giản hóa, hoặc có thể gọi qua logic 
# nếu muốn validate kỹ hơn

app = FastAPI()

# --- CẤU HÌNH CORS (GIẤY PHÉP THÔNG HÀNH) ---
# Cho phép tất cả các trang web khác gọi vào API này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------------

# Định nghĩa khuôn mẫu dữ liệu gửi lên (để thay thế input)
class TaskInput(BaseModel):
    title: str

# 1. API lấy danh sách (Giống chức năng 1)
# Khi truy vấn đường dẫn http://localhost:8000/tasks
@app.get("/tasks")
def read_tasks():
    return data.get_all_tasks()

# 2. API thêm mới (Giống chức năng 2)
@app.post("/tasks")
def create_task(task: TaskInput):
    # Hàm save_task bây giờ trả về object có cả ID
    new_task = data.save_task(task.title)
    return {"message": "Thêm thành công", "task": new_task}

# 3. API xóa (Giống chức năng 4)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    data.remove_task_by_id(task_id) # Gọi hàm mới bên data 
    return {"message": "Đã xóa"}

if __name__ == "__main__":
    import uvicorn
    import os
    # Lấy port từ biến môi trường của server, nếu không có thì dùng 8000
    port = int(os.environ.get("PORT", 8000))
    # host="0.0.0.0" là bắt buộc để chạy trên server cloud
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)

