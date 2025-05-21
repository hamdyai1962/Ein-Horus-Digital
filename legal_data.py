import json
import os
import logging
from config import SAMPLE_LAWS, logger

class LegalDataHandler:
    def __init__(self,

Copy
# إنشاء ملف legal_data.py للتعامل مع البيانات القانونية
 = @"
import json
import os
import logging
from config import SAMPLE_LAWS, logger

class LegalDataHandler:
    def __init__(self, data_dir='data'):
        """
        مدير التعامل مع البيانات القانونية
        
        Args:
            data_dir: مجلد لتخزين البيانات القانونية
        """
        self.data_dir = data_dir
        self.laws = SAMPLE_LAWS
        
        # التأكد من وجود مجلد البيانات
        os.makedirs(data_dir, exist_ok=True)
    
    def get_all_laws(self):
        """
        الحصول على جميع القوانين المتاحة
        
        Returns:
            قائمة بجميع القوانين
        """
        return self.laws
    
    def get_law_by_id(self, law_index):
        """
        الحصول على قانون محدد بواسطة فهرسه
        
        Args:
            law_index: فهرس القانون (0-based)
            
        Returns:
            بيانات القانون أو None إذا كان الفهرس غير صالح
        """
        try:
            return self.laws[law_index]
        except (IndexError, ValueError):
            logger.error(f"فهرس القانون غير صالح: {law_index}")
            return None
    
    def search_laws(self, query):
        """
        البحث في القوانين باستخدام استعلام نصي
        
        Args:
            query: نص الاستعلام للبحث
            
        Returns:
            قائمة بالقوانين المطابقة
        """
        if not query:
            return []
            
        query = query.lower()
        results = []
        
        for law in self.laws:
            # البحث في العنوان والوصف
            if (query in law['title'].lower() or 
                query in law['description'].lower() or
                query in law['law_number'].lower() or
                query in law['year'].lower() or
                query in law['summary'].lower()):
                results.append(law)
                
        return results
