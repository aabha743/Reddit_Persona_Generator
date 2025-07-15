import hashlib

def generate_avatar_url(persona_text):
    """Generate an avatar URL based on persona characteristics using DiceBear API.
    
    Args:
        persona_text (str): The persona text containing user characteristics
        
    Returns:
        str: URL to the generated avatar
    """
    # Extract key characteristics from persona text
    characteristics = []
    colors = []
    age = '25'  # Default age - moved to function scope
    
    # Add personality traits if present
    if 'PERSONALITY:' in persona_text:
        personality_section = persona_text.split('PERSONALITY:')[1].split('\n\n')[0]
        traits = personality_section.lower()
        
        # Map personality traits to colors
        if 'introvert' in traits:
            colors.extend(['b6e3f4', '9db4d0'])  # Cool, calming colors
        if 'extrovert' in traits:
            colors.extend(['ffb347', 'ffd700'])  # Warm, energetic colors
        if 'thinking' in traits:
            colors.extend(['7dc9e7', '4682b4'])  # Clear, analytical colors
        if 'feeling' in traits:
            colors.extend(['e6a8d7', 'dda0dd'])  # Soft, emotional colors
            
        characteristics.extend(personality_section.split())
    
    # Add basic information keywords
    if 'BASIC INFORMATION:' in persona_text:
        basic_info = persona_text.split('BASIC INFORMATION:')[1].split('\n\n')[0].lower()
        
        # Extract age for size adjustment
        age_line = [line for line in basic_info.split('\n') if 'age:' in line.lower()]
        if age_line:
            age_text = age_line[0].split(':')[1].strip()
            extracted_age = ''.join(filter(str.isdigit, age_text))
            if extracted_age:
                age = extracted_age
        
        characteristics.extend(basic_info.split())
    
    # Create a deterministic seed based on characteristics
    seed = ' '.join(characteristics).lower()
    seed_hash = hashlib.md5(seed.encode()).hexdigest()
    
    # Select background color based on personality
    background_color = colors[int(seed_hash[0], 16) % len(colors)] if colors else 'b6e3f4'
    
    # Generate avatar URL using DiceBear API with customized parameters
    avatar_url = (
        f"https://api.dicebear.com/7.x/bottts/svg"
        f"?seed={seed_hash}"
        f"&backgroundColor={background_color}"
        f"&scale={min(100, int(age) + 50)}"
        f"&radius=10"
        f"&translateY=5"
    )
    
    return avatar_url