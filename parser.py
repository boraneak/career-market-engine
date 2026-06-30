import json
from groq import Groq
import config
from logger import logger
from typing import List, Dict, Any


client = Groq(api_key=config.GROQ_API_KEY)


def parse_markdown_to_jobs(text: str) -> List[Dict[str, Any]]:
    """
    Parses markdown text into a list of job dictionaries using Groq AI.
    
    Args:
        text: Raw markdown content to parse
        
    Returns:
        List of job dictionaries with keys: job_id, job_title, company, 
        location, application_link, skills_list
    """
    if not text:
        logger.warning("Empty text provided to parser")
        return []

    try:
        logger.info(f"Parsing markdown content ({len(text)} characters)...")
        
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
        jobs = data.get("jobs", [])
        logger.info(f"Successfully parsed {len(jobs)} jobs from markdown")
        return jobs

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error from Groq response: {e}", exc_info=True)
        return []
    except Exception as e:
        if "rate_limit" in str(e).lower():
            logger.error("Rate limit exceeded on Groq API - backing off")
        else:
            logger.error(f"Parsing error: {e}", exc_info=True)
        return []
