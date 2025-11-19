from google import genai
from google.genai.types import GenerateContentConfig

client = genai.Client(api_key="AIzaSyBRI34bmdhGKLN_loRSnxRaS32C3fFcYns")

prompt = """
คุณคือผู้เชี่ยวชาญด้านการตลาด
ช่วยสร้างไอเดียแคมเปญสำหรับแบรนด์ F&B
ให้เหมาะกับกลุ่มเป้าหมาย Gen Z
และให้ออกมาเป็นข้อความแบบละเอียด
"""

config = GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=2500  # เพิ่มเพื่อป้องกัน MAX_TOKENS
)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    if response.text:
        print("=== LLM Response ===\n")
        print(response.text)
    else:
        print("--- ไม่พบข้อความ (Content Filter หรือ Stop Reason) ---")
        if response.candidates:
            print("Stop Reason:", response.candidates[0].finish_reason.name)

except Exception as e:
    print("เกิดข้อผิดพลาด:", str(e))

