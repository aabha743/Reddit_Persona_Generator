import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# -------- CONFIGURATION --------
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # or llama3-70b or any available
GROQ_API_KEY = os.getenv('API_KEY')

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# -------- DATA HANDLING --------
def load_cleaned_data(username, path="data/cleaned"):
    with open(f"{path}/{username}.json", "r", encoding="utf-8") as f:
        return json.load(f)

def group_by_subreddit(cleaned_data):
    subreddit_groups = {}
    
    # Group comments by subreddit
    for comment in cleaned_data.get("comments", []):
        subreddit = comment["subreddit"]
        if subreddit not in subreddit_groups:
            subreddit_groups[subreddit] = []
        subreddit_groups[subreddit].append({
            "type": "comment",
            "text": comment["cleaned_body"],
            "permalink": comment["permalink"]
        })
    
    # Group posts by subreddit
    for post in cleaned_data.get("posts", []):
        subreddit = post["subreddit"]
        if subreddit not in subreddit_groups:
            subreddit_groups[subreddit] = []
        subreddit_groups[subreddit].append({
            "type": "post",
            "text": post["cleaned_text"],
            "permalink": post["permalink"]
        })
    
    return subreddit_groups

def format_content(content_list):
    formatted_text = ""
    citations = ""
    for idx, item in enumerate(content_list, 1):
        item_type = "Post" if item["type"] == "post" else "Comment"
        formatted_text += f"\n{item_type}: {item['text']} [ref{idx}]"
        citations += f"\n[ref{idx}]: {item['permalink']}"
    return formatted_text, citations

def analyze_content(subreddit_groups):
    all_content = []
    all_citations = []
    
    # Sort subreddits by content count to prioritize most active communities
    sorted_subreddits = sorted(subreddit_groups.items(), key=lambda x: len(x[1]), reverse=True)
    
    for subreddit, content in sorted_subreddits:
        formatted_content, citations = format_content(content)
        all_content.append({
            "subreddit": subreddit,
            "content": formatted_content,
            "content_count": len(content)
        })
        all_citations.append(citations)
    
    return all_content, all_citations

# -------- PROMPT TEMPLATE --------
PERSONA_TEMPLATE = """
Create a professional user persona card based on Reddit activity. Structure the response in this exact format:

### BASIC INFORMATION
- Age: [Inferred age]
- Occupation: [Based on discussions]
- Status: [Relationship/life status if mentioned]
- Location: [Based on location mentions]
- Type: [User archetype]
- Archetype: [Brief descriptor]

### BEHAVIOUR & HABITS
[List 3-4 key behavioral patterns with supporting quotes]

### FRUSTRATIONS
[List 3-4 main pain points or challenges mentioned]

### MOTIVATIONS
- Convenience: [Rate 1-5]
- Wellness: [Rate 1-5]
- Speed: [Rate 1-5]
- Preferences: [Rate 1-5]
- Comfort: [Rate 1-5]
- Dietary Needs: [Rate 1-5]

### PERSONALITY
[Rate on scales:]
- Introvert <-> Extrovert
- Intuition <-> Sensing
- Feeling <-> Thinking
- Perceiving <-> Judging

Include a relevant quote that captures their essence.

Content to analyze:
{text}
"""

# -------- MAIN GENERATOR --------
def generate_persona(username):
    try:
        # Load and group the data
        cleaned_data = load_cleaned_data(username)
        subreddit_groups = group_by_subreddit(cleaned_data)
        analyzed_content = analyze_content(subreddit_groups)

        os.makedirs("data/personas", exist_ok=True)
        output_path = f"data/personas/{username}_persona.txt"
        
        # Prepare all content for analysis
        content_list, _ = analyzed_content  # Unpack tuple, ignore citations for prompt
        all_content = ""
        for content_group in content_list:
            if content_group['content_count'] >= 3:  # Skip subreddits with very few posts/comments
                all_content += f"\n[Subreddit: {content_group['subreddit']}] {content_group['content']}"
        
        # Generate persona sketch
        prompt = PERSONA_TEMPLATE.format(text=all_content)
        print("\n🎯 Generating persona sketch...")
        
        stream = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_completion_tokens=2048,  # Increased token limit for fuller responses
            top_p=1,
            stream=True,
        )

        persona_sketch = ""
        current_line = ""
        for token in stream:
            token_text = token.choices[0].delta.content or ""
            current_line += token_text
            
            # Print and save complete lines only
            if "\n" in token_text:
                lines = current_line.split("\n")
                for line in lines[:-1]:  # Process all complete lines
                    if line.strip():  # Only process non-empty lines
                        # Remove duplicates within the same line
                        if line not in persona_sketch:
                            print(line)
                            persona_sketch += line + "\n"
                current_line = lines[-1]  # Keep the incomplete line
            else:
                print(token_text, end="", flush=True)

        # Add any remaining content
        if current_line:
            print(current_line)
            persona_sketch += current_line

        # Save the persona sketch with citations
        content_list, citations_list = analyzed_content  # Unpack the tuple correctly
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(persona_sketch)
            f.write("\n\n### CITATIONS\n")
            for citations in citations_list:  # Use the unpacked citations list
                f.write(citations)

        print(f"\n✅ Persona sketch saved to {output_path}")
        return persona_sketch  # Return the persona sketch text
    
    except Exception as e:
        error_message = f"Error generating persona: {str(e)}"
        print(error_message)
        return error_message  # Return error message instead of None
