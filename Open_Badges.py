import streamlit as st
import json
from openbadges_bakery import bake, unbake

st.title("🏅 Samarth - Open Badges Integration")

# Sidebar for user role
role = st.sidebar.selectbox("Select Role", ["Issuer", "Student"])

# ---- Issuer Interface ---- #
if role == "Issuer":
    st.header("🎖 Issue a Digital Badge")
    student_name = st.text_input("Enter Student Name")
    badge_title = st.text_input("Badge Title", "AI Expert")
    badge_desc = st.text_area("Badge Description", "Awarded for excellence in AI coursework")
    badge_criteria = st.text_area("Criteria", "Scored above 90% in AI assessments")
    badge_image = "https://samarth.edu.in/badges/ai-expert.png"  # Placeholder image URL
    
    if st.button("Generate Badge"):
        badge_data = {
            "@context": "https://w3id.org/openbadges/v2",
            "type": "BadgeClass",
            "id": f"https://samarth.edu.in/badges/{student_name.replace(' ', '_')}-badge",
            "name": badge_title,
            "description": badge_desc,
            "image": badge_image,
            "criteria": {"narrative": badge_criteria},
            "issuer": {
                "id": "https://samarth.edu.in",
                "name": "Samarth University",
                "url": "https://samarth.edu.in",
                "email": "admin@samarth.edu.in"
            }
        }
        
        # Save badge metadata
        badge_filename = f"{student_name.replace(' ', '_')}_badge.json"
        with open(badge_filename, "w") as f:
            json.dump(badge_data, f, indent=4)
        
        # Generate badge image with metadata baked in
        badge_image_filename = f"{student_name.replace(' ', '_')}_badge.png"
        bake(badge_filename, badge_image_filename)
        
        st.success(f"Badge Issued Successfully for {student_name}!")
        st.image(badge_image_filename, caption="🏅 Digital Badge")
        
# ---- Student Interface ---- #
elif role == "Student":
    st.header("🔍 Verify Your Badge")
    uploaded_badge = st.file_uploader("Upload Badge Image", type=["png"])
    
    if uploaded_badge and st.button("Verify Badge"):
        badge_info = unbake(uploaded_badge)
        st.json(badge_info)
        st.success("✅ Badge Verified Successfully!")