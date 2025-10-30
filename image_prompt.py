import streamlit as st
import urllib.parse

# Constants for options
ASPECT_RATIOS = ["16:9", "3:2", "1:1", "4:3", "2:3", "21:9", "5:4", "7:5", "4:5", "2:1", "9:16"]
SUBSTRATES = ["inked comic illustration", "digital paint", "oil painting", "sketch", "realistic", "3D render", "collage", "pastel", "pixel art", "watercolor"]
ARTISTS = ["Frank Miller", "vintage DC", "photorealism", "pop art", "noir comics", "Moebius", "Hergé", "Jack Kirby", "Studio Ghibli", "Banksy"]
COATINGS = ["crosshatch texture", "smooth paint", "grainy paper", "canvas", "scratched vinyl", "halftone", "glossy", "matte"]
ENVIRONMENTS = ["mid-century modern cafe", "nightclub", "alleyway", "office", "foggy street", "apartment", "desert", "battlefield", "studio"]
STYLES = ["dramatic noir illustration", "graphic novel", "fine art", "cartoon", "cinematic", "modern comic", "vintage comic", "hyper-real", "expressionist", "anime"]
WEATHERS = ["indoors", "rainy", "foggy", "clear", "dusty", "snowy", "stormy", "hazy", "humid"]
TIMES = ["evening", "night", "sunset", "day", "afternoon", "dawn", "midnight"]

def render_field(label, options, default, key):
    extended_options = options + ["Custom..."]
    selected = st.selectbox(label, extended_options, index=extended_options.index(default) if default in extended_options else len(extended_options)-1, key=key)
    if selected == "Custom...":
        return st.text_input(f"Custom value for {label}", key=f"{key}_custom")
    return selected

# Page config
st.set_page_config(page_title="AI Image Prompt Generator & Launcher", layout="wide")

# Modern, professional dark theme with subtle elegance
st.markdown("""
<style>
body, .main {
    background: linear-gradient(135deg, #2c3e50, #4ca1af);
    min-height: 100vh;
    color: #f0f0f5 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3 {
    color: #dfe6e9 !important; /* muted light shade for headers */
    font-weight: 700;
    letter-spacing: 1.2px;
}
.stButton>button {
    background: linear-gradient(45deg, #2980b9, #6a11cb);
    color: #fff !important;
    border-radius: 10px !important;
    height: 3em !important;
    font-weight: 700;
    font-size: 1.1em;
    box-shadow: 0 4px 12px rgba(41, 128, 185, 0.4);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(45deg, #6a11cb, #2980b9);
    box-shadow: 0 6px 18px rgba(41, 128, 185, 0.6);
}
.stTextInput>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div>input {
    background-color: #34495e !important;
    color: #f0f0f5 !important;
    border-radius: 8px !important;
    border: 1px solid #2980b9 !important;
    padding-left: 12px;
    font-size: 1em;
}
.stTextInput>div>input::placeholder, .stTextArea>div>textarea::placeholder {
    color: #bdc3c7 !important;
    opacity: 0.8;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #34495e, #2c3e50);
    color: #f0f0f5;
    font-weight: 600;
}
img {
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    transition: transform 0.3s ease;
}
img:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

st.title("AI Image Prompt Generator & Launcher")

# Input sections
col1, col2 = st.columns(2)

with col1:
    aspect_ratio = render_field("Aspect Ratio", ASPECT_RATIOS, "16:9", "aspect_ratio")
    substrate = render_field("Art Substrate", SUBSTRATES, "inked comic illustration", "substrate")
    artist_style = render_field("Artist Style", ARTISTS, "Frank Miller", "artist_style")
    coating = render_field("Coating Texture", COATINGS, "crosshatch texture", "coating")
    environment = render_field("Environment", ENVIRONMENTS, "mid-century modern cafe", "environment")

with col2:
    style = render_field("Overall Style", STYLES, "dramatic noir illustration", "style")
    weather = render_field("Weather", WEATHERS, "indoors", "weather")
    time_of_day = render_field("Time of Day", TIMES, "evening", "time_of_day")

instruction_prompt = st.text_area("Instruction Prompt (Describe your image)", height=80, placeholder="E.g., cinematic hero shot in bronze hues")

# Create the combined prompt
def create_text_prompt():
    parts = [
        instruction_prompt.strip(),
        f"Aspect Ratio: {aspect_ratio}",
        f"Substrate: {substrate}",
        f"Artist Style: {artist_style}",
        f"Texture: {coating}",
        f"Environment: {environment}",
        f"Style: {style}",
        f"Weather: {weather}",
        f"Time of Day: {time_of_day}"
    ]
    return ", ".join([p for p in parts if p])

text_prompt = create_text_prompt()

st.markdown("### Generated Text Prompt")
st.text_area("Copy or edit your prompt below", text_prompt, height=140, key="generated_prompt_text_area")

# Launch options in professional, elegant style
st.markdown("---")
st.subheader("Launch Prompt in AI Generators")

user_prompt = st.session_state.get("generated_prompt_text_area", text_prompt)

def encode_prompt(prompt: str):
    return urllib.parse.quote_plus(prompt)

encoded_prompt = encode_prompt(user_prompt)
AUTOMATIC1111_url = f"http://localhost:7860/?__theme=dark#txt2img&txt2img_prompt={encoded_prompt}"

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Midjourney (Discord)**")
    st.write("Copy the prompt below and paste it in Midjourney DM or server `/imagine prompt:`")
    st.text_area("Midjourney Prompt", user_prompt, height=100, key="mid_prompt")
    if st.button("I have copied the prompt"):
        st.info("Paste it into Midjourney Discord after copying.")

with col2:
    st.markdown("**DALL·E 3**")
    st.write("Open [DALL·E 3](https://openai.com/dall-e) and paste the prompt.")
    
with col3:
    st.markdown("**Stable Diffusion (Local UI)**")
    st.write("If you have a local server, click the link below to launch with prompt.")
    st.markdown(f"[Launch with Prompt]({AUTOMATIC1111_url})")

st.markdown("---")
