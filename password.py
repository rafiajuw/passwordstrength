import streamlit as st
import re
from datetime import datetime, timedelta

def estimate_crack_time(password):
    """Simple crack time estimation"""
    if not password:
        return "instant"
    
    char_space = 0
    if re.search(r'[a-z]', password): char_space += 26
    if re.search(r'[A-Z]', password): char_space += 26
    if re.search(r'[0-9]', password): char_space += 10
    if re.search(r'[^A-Za-z0-9]', password): char_space += 32
    
    combinations = char_space ** len(password)
    guesses_per_second = 1e4  # Conservative estimate
    
    seconds = combinations / guesses_per_second
    
    if seconds < 60:
        return "less than a minute"
    elif seconds < 3600:
        return f"about {int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"about {int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"about {int(seconds/86400)} days"
    else:
        return f"about {int(seconds/31536000)} years"

def password_strength(password):
    """Calculate password strength score (0-4)"""
    if not password:
        return 0, "No password entered"
    
    score = 0
    
    # Length check
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    
    # Complexity checks
    checks = [
        bool(re.search(r'[a-z]', password)),
        bool(re.search(r'[A-Z]', password)),
        bool(re.search(r'[0-9]', password)),
        bool(re.search(r'[^A-Za-z0-9]', password))
    ]
    
    score += sum(checks)
    
    # Cap at 4
    score = min(score, 4)
    
    feedback = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong"
    }
    
    return score, feedback[score]

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")
    st.title("🔒 Password Strength Meter")
    
    password = st.text_input("Enter password:", type="password")
    
    if password:
        score, strength = password_strength(password)
        crack_time = estimate_crack_time(password)
        
        # Visual strength meter
        colors = ["#ff0000", "#ff4000", "#ff8000", "#ffbf00", "#00ff00"]
        st.markdown(f"""
        <div style="background-color: #f0f0f0; border-radius: 5px; padding: 3px; margin: 10px 0;">
            <div style="background-color: {colors[score]}; width: {(score+1)*20}%; height: 20px; border-radius: 3px;"></div>
        </div>
        <p style="text-align: center; font-weight: bold; color: {colors[score]}">{strength}</p>
        """, unsafe_allow_html=True)
        
        st.write(f"Estimated crack time: {crack_time}")
        
        # Complexity checks
        st.subheader("Requirements met:")
        cols = st.columns(4)
        checks = [
            ("Length ≥8", len(password) >= 8),
            ("Uppercase", bool(re.search(r'[A-Z]', password))),
            ("Digit", bool(re.search(r'[0-9]', password))),
            ("Special char", bool(re.search(r'[^A-Za-z0-9]', password)))
        ]
        
        for i, (label, met) in enumerate(checks):
            cols[i].metric(label, "✓" if met else "✗")

if __name__ == "__main__":
    main()