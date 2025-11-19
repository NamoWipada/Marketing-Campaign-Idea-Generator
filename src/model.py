# src/model.py
from google import genai
from google.genai.types import GenerateContentConfig

# ==============================
# ใช้ API Key ของคุณตรงนี้
# ==============================
client = genai.Client(api_key="AIzaSyBRI34bmdhGKLN_loRSnxRaS32C3fFcYns")

class GeminiFlashCampaignGenerator:
    def __init__(self):
        self.client = client
        self.model_name = "gemini-2.5-flash"  # เลือกโมเดลตามงาน

    def _build_prompt(self, parameters: dict) -> str:
        industry = parameters.get("industry")
        campaign_objective = parameters.get("campaign_objective")
        target_audience = parameters.get("target_audience")
        budget_range = parameters.get("budget_range")
        channels = ", ".join(parameters.get("channels_preference", []))
        mood_tone = parameters.get("mood_tone", "Not specified")
        topic = parameters.get("topic", "Not specified")

        # prompt = (
        #     f"You are a Senior Marketing Strategist.\n"
        #     f"Generate a full marketing campaign blueprint based on the following user input:\n\n"
        #     f"Industry: {industry}\n"
        #     f"Campaign Objective: {campaign_objective}\n"
        #     f"Target Audience: {target_audience}\n"
        #     f"Budget Range: {budget_range}\n"
        #     f"Channels: {channels}\n"
        #     f"Mood & Tone: {mood_tone}\n"
        #     f"Topic: {topic}\n\n"
        #     "Provide detailed sections: Executive Summary, Business Objective, Target Audience + Persona, "
        #     "Customer Insight, Big Idea, Creative Executions, Media Strategy, KPI & Measurement, "
        #     "Campaign Phases / Roadmap, Risk & Mitigation."
        # )
        # return prompt
        prompt = (
            f"คุณคือผู้เชี่ยวชาญด้านการตลาด\n"
            f"โปรดสร้างแผนแคมเปญการตลาดแบบเต็มรูปแบบสำหรับ '{topic}' "
            f"โดยมุ่งเน้น {campaign_objective} กับกลุ่มเป้าหมาย {target_audience} "
            f"ด้วยงบประมาณ {budget_range} และช่องทาง {channels} "
            f"โดยให้โทนและอารมณ์ {mood_tone}\n\n"
            "ผลลัพธ์ควรออกมาเป็น Campaign Blueprint ภาษาไทย กระชับ และจัดเป็นหัวข้อ ดังนี้:\n"
            "## 1. Campaign Snapshot\n"
            "- Campaign Name\n"
            "- Big Idea / Concept\n"
            "- Primary Objective\n"
            "- Target Audience / Persona\n"
            "- Customer Insight\n\n"
            "## 2. Big Idea & Concept Development\n"
            "## 3. Creative Execution & Content\n"
            "## 4. Media & Channel Strategy\n"
            "## 5. KPI Tracking & Analytics\n"
            "## 6. Phase / Roadmap\n"
            "## 7. Risk & Mitigation\n"
            "## 8. Summary & Next Steps\n"
            "## (I) Why This Will Work? – เหตุผลเชิงตรรกะ + ข้อมูลอ้างอิง\n\n"
            "โปรดตอบสั้น กระชับ ใช้ภาษาไทยและจัดเรียงตามหัวข้ออย่างชัดเจน"
        )
        return prompt
        

    def generate_campaign(self, parameters: dict, max_output_tokens: int = 2500) -> str:
        prompt = self._build_prompt(parameters)
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=max_output_tokens
                )
            )

            if response.text:
                return response.text
            else:
                # ถ้ามี Stop Reason หรือถูก Content Filter
                if response.candidates:
                    candidate = response.candidates[0]
                    return f"--- ไม่พบข้อความ (Stop Reason: {candidate.finish_reason.name}) ---"
                return "No response generated."

        except Exception as e:
            return f"เกิดข้อผิดพลาด: {str(e)}"


# ==============================
# ทดสอบโมดูลแบบ standalone
# ==============================
# if __name__ == "__main__":
    # sample_input = {
    #     "industry": "F&B",
    #     "campaign_objective": "Brand Engagement",
    #     "target_audience": "Gen Z",
    #     "budget_range": "High",
    #     "channels_preference": ["Social", "Mobile"],
    #     "mood_tone": "Playful, vibrant, colorful",
    #     "topic": "Cold Brew Summer Festival"
    # }

#     generator = GeminiFlashCampaignGenerator()
#     output = generator.generate_campaign(sample_input)

#     print("=== Marketing Campaign Blueprint ===\n")
#     print(output)
