import json
from pathlib import Path
from typing import Dict, List

import streamlit as st

STATE_FILE = Path("probation_progress.json")

# Đã cập nhật nội dung chuẩn theo bản docs của bạn
SECTIONS: Dict[str, List[str]] = {
    "Key Principles": [
        "1. Đi làm phải enjoy + giao tiếp + làm quen với mọi người",
        "2. Mục tiêu 2 tháng thử việc & 2-3 năm tại Shopee (DS/ AI).",
        "3. Có Plan rõ ràng và bám sát Leader",
        "4. On the Job làm các task thực tế daily như kéo Data, làm Dashboard & support các task khó hơn",
        "5. Chủ động và tạo ra giá trị thực tế",
        "6. Hiểu toàn bộ Data/Dash của team và Impact value của phòng",
        "7. Xin Feedback từ Leader & đồng nghiệp trong các tuần",
        "8. Tìm hiểu business của Shopee/ Partner/ Team để hiểu giá trị công việc",
        "9. Hiểu Impact value của team & phòng Data/ BI",
        "10. Tìm hiểu các chỉ số Fraud & Model thuật toán (nếu có)"
    ],
    "Week 1-2": [
        "Ngày 1-2: Gặp trực tiếp Leader để hỏi rõ mục tiêu 2 tháng Probation",
        "Trình bày mục tiêu bản thân/lộ trình làm Data Consultant với sếp",
        "Xin quyền vào DWH, Data Dictionary, Confluence và các Dashboard team",
        "Học thuộc các dashboard/metrics và luồng dữ liệu đổ vào",
        "Ngày 2-7: Mời đồng nghiệp ăn trưa/trà sữa để làm quen",
        "Nhờ anh/chị chỉ bảng core, database hay dùng và các chỉ số chính",
        "Nắm bắt bức tranh tổng quan và các metrics ít dùng"
    ],
    "Week 2-3": [
        "Nắm bắt 80%-100% DWH/Metrics/Dashboard team hay xài",
        "Xin tips hướng dẫn và feedback từ các anh/chị Senior",
        "Cuối tuần 2/Đầu tuần 3: Xin Going On the Job (kéo số thực tế)",
        "Làm chính các task dễ/ổn định và support các task khó/Advanced"
    ],
    "Week 4": [
        "Bắt đầu chạy Data và duy trì (run daily) cho các Dashboard",
        "Chủ động bám sát kế hoạch để duy trì công việc ổn định"
    ],
    "Week 5-6": [
        "Đảm nhận các task hằng ngày, xin làm chính càng nhiều càng tốt",
        "Tìm hiểu sâu Business Shopee/Partner để hiểu giá trị công việc",
        "Nghiên cứu ROI của team và tác động tới Business/Revenue",
        "Tìm hiểu các chỉ số Fraud & Model thuật toán (nếu có)",
        "Xin feedback sếp để tối ưu hiệu quả cho 2 tuần cuối"
    ],
    "Week 7-8": [
        "Duy trì task và chuẩn bị báo cáo kết quả sau 2 tháng",
        "Họp 1:1 với sếp về kết quả Probation",
        "Thảo luận lộ trình phát triển (Growth) sau Probation",
        "Đăng ký tham gia các project mới hoặc học thêm kỹ năng mới"
    ],
    "Senior DA": [
        "Xây dựng định hướng rõ ràng cho 2-3 năm tới",
        "Nhờ sếp tư vấn các bước để đạt được cấp độ Senior"
    ],
}

def load_saved_state() -> Dict[str, bool]:
    if not STATE_FILE.exists():
        return {}
    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {str(k): bool(v) for k, v in data.items()}
    except (json.JSONDecodeError, OSError):
        pass
    return {}

def save_state(state: Dict[str, bool]) -> None:
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def task_key(section: str, item: str) -> str:
    return f"{section}::{item}"

def initialize_session() -> None:
    if "task_state" not in st.session_state:
        st.session_state.task_state = load_saved_state()

    # Ensure every task has a key in state.
    for section, tasks in SECTIONS.items():
        for item in tasks:
            key = task_key(section, item)
            st.session_state.task_state.setdefault(key, False)

def render_header() -> None:
    st.set_page_config(
        page_title="Shopee Probation Tracker",
        page_icon="🛍️",
        layout="wide",
    )
    
    # CSS Customization cho Vibe Shopee (Màu cam #EE4D2D)
    st.markdown("""
    <style>
    /* Đổi màu chữ tiêu đề chính sang Cam Shopee */
    h1 {
        color: #EE4D2D !important;
        font-weight: 800;
    }
    h2, h3 {
        color: #FF5722 !important;
    }
    /* Đổi màu nút bấm Primary */
    .stButton>button[kind="primary"] {
        background-color: #EE4D2D !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #D73315 !important;
    }
    /* Đổi màu nút bấm Secondary khi hover */
    .stButton>button[kind="secondary"]:hover {
        border-color: #EE4D2D !important;
        color: #EE4D2D !important;
    }
    /* Đổi màu thanh Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #EE4D2D !important;
    }
    /* Đổi màu các Tab đang được chọn */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #EE4D2D !important;
        border-bottom-color: #EE4D2D !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🛍️ Shopee 2-Month Probation Tracker")
    st.caption("Quản lý tiến độ Onboarding và Probation tại Shopee. Quan trọng là luôn follow-up và báo cáo với Leader!")

def render_progress() -> None:
    values = list(st.session_state.task_state.values())
    completed = sum(values)
    total = len(values)
    percent = (completed / total) if total else 0

    st.markdown("### 🚀 Tiến độ tổng quan")
    st.progress(percent)
    st.write(f"**Hoàn thành {completed}/{total} công việc ({percent * 100:.1f}%)**")

def render_sections() -> None:
    tab_names = list(SECTIONS.keys())
    tabs = st.tabs(tab_names)

    for tab, section in zip(tabs, tab_names):
        with tab:
            st.subheader(f"📌 {section}")
            for item in SECTIONS[section]:
                key = task_key(section, item)
                checked = st.checkbox(item, value=st.session_state.task_state[key], key=key)
                st.session_state.task_state[key] = checked

def render_actions() -> None:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Lưu tiến độ (Save Progress)", type="primary", use_container_width=True):
            save_state(st.session_state.task_state)
            st.success("Đã lưu tiến độ thành công!")
    with c2:
        if st.button("Làm mới (Reset All)", use_container_width=True):
            for k in st.session_state.task_state:
                st.session_state.task_state[k] = False
            save_state(st.session_state.task_state)
            st.rerun()

def main() -> None:
    render_header()
    initialize_session()
    render_progress()
    st.divider()
    render_sections()
    st.divider()
    render_actions()

    # Auto-save on every rerun so refresh doesn't lose progress.
    save_state(st.session_state.task_state)

if __name__ == "__main__":
    main()