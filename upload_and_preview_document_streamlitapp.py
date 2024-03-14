import streamlit as st
import fitz  # PyMuPDF
import streamlit as st
st.set_page_config(layout="wide")
custom_css = """
    <style>
        .stApp {
            max-width: 100%;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
# Khởi tạo session state cho danh sách file đã upload nếu chưa có
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

def upload_file(uploaded_file):
    if uploaded_file is not None:
        # Kiểm tra xem file đã tồn tại trong danh sách chưa để tránh nhân đôi
        if not any(f.name == uploaded_file.name for f in st.session_state['uploaded_files']):
            st.session_state['uploaded_files'].append(uploaded_file)

def display_file(file):
    # Xử lý và hiển thị file dựa trên loại file
    file_type = file.type.split('/')[1]
    if file_type == "pdf":
        try:
            doc = fitz.open(stream=file.getvalue(), filetype="pdf")
            page = doc.load_page(0)  # Chỉ hiển thị trang đầu tiên của PDF
            pix = page.get_pixmap()
            img = pix.tobytes("png")
            st.image(img)
        except Exception as e:
            st.error(f"Could not load PDF file: {e}")
    elif file_type in ["jpeg", "png", "jpg"]:
        st.image(file.getvalue())
    else:
        st.error("File format not supported.")

# Sidebar với navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home", "Upload document", "Dashboard"))

if page == "Home":
    st.title("Home Page")
    st.write("Welcome to the Home Page!")

elif page == "Upload document":
    st.title("Upload and Preview Document")
    # Điều chỉnh tỷ lệ cột, ví dụ: cột upload nhỏ hơn, cột preview lớn hơn
    upload_col, preview_col = st.columns([2, 3])  # Thay đổi tỷ lệ cột ở đây

    with upload_col:
        st.header("Upload Files")
        uploaded_file = st.file_uploader("", type=["pdf", "jpeg", "png", "jpg"], help="Upload your file here")
        if uploaded_file is not None:
            upload_file(uploaded_file)

        if st.session_state['uploaded_files']:
            file_names = [f.name for f in st.session_state['uploaded_files']]
            selected_file_name = st.selectbox("Choose a file to preview", file_names, key="file_selector")

    with preview_col:
        st.header("Preview")
        if 'uploaded_files' in st.session_state and st.session_state['uploaded_files']:
            # Tìm file đã chọn để hiển thị
            for uploaded_file in st.session_state['uploaded_files']:
                if uploaded_file.name == st.session_state['file_selector']:
                    display_file(uploaded_file)
                    break
elif page == "Dashboard":
    st.title("Dashboard")
    st.write("Dashboard content will be here.")
