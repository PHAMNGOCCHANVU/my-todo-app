# logic.py - Đóng vai trò xử lý nghiệp vụ
# Cần import module để thao tác với dữ liệu

import data
def add_new_task(content):
    #Logic thêm mới: Kiểm tra rỗng trước khi lưu
    clean_content = content.strip()
    if len(clean_content) == 0:
        return False, "Lỗi: Nội dung không được để trống!"
    
    data.save_task(clean_content)
    return True, "Thêm thành công!"
    
def get_formatted_list():
    #Logic lấy dữ liệu: Lấy từ data và đánh số thứ tự
    raw_tasks = data.get_all_tasks()
    if not raw_tasks:
        return "Danh sách trống."
    
    result = ""
    for i, task in enumerate(raw_tasks):
        #Kiểm tra trạng thái để đánh dấu X
        status_icon = "[X]" if task["complete"] else "[ ]"
        #Lấy tên công việc từ key "title"
        result += f"{i + 1}. {status_icon} {task['title']}\n"
    return result

def mark_done(index_str):
    #Logic mới: Đánh dấu đã hoàn thành
    if not index_str.isdigit():
        return False, "Lỗi: Phải nhập số!"
    
    index = int(index_str) - 1
    if data.update_status(index, True):
        return True, "Đã đánh dấu hoàn thành!"
    else:
        return False, "Lỗi: Số thứ tự không tồn tại!"

def delete_task(index_str):
    "Logic xóa: Kiểm tra xem người dùng có nhập số không"
    if not index_str.isdigit():
        return False, "Lỗi. Bạn phải nhập một con số!"
    
    index = int(index_str) - 1
    delete_title = data.remove_task_by_index(index)
    if delete_title:
        return True, f"Đã xóa: {delete_title}"
    else:
        return False, "Lỗi: Số thứ tự không tồn tại!"
    