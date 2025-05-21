import requests
import logging
import json
import os
from huggingface_hub import InferenceClient
from config import MODEL_ID, SYSTEM_PROMPT, HUGGINGFACE_API_KEY, logger

class ModelHandler:
    def __init__(self):
        """
        مدير التعامل مع نموذج اللغة الكبير (LLM) للمساعد القانوني
        """
        self.model_id = MODEL_ID
        self.system_prompt = SYSTEM_PROMPT
        self.api_key = HUGGINGFACE_API_KEY
        self.client = None
        
        # تهيئة العميل
        self.initialize_client()
    
    def initialize_client(self):
        """تهيئة عميل Hugging Face Inference API"""
        try:
            # استخدام InferenceClient من huggingface_hub
            self.client = InferenceClient(
                model=self.model_id,
                token=self.api_key if self.api_key else None
            )
            logger.info(f"تم تهيئة عميل النموذج بنجاح للنموذج: {self.model_id}")
            return True
        except Exception as e:
            logger.error(f"فشل في تهيئة عميل النموذج: {str(e)}")
            return False
    
    def generate_response(self, query, max_tokens=1024, temperature=0.1):
        """
        إنشاء استجابة من النموذج باستخدام الاستعلام المقدم
        
        Args:
            query: نص الاستعلام المقدم من المستخدم
            max_tokens: الحد الأقصى لعدد الرموز في الاستجابة
            temperature: درجة الحرارة للتحكم في إبداعية الاستجابة
            
        Returns:
            نص الاستجابة
        """
        if not self.client:
            if not self.initialize_client():
                return "عذراً، لا يمكن الاتصال بالنموذج في الوقت الحالي. يرجى المحاولة مرة أخرى لاحقاً."
        
        try:
            # تحضير المدخلات للنموذج (يختلف التنسيق حسب النموذج)
            prompt = f"<s>[INST] {self.system_prompt}\n\n{query} [/INST]"
            
            # استدعاء النموذج
            response = self.client.text_generation(
                prompt=prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                repetition_penalty=1.1,
                do_sample=True,
                return_full_text=False
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء إنشاء الاستجابة: {str(e)}")
            
            # محاولة استخدام واجهة برمجة التطبيقات العامة كخطة بديلة
            try:
                logger.info("محاولة استخدام واجهة برمجة تطبيقات Hugging Face العامة كخطة بديلة...")
                
                # استخدام واجهة برمجة تطبيقات Hugging Face العامة
                api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
                headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": max_tokens,
                        "temperature": temperature,
                        "repetition_penalty": 1.1,
                        "do_sample": True,
                        "return_full_text": False
                    }
                }
                
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()  # رفع استثناء في حالة حدوث خطأ
                
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                
                return "عذراً، لم أتمكن من فهم الاستجابة من النموذج."
                
            except Exception as backup_error:
                logger.error(f"فشلت الخطة البديلة أيضاً: {str(backup_error)}")
                
                # في حالة فشل كل الطرق، قدم استجابة معدة مسبقاً
                fallback_responses = {
                    "قانون": "عذراً، لا يمكنني الوصول إلى النموذج اللغوي في الوقت الحالي. للحصول على معلومات قانونية موثوقة، يرجى الرجوع إلى موقع وزارة العدل المصرية أو استشارة محامٍ مختص.",
                    "محكمة": "عذراً، لا يمكنني الوصول إلى النموذج اللغوي في الوقت الحالي. للاستفسار عن إجراءات المحكمة، يرجى زيارة موقع وزارة العدل المصرية أو الاتصال بالمحكمة المختصة.",
                    "دعوى": "عذراً، لا يمكنني الوصول إلى النموذج اللغوي في الوقت الحالي. لمعرفة كيفية رفع دعوى، يرجى استشارة محامٍ أو زيارة موقع وزارة العدل المصرية."
                }
                
                # البحث عن كلمات مفتاحية في الاستعلام
                for keyword, response in fallback_responses.items():
                    if keyword in query.lower():
                        return response
                
                # استجابة افتراضية
                return "عذراً، لا يمكنني الوصول إلى النموذج اللغوي في الوقت الحالي. يرجى المحاولة مرة أخرى لاحقاً، أو البحث عن معلوماتك القانونية من مصادر رسمية موثوقة."
