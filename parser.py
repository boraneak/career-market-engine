import json
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)


def parse_markdown_to_jobs(text):
    """
    Parses markdown text into a list of job dicts using Groq.
    This function is PURE MEMORY. No files allowed.
    """
    if not text:
        return []

    try:
        # 8k chars stays safe under 12k token Groq TPM limit
        content_chunk = text[:8000]
        prompt = """
        SYSTEM: You are a high-precision Data Extractor.
        USER: Extract the first 20 REAL jobs from the Markdown table into JSON.
        RULES: 1. Valid JSON object. 2. Ignore 'Various' companies. 3. Slugify 'company-title' for 'job_id'.
        FORMAT: { "jobs": [ { "job_title": "", "company": "", "location": "", "application_link": "", "job_id": "", "skills_list": [] } ] }
        """
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"{prompt}\n\nTEXT:\n{content_chunk}"}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("jobs", [])

    except Exception as e:
        msg = "Rate Limit" if "rate_limit" in str(e).lower() else e
        print(f"  [!] Parsing Error: {msg}")
        return []
