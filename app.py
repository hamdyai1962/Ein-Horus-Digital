import streamlit as st
import os
import json
import time
from datetime import datetime

# استيراد الوحدات الخاصة بالمشروع
from config import APP_TITLE, APP_DESCRIPTION, APP_ICON, APP_VERSION, logger
from model_handler import ModelHandler
from legal_data import LegalDataHandler

# التأكد من وجود مجلدات المشروع
os.makedirs("data", exist_ok=True)

# تهيئة مديري البيانات والنموذج
legal_data = LegalDataHandler()

# ضبط تكوين الصفحة
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# أنماط CSS مخصصة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif !important;
    }
    
    .main-header {
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 20px;
    }
    
    .subheader {
        text-align: center;
        color: #4b5563;
        margin-bottom: 30px;
    }
    
    .stTextInput, .stTextArea {
        direction: rtl;
    }
    
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-right: 5px solid #1976d2;
    }
    
    .bot-message {
        background-color: #f1f8e9;
        border-right: 5px solid #7cb342;
    }
    
    .info-box {
        background-color: #fff3e0;
        border: 1px solid #ffe0b2;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .footer {
        text-align: center;
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid #e5e7eb;
        color: #6b7280;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# الدالة الرئيسية للتطبيق
def main():
    # الشريط الجانبي
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/eye-of-horus.png", width=100)
        st.markdown(f"<h2 style='text-align: center;'>عين حورس الرقمية</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>المساعد القانوني المصري الذكي</p>", unsafe_allow_html=True)
        
        st.markdown("### القائمة الرئيسية")
        page = st.radio("اختر الصفحة:", ["المساعد القانوني", "قاعدة المعرفة القانونية", "حول المشروع"])
        
        st.markdown("---")
        
        # قسم الإعدادات
        st.markdown("### إعدادات المساعد القانوني")
        max_tokens = st.slider("الحد الأقصى لطول الإجابة:", 256, 4096, 1024, 256)
        temperature = st.slider("درجة الإبداعية:", 0.0, 1.0, 0.1, 0.1)
        
        # تخزين الإعدادات في جلسة المستخدم
        st.session_state['max_tokens'] = max_tokens
        st.session_state['temperature'] = temperature
        
        st.markdown("---")
        
        # معلومات المشروع
        st.markdown("### معلومات المشروع")
        st.markdown(f"**الإصدار:** {APP_VERSION}")
        st.markdown(f"**تاريخ الإنشاء:** {datetime.now().strftime('%Y-%m-%d')}")
    
    # العنوان الرئيسي
    st.markdown(f"<h1 class='main-header'>{APP_TITLE}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subheader'>{APP_DESCRIPTION}</p>", unsafe_allow_html=True)
    
    # عرض الصفحة المختارة
    if page == "المساعد القانوني":
        show_legal_assistant()
    elif page == "قاعدة المعرفة القانونية":
        show_legal_database()
    elif page == "حول المشروع":
        show_about_page()
    
    # تذييل الصفحة
    st.markdown("<div class='footer'>© 2025 عين حورس الرقمية - جميع الحقوق محفوظة</div>", unsafe_allow_html=True)

def show_legal_assistant():
    """عرض واجهة المساعد القانوني"""
    st.markdown("## المساعد القانوني")
    
    st.markdown(
        """
        <div class="info-box">
            أهلاً بك في المساعد القانوني! يمكنك طرح أي سؤال قانوني يتعلق بالقوانين المصرية، 
            وسأحاول مساعدتك بأفضل ما لدي من معلومات.
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # تهيئة جلسة المحادثة إذا لم تكن موجودة
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    # تهيئة مدير النموذج عند الحاجة
    if 'model_handler' not in st.session_state:
        with st.spinner("جاري تهيئة المساعد القانوني..."):
            st.session_state['model_handler'] = ModelHandler()
    
    # عرض سجل المحادثة
    for message in st.session_state['messages']:
        if message['role'] == 'user':
            st.markdown(
                f"""
                <div class="chat-message user-message">
                    <b>أنت:</b> {message['content']}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="chat-message bot-message">
                    <b>عين حورس:</b> {message['content']}
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    # مربع إدخال الاستعلام القانوني
    prompt = st.text_area("اكتب استعلامك القانوني هنا:", height=120, max_chars=2000)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        submit_button = st.button("إرسال", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("مسح المحادثة", use_container_width=True)
    
    # معالجة الاستعلام عند النقر على زر الإرسال
    if submit_button and prompt:
        # إضافة استعلام المستخدم إلى سجل المحادثة
        st.session_state['messages'].append({'role': 'user', 'content': prompt})
        
        # عرض الاستعلام الحالي
        st.markdown(
            f"""
            <div class="chat-message user-message">
                <b>أنت:</b> {prompt}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # الحصول على إجابة النموذج
        with st.spinner("جاري معالجة استعلامك..."):
            try:
                # استخدام النموذج للحصول على إجابة
                response = st.session_state['model_handler'].generate_response(
                    query=prompt,
                    max_tokens=st.session_state.get('max_tokens', 1024),
                    temperature=st.session_state.get('temperature', 0.1)
                )
                
                # إضافة إجابة النموذج إلى سجل المحادثة
                st.session_state['messages'].append({'role': 'assistant', 'content': response})
                
                # عرض الإجابة
                st.markdown(
                    f"""
                    <div class="chat-message bot-message">
                        <b>عين حورس:</b> {response}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                error_message = f"عذراً، حدث خطأ أثناء معالجة استعلامك: {str(e)}"
                st.error(error_message)
                st.session_state['messages'].append({'role': 'assistant', 'content': error_message})
        
        # إعادة تشغيل التطبيق لتحديث العرض
        st.experimental_rerun()
    
    # مسح المحادثة عند النقر على زر المسح
    if clear_button:
        st.session_state['messages'] = []
        st.experimental_rerun()

def show_legal_database():
    """عرض قاعدة المعرفة القانونية"""
    st.markdown("## قاعدة المعرفة القانونية")
    
    st.markdown(
        """
        <div class="info-box">
            تحتوي هذه الصفحة على قاعدة معرفية من القوانين والتشريعات المصرية.
            يمكنك البحث واستعراض مختلف القوانين والمواد القانونية.
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # البحث في القوانين
    search_query = st.text_input("البحث في القوانين:", placeholder="اكتب كلمة للبحث...")
    
    if search_query:
        search_results = legal_data.search_laws(search_query)
        if search_results:
            st.success(f"تم العثور على {len(search_results)} نتيجة.")
            for i, law in enumerate(search_results):
                with st.expander(f"{law['title']} - {law['law_number']}/{law['year']}"):
                    st.markdown(f"**رقم القانون:** {law['law_number']}")
                    st.markdown(f"**السنة:** {law['year']}")
                    st.markdown(f"**الوصف:** {law['description']}")
                    st.markdown(f"**ملخص:** {law['summary']}")
        else:
            st.warning("لم يتم العثور على نتائج مطابقة.")
    
    # عرض جميع القوانين
    st.markdown("### القوانين المصرية")
    
    laws = legal_data.get_all_laws()
    for i, law in enumerate(laws):
        with st.expander(f"{law['title']} - {law['law_number']}/{law['year']}"):
            st.markdown(f"**رقم القانون:** {law['law_number']}")
            st.markdown(f"**السنة:** {law['year']}")
            st.markdown(f"**الوصف:** {law['description']}")
            st.markdown(f"**ملخص:** {law['summary']}")

def show_about_page():
    """عرض صفحة حول المشروع"""
    st.markdown("## حول مشروع عين حورس الرقمية")
    
    st.markdown(
        """
        ### ما هو عين حورس الرقمية؟
        
        عين حورس الرقمية هو مساعد قانوني ذكي متخصص في القوانين والتشريعات المصرية. 
        يهدف المشروع إلى جعل المعرفة القانونية متاحة للجميع بطريقة سهلة وبسيطة.
        
        ### المميزات الرئيسية:
        
        - **المساعد القانوني الذكي**: الإجابة على الاستفسارات القانونية بدقة عالية باستخدام نماذج الذكاء الاصطناعي.
        - **قاعدة معرفية شاملة**: قاعدة بيانات تضم القوانين والتشريعات المصرية مع تحديثات دورية.
        - **واجهة سهلة الاستخدام**: تصميم بسيط وسهل الاستخدام يناسب جميع المستخدمين.
        - **مفتوح المصدر**: المشروع مفتوح المصدر بالكامل، مما يسمح للمجتمع بالمساهمة في تطويره.
        
        ### التقنيات المستخدمة:
        
        - نماذج اللغات الكبيرة من Hugging Face
        - Python و Streamlit لواجهة المستخدم
        - تقنيات معالجة اللغة الطبيعية (NLP)
        
        ### إخلاء المسؤولية:
        
        المعلومات المقدمة من خلال "عين حورس الرقمية" هي لأغراض إعلامية فقط ولا يجب اعتبارها استشارة قانونية رسمية.
        يرجى الرجوع دائمًا إلى محامٍ مؤهل للحصول على المشورة القانونية.
        """
    )

# تشغيل التطبيق
if __name__ == "__main__":
    main()
