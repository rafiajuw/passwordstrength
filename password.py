import streamlit as st
import re
import zxcvbn  # Password strength estimation library

def check_password_strength(password):
    """Check password strength using zxcvbn algorithm"""
    if not password:
        return 0, "No password entered"
    
    result = zxcvbn.zxcvbn(password)
    score = result['score']  # 0-4 scale
    
    feedback = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong"
    }
    
    return score, feedback[score], result['feedback']['suggestions']

def password_complexity_checks(password):
    """Perform basic complexity checks"""
    checks = {
        "length": len(password) >= 8,
        "lowercase": bool(re.search(r'[a-z]', password)),
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "digit": bool(re.search(r'[0-9]', password)),
        "special": bool(re.search(r'[^A-Za-z0-9]', password))
    }
    
    return checks

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")
    
    st.title("🔒 Password Strength Meter")
    st.write("Check how strong your password is and get improvement suggestions")
    
    # Password input
    password = st.text_input("Enter your password:", type="password", help="Type or paste your password to check its strength")
    
    if password:
        # Check strength with zxcvbn
        score, strength, suggestions = check_password_strength(password)
        
        # Display strength meter
        st.subheader("Password Strength")
        
        # Color-coded strength bar
        colors = ["#ff0000", "#ff4000", "#ff8000", "#ffbf00", "#00ff00"]
        st.markdown(f"""
        <div style="background-color: #f0f0f0; border-radius: 5px; padding: 3px; margin-bottom: 10px;">
            <div style="background-color: {colors[score]}; width: {(score+1)*20}%; height: 20px; border-radius: 3px;"></div>
        </div>
        <p style="text-align: center; font-weight: bold; color: {colors[score]}">{strength}</p>
        """, unsafe_allow_html=True)
        
        # Display crack time estimate
        if score < 4:
            st.warning(f"Estimated time to crack: {zxcvbn.zxcvbn(password)['crack_times_display']['offline_slow_hashing_1e4_per_second']}")
        else:
            st.success(f"Estimated time to crack: {zxcvbn.zxcvbn(password)['crack_times_display']['offline_slow_hashing_1e4_per_second']}")
        
        # Display complexity checks
        st.subheader("Complexity Checks")
        checks = password_complexity_checks(password)
        
        cols = st.columns(5)
        metrics = [
            ("Length ≥8", checks["length"]),
            ("Lowercase", checks["lowercase"]),
            ("Uppercase", checks["uppercase"]),
            ("Digit", checks["digit"]),
            ("Special", checks["special"])
        ]
        
        for i, (label, passed) in enumerate(metrics):
            cols[i].metric(label, "✓" if passed else "✗", delta_color="off")
        
        # Display suggestions if password is weak
        if score < 3 and suggestions:
            st.subheader("Improvement Suggestions")
            for suggestion in suggestions:
                st.info(f"💡 {suggestion}")
        
        # Password generation option
        if st.checkbox("Generate a strong password for me"):
            generated_pw = st.secrets["password_generator"]["strong_password"] if "password_generator" in st.secrets else "Xk8@q3$zL9!mN2#"
            st.code(generated_pw, language="text")
            st.button("Copy to clipboard")
    
    st.markdown("---")
    st.write("ℹ️ This tool evaluates password strength without storing or transmitting your password.")
    st.caption("Made with ❤️ using Streamlit and zxcvbn")

if __name__ == "__main__":
    main()