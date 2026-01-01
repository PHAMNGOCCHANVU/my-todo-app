# data.py - Phiên bản ORM (SQLAlchemy)
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. CẤU HÌNH KẾT NỐI
DB_FILE = "sqlite:///tasks.db" 
engine = create_engine(DB_FILE, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 2. ĐỊNH NGHĨA MODEL (Dữ liệu được coi là Class, không phải là Table)
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)

# Tự động tạo bảng dựa trên Class Task ở trên (không cần viết CREATE TABLE)
Base.metadata.create_all(bind=engine)

# --- CÁC HÀM GIAO TIẾP (PUBLIC) ---

def get_db():
    # Hàm phụ trợ để lấy phiên làm việc (Session)
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_all_tasks():
    db = get_db()
    # ORM: Thay vì "SELECT *", ta dùng db.query(Task).all()
    tasks = db.query(Task).all()
    return tasks
    # SQLAlchemy tự trả về list các Object, api.py sẽ tự hiểu

def save_task(title_text):
    db = get_db()
    # ORM: Tạo một object Python mới
    new_task = Task(title=title_text, completed=False)

    db.add(new_task) # Thêm vào phiên làm việc
    db.commit() # Lưu xuống DB (tương đương INSERT)
    db.refresh(new_task) # Lấy lại ID vửa tạo
    return new_task

def remove_task_by_id(task_id):
    db = get_db()
    # Tìm task theo ID
    task_to_delete = db.query(Task).filter(Task.id == task_id).first()

    if task_to_delete:
        db.delete(task_to_delete)
        db.commit() # Lưu thay đổi (tương đương DELETE)
        return True
    return False

def update_status(task_id, is_completed):
    db = get_db()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = is_completed
        db.commit() # SQLAlchemy tự biết update dòng nào thay đổi 
        return True
    return False
