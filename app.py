import streamlit as st
import chromadb
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="India Legal AI Platform",
    page_icon="⚖️",
    layout="wide"
)

# Initialize Session State for Multi-Page Navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

if "selected_state" not in st.session_state:
    st.session_state.selected_state = "Uttar Pradesh"

if "selected_district" not in st.session_state:
    st.session_state.selected_district = "Gautam Buddha Nagar (Noida/Greater Noida)"

# Initialize ChromaDB and Groq Client
@st.cache_resource
def init_resources():
    db_client = chromadb.PersistentClient(path="data/processed/chroma_db")
    collection = db_client.get_or_create_collection(name="indian_property_laws")
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return collection, groq_client

collection, groq_client = init_resources()

# ==============================================================================
# DATA DICTIONARIES: STATES & DISTRICTS OF INDIA
# ==============================================================================
INDIAN_STATES = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", 
    "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", 
    "Delhi (NCT)", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", 
    "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", 
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", 
    "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", 
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

UP_DISTRICTS = [
    "Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha", "Auraiya", "Ayodhya", 
    "Azamgarh", "Baghpat", "Bahraich", "Ballia", "Balrampur", "Banda", "Barabanki", 
    "Bareilly", "Basti", "Bhadohi", "Bijnor", "Budaun", "Bulandshahr", "Chandauli", 
    "Chitrakoot", "Deoria", "Etah", "Etawah", "Farrukhabad", "Fatehpur", "Firozabad", 
    "Gautam Buddha Nagar (Noida/Greater Noida)", "Ghaziabad", "Ghazipur", "Gonda", 
    "Gorakhpur", "Hamirpur", "Hapur", "Hardoi", "Hathras", "Jalaun", "Jaunpur", 
    "Jhansi", "Kannauj", "Kanpur Dehat", "Kanpur Nagar", "Kasganj", "Kaushambi", 
    "Kushinagar", "Lakhimpur Kheri", "Lalitpur", "Lucknow", "Maharajganj", "Mahoba", 
    "Mainpuri", "Mathura", "Mau", "Meerut", "Mirzapur", "Moradabad", "Muzaffarnagar", 
    "Pilibhit", "Pratapgarh", "Prayagraj", "Raebareli", "Rampur", "Saharanpur", 
    "Sambhal", "Sant Kabir Nagar", "Shahjahanpur", "Shamli", "Shravasti", "Siddharthnagar", 
    "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi"
]

# ==============================================================================
# PAGE 1: LANDING PAGE (TWO CARDS SELECTION)
# ==============================================================================
if st.session_state.current_page == "landing":
    st.title("⚖️ National Legal Tech Platform")
    st.markdown("### AI-Powered Statutory Intelligence & Real Estate Due Diligence")
    st.caption("Select a service below to proceed")
    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("💬 AI Legal Guidance Assistant")
        st.markdown(
            """
            * **General Property & Civil Law Query Answering**
            * **RAG-backed Statutory Context** (Bare Acts, IPC/BNS, Property Acts)
            * **Interactive Legal Q&A** for buyers, sellers, and advocates
            """
        )
        if st.button("Launch Legal Chatbot 🤖", use_container_width=True):
            st.session_state.current_page = "chatbot"
            st.rerun()

    with col2:
        st.subheader("🔍 Automated Property Legal Audit Engine")
        st.markdown(
            """
            * **Jurisdiction-Specific Due Diligence Audit**
            * **Title Tenure & Statutory Tax Calculation Engine**
            * **Noida / UP Authority Regulatory Compliance Reports**
            """
        )
        if st.button("Start Property Due Diligence Audit 🏢", type="primary", use_container_width=True):
            st.session_state.current_page = "location_select"
            st.rerun()

# ==============================================================================
# PAGE 2: LOCATION SELECTOR PAGE
# ==============================================================================
elif st.session_state.current_page == "location_select":
    st.button("⬅️ Back to Main Menu", on_click=lambda: st.session_state.update({"current_page": "landing"}))
    
    st.title("📍 Select Jurisdiction & Location")
    st.markdown("Select your property location to apply local land revenue codes, municipal laws, and authority rules.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        state = st.selectbox("Select State / Union Territory", INDIAN_STATES, index=INDIAN_STATES.index("Uttar Pradesh"))
        st.session_state.selected_state = state

    with col2:
        if state == "Uttar Pradesh":
            district = st.selectbox("Select District / Authority Region", UP_DISTRICTS, index=28)
            st.session_state.selected_district = district
        else:
            district = st.text_input("Enter District / Municipal Region", value="Central District")
            st.session_state.selected_district = district

    st.divider()

    if st.button("Proceed to Title Audit Intake Form 🚀", type="primary"):
        st.session_state.current_page = "audit_form"
        st.rerun()

# ==============================================================================
# PAGE 3: CHATBOT PAGE
# ==============================================================================
elif st.session_state.current_page == "chatbot":
    st.button("⬅️ Back to Main Menu", on_click=lambda: st.session_state.update({"current_page": "landing"}))
    
    st.title("💬 AI Legal Guidance Assistant")
    st.caption("Ask queries regarding Indian Property Laws, Transfer of Property Act, RERA, and Land Regulations")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask a legal question..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching legal vector database..."):
                # RAG Query
                results = collection.query(query_texts=[user_prompt], n_results=4)
                context = "\n\n".join(results["documents"][0]) if results["documents"] else ""
                
                full_prompt = f"Context from Legal Database:\n{context}\n\nUser Question: {user_prompt}"
                
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": full_prompt}],
                    temperature=0.2
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# ==============================================================================
# PAGE 4: PROPERTY AUDIT INTAKE & GENERATION ENGINE
# ==============================================================================
elif st.session_state.current_page == "audit_form":
    st.button("⬅️ Change Location / Back", on_click=lambda: st.session_state.update({"current_page": "location_select"}))
    
    st.title(f"⚖️ Property Legal Audit: {st.session_state.selected_district}, {st.session_state.selected_state}")
    st.caption("Interactive Intake Form & Deterministic Local Law Engine")

    # Dynamic Jurisdiction Context Alert
    if "Gautam Buddha Nagar" in st.session_state.selected_district:
        st.info("ℹ️ Jurisdiction Detected: Gautam Buddha Nagar (Noida Authority / Greater Noida / YEIDA). Enforcing 99-year Leasehold Framework, UP Revenue Code 2006, and Transfer Memorandum (TM) rules.")
    else:
        st.warning(f"ℹ️ Jurisdiction Detected: {st.session_state.selected_district}. Applying General State Land Revenue Code and Municipal Registration Rules.")

    st.subheader("📋 Step 1: Property & Transaction Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        sector_number = st.text_input("Sector / Area / Pocket Name", value="121")
        plot_category = st.selectbox(
            "Land & Title Tenure Category",
            [
                "Noida Authority Direct Allotted Residential Plot",
                "Builder Plotted Township / Sub-Plot",
                "Village Abadi / Lal Dora Land",
                "Gram Sabha Agricultural Land (Unconverted)"
            ]
        )
        seller_type = st.selectbox(
            "Seller Status & Legal Capacity",
            [
                "Individual Allottee / Owner",
                "General Power of Attorney (GPA) Holder",
                "Non-Resident Indian (NRI)",
                "Corporate Entity / Company / LLP",
                "Minor Owner / Trust Property"
            ]
        )

    with col2:
        agreed_price = st.number_input("Agreed Sale Consideration (₹)", min_value=100000, value=8500000, step=100000)
        circle_rate_value = st.number_input("Circle Rate Valuation of Property (₹)", min_value=100000, value=8000000, step=100000)
        buyer_gender = st.selectbox(
            "Primary Buyer Gender / Ownership Category",
            [
                "Male Individual",
                "Female Single Owner",
                "Joint Ownership (Male + Female)"
            ]
        )

    with col3:
        mortgage_status = st.selectbox(
            "Active Mortgage Status",
            [
                "Unencumbered (No Active Loan)",
                "Active Bank Loan / Documents in Bank Vault"
            ]
        )
        construction_status = st.selectbox(
            "Construction Status",
            [
                "Vacant Unconstructed Plot",
                "Partially Constructed / Stilt+4 Completed"
            ]
        )
        proposed_token = st.number_input("Proposed Token / Advance Amount (₹)", min_value=0, value=200000, step=50000)

    st.divider()

    # Deterministic Local Law Calculation Engine
    taxable_val = max(agreed_price, circle_rate_value)
    is_female = (buyer_gender == "Female Single Owner")

    # Stamp Duty Rules (UP Stamp Act)
    stamp_duty = taxable_val * 0.07
    if is_female:
        stamp_duty = max(0, stamp_duty - 10000)

    reg_fee = taxable_val * 0.01
    tds_required = taxable_val >= 5000000
    tds_val = taxable_val * 0.01 if tds_required else 0.0
    tm_charge = circle_rate_value * 0.025

    if st.button("🚀 Run Master Legal Audit", type="primary"):
        search_query = f"{st.session_state.selected_district} plot transfer rules, UP Revenue Code Section 80, Income Tax Section 194-IA TDS, UP Stamp Duty female rebate, GPA Suraj Lamp"
        results = collection.query(query_texts=[search_query], n_results=6)
        retrieved_legal_text = "\n\n".join(results["documents"][0]) if results["documents"] else "Standard Statutory Provisions Apply."

        prompt = f"""
        You are a Senior Real Estate Legal Advocate in {st.session_state.selected_district}, {st.session_state.selected_state}.
        
        Synthesize an exhaustive 10/10 Master Legal Due Diligence Dossier based on the input profile:

        PROPERTY & TRANSACTION PROFILE:
        --------------------------------------------------
        - Jurisdiction: {st.session_state.selected_district}, {st.session_state.selected_state}
        - Sector/Area: Sector {sector_number}
        - Title Category: {plot_category}
        - Seller Type: {seller_type}
        - Agreed Price: ₹{agreed_price:,.2f} | Circle Rate Value: ₹{circle_rate_value:,.2f}
        - Taxable Valuation: ₹{taxable_val:,.2f}
        - Buyer Category: {buyer_gender}
        - Mortgage Status: {mortgage_status}
        - Construction Status: {construction_status}
        - Proposed Token Payment: ₹{proposed_token:,.2f}
        --------------------------------------------------

        PRE-COMPUTED STATUTORY DUES:
        - Calculated Stamp Duty: ₹{stamp_duty:,.2f} (Female Rebate Applied: {is_female})
        - Registration Fees: ₹{reg_fee:,.2f}
        - TDS Liability (Sec 194-IA): ₹{tds_val:,.2f} (Required: {tds_required})
        - Estimated Noida Authority TM Charge: ₹{tm_charge:,.2f}

        RETRIEVED STATUTORY CONTEXT FROM CHROMADB:
        --------------------------------------------------
        {retrieved_legal_text}
        --------------------------------------------------

        INSTRUCTIONS:
        Generate a 6-part legal report tailored to {st.session_state.selected_district}:
        1. EXECUTIVE TITLE RISK ASSESSMENT: Highlight red flags with '{plot_category}' and '{seller_type}' (cite Suraj Lamp v. State of Haryana if GPA, Sec 80 UP Revenue Code if agricultural).
        2. MANDATORY STATUTORY CHECKLIST: List primary documents required (Allotment Letter, Lease Deed, 30-year Search, Form 15/16 EC, TM Order).
        3. LOCAL MUNICIPAL & BUILDING COMPLIANCE: Detail Transfer Memorandum (TM) process, unconstructed plot extension penalties, and Noida Building Bye-Laws (FAR 1.80, height caps, setbacks).
        4. STATUTORY FINANCIAL & TAX AUDIT TABLE: Show pre-computed stamp duty, registration, 1% TDS (Sec 194-IA) via Form 26QB, and TM fees with legal explanations.
        5. CONTRACTUAL SAFEGUARDS IN ATS: Specify indemnity, clear title warranty, and token refund clauses. Cap advance payments appropriately.
        6. STEP-BY-STEP EXECUTION PROTOCOL: Outline sequential steps from SRO Registration to Local Mutation (Namantaran).
        """

        with st.spinner("Analyzing local statutory provisions and building regulations..."):
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            report = completion.choices[0].message.content

        st.success("✅ Master Legal Due Diligence Dossier Generated Successfully!")
        
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Calculated Stamp Duty", f"₹{stamp_duty:,.0f}")
        mcol2.metric("Registration Fees", f"₹{reg_fee:,.0f}")
        mcol3.metric("Section 194-IA TDS", f"₹{tds_val:,.0f}")
        mcol4.metric("Noida TM Fee (Est.)", f"₹{tm_charge:,.0f}")

        st.markdown("---")
        st.markdown(report)
