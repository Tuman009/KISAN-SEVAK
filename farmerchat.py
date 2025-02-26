import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with KISAN SEVAK...!",
    page_icon=":crop:",  # Favicon emoji
    layout="centered",    # Page layout option
)


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Function to check if a question is related to farming
def is_farming_question(question):
    farming_keywords = ["advantages","disadvantages","Advantages","Disadvantages","season","types","best","earning","money","cost",
    "farm", "farmer", "agriculture", "crop", "livestock", "harvest", "plant", "soil", "irrigation","grow","place","worst","government"," policies",
    "fertilizer", "pesticide", "tractor", "agribusiness", "horticulture", "agronomy", "farming", "weather","seeds","seed","place",
    "climate", "rain", "drought", "flood", "temperature", "humidity", "forecast", "precipitation",
    "farming techniques", "organic", "sustainable", "yield", "seed", "greenhouse", "pest", "disease control",
    "tillage", "conservation", "aquaculture", "hydroponics", "permaculture", "animal husbandry", "cultivation", "cultivate",
    "dairy", "poultry", "bee", "apiculture", "silviculture", "forestry", "crop rotation",
    "composting", "green manure", "cover crops", "mulching", "pruning", "grafting", "genetically modified",
    "biotechnology", "soil health", "soil erosion", "water management", "farm management", "market",
    "pricing", "export", "import", "rural", "extension services", "farm policy", "food security", "agroecology", "growing",
    "vertical farming", "agritech", "precision agriculture", "drone technology", "smart farming", "urban farming", "microgreens",
    "food supply chain", "carbon farming", "regenerative agriculture", "agricultural innovation", "farmland",
    "agricultural sustainability", "climate-smart agriculture", "nutrient management", "food safety", "supply chain management",
    "agricultural policy", "digital farming", "blockchain in agriculture", "AI in agriculture", "robotic farming", "crop monitoring",
    "land management", "agricultural economics", "farmer cooperatives", "biopesticides", "integrated pest management",
    "agricultural engineering", "supply chain resilience", "data-driven agriculture", "farm-to-table", "local food systems",
    "traceability", "biodiversity", "agroforestry", "farmer training", "agricultural finance", "smart irrigation", "agricultural research",
    "sustainable practices", "renewable energy in agriculture", "agricultural education", "community-supported agriculture",
    "e-agriculture", "farm safety", "crop insurance", "agrifood", "alternative proteins", "soil carbon sequestration",
    "farmer livelihoods", "post-harvest management", "aquaponics", "biocontrol", "circular agriculture", "farmer empowerment",
    "climate adaptation", "resilient agriculture", "plant breeding", "vertical integration", "organic certification",
    "agroinformatics", "soil microbiome", "food sovereignty", "biofortification", "climate resilience", 
    "nutraceuticals", "agro-tourism", "eco-friendly farming", "perennial crops", "conservation tillage",
    "crop diversification", "biostimulants", "farmer aggregation", "agro-climatic zones", "food traceability", 
    "zero tillage", "smart greenhouses", "agricultural drones", "weather stations", "sustainable intensification",
    "soil fertility", "biochar", "trace gas emissions", "remote sensing", "ecosystem services", "precision livestock farming",
    "land tenure", "farm digitization", "crop modeling", "water footprint", "food miles", "digital soil mapping",
    "integrated farming", "nutrient cycling", "agri-fintech", "crop phenotyping", "food hubs", "carbon sequestration",
    "vertical integration", "open-pollinated varieties", "natural farming", "agricultural robotics", "traceability",
    "regenerative systems", "climate mitigation", "agricultural transformation", "agribusiness entrepreneurship",
    "regional food systems", "ecosystem management", "renewable resources", "pest resistance", "agricultural resilience"
]

    return any(keyword in question.lower() for keyword in farming_keywords)

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 KISAN SEVAK - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask KISAN SEVAK...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    if is_farming_question(user_prompt):
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    else:
        # Display a message about the chatbot's focus
        with st.chat_message("assistant"):
            st.markdown("I'm here to answer farming-related questions. Please ask something about farming.")
