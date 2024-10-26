import streamlit as st
from fpdf import FPDF
import base64

# Function to load CSS
#def load_css (file_path):    
#    with open (file_path) as f:
#        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the external CSS from the same directory as main.py
#load_css("styles.css")

# Set the page layout to wide mode
st.set_page_config(layout="wide", page_icon="🪥", page_title="Dental Treatment Plan")

# Tooth descriptions dictionary
tooth_descriptions = {
    'UR1': 'Upper right first incisor',
    'UR2': 'Upper right second incisor',
    'UR3': 'Upper right canine',
    'UR4': 'Upper right first premolar',
    'UR5': 'Upper right second premolar',
    'UR6': 'Upper right first molar',
    'UR7': 'Upper right second molar',
    'UR8': 'Upper right third molar',
    'UL1': 'Upper left first incisor',
    'UL2': 'Upper left second incisor',
    'UL3': 'Upper left canine',
    'UL4': 'Upper left first premolar',
    'UL5': 'Upper left second premolar',
    'UL6': 'Upper left first molar',
    'UL7': 'Upper left second molar',
    'UL8': 'Upper left third molar',
    'LR1': 'Lower right first incisor',
    'LR2': 'Lower right second incisor',
    'LR3': 'Lower right canine',
    'LR4': 'Lower right first premolar',
    'LR5': 'Lower right second premolar',
    'LR6': 'Lower right first molar',
    'LR7': 'Lower right second molar',
    'LR8': 'Lower right third molar',
    'LL1': 'Lower left first incisor',
    'LL2': 'Lower left second incisor',
    'LL3': 'Lower left canine',
    'LL4': 'Lower left first premolar',
    'LL5': 'Lower left second premolar',
    'LL6': 'Lower left first molar',
    'LL7': 'Lower left second molar',
    'LL8': 'Lower left third molar',
    'UA' : 'Upper arch',
    'LA' : 'Lower arch'
}

# Function to map tooth codes to descriptions
def map_tooth_code(code):
    return tooth_descriptions.get(code, code)  # Fallback to code if not found

st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Header with total cost box
header_col1, header_col2 = st.columns([6, 1])
with header_col1:
    st.header("Dental Treatment Plan")

# Initialize total cost
total_cost = 0

st.divider()

# Define a structure for upper and lower teeth, organized by quadrants
upper_right = ['UA', 'UR8', 'UR7', 'UR6', 'UR5', 'UR4', 'UR3', 'UR2', 'UR1']
upper_left = ['UL1', 'UL2', 'UL3', 'UL4', 'UL5', 'UL6', 'UL7', 'UL8']
lower_right = ['LA', 'LR8', 'LR7', 'LR6', 'LR5', 'LR4', 'LR3', 'LR2', 'LR1']
lower_left = ['LL1', 'LL2', 'LL3', 'LL4', 'LL5', 'LL6', 'LL7', 'LL8']

# Create empty dictionary to store treatment status
teeth_status = {}

# Create three columns: one for upper right, one as a spacer, and one for upper left
col1, spacer, col2 = st.columns([2.3, 0.0001, 2])  # Adjust the size of columns: 8 for content, 1 for space

# Display Upper Right Teeth in the first column
with col1:
    st.write("‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ Upper Right Teeth")
    cols = st.columns(9)  # Create 8 columns for the 8 upper right teeth
    for i, tooth in enumerate(upper_right):
        teeth_status[tooth] = cols[i].checkbox(f"{tooth}", key=tooth)

# Add a blank spacer in the middle
with spacer:
    st.write(" ")  # Spacer column

# Display Upper Left Teeth in the third column
with col2:
    st.write("Upper Left Teeth")
    cols = st.columns(8)  # Create 8 columns for the 8 upper left teeth
    for i, tooth in enumerate(upper_left):
        teeth_status[tooth] = cols[i].checkbox(f"{tooth}", key=tooth)

# Create three columns: one for lower right, one as a spacer, and one for lower left
col3, spacer2, col4 = st.columns([2.3, 0.0001, 2])  # Adjust the size of columns: 8 for content, 1 for space

# Display lower Right Teeth in the first column
with col3:
    st.write("‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ Lower Right Teeth")
    cols = st.columns(9)  # Create 8 columns for the 8 lower right teeth
    for i, tooth in enumerate(lower_right):
        teeth_status[tooth] = cols[i].checkbox(f"{tooth}", key=tooth)

# Add a blank spacer in the middle
with spacer2:
    st.write(" ")  # Spacer column

# Display lower Left Teeth in the third column
with col4:
    st.write("Lower Left Teeth")
    cols = st.columns(8)  # Create 8 columns for the 8 lower left teeth
    for i, tooth in enumerate(lower_left):
        teeth_status[tooth] = cols[i].checkbox(f"{tooth}", key=tooth)

selected_treatments = []

with st.container(height=530):
    # Handle Treatment paths
    stabilisation_data = []
    for tooth, selected in teeth_status.items():
        if selected:
            tooth_data = {"Tooth": tooth, "Treatments": []}
            # Check if UA or LA is selected for Denture path
            if tooth in ['UA', 'LA']:
                st.markdown(f"<div style='font-size:16px; font-weight:bold;'>Treatment for {tooth} ({map_tooth_code(tooth)})</div>", unsafe_allow_html=True)
                col_treatment, col_time, col_lab_fee, col_cost = st.columns([2, 1, 1, 1])
                treatment_option = col_treatment.selectbox(
                    "Treatment Required",
                    ["Please select", "Full denture", "Partial denture (Metal)", "Partial denture (Plastic)"],
                    key=f"treatment_{tooth}_denture"
                )
                time_required = col_time.number_input(
                    "Time Required (minutes)",
                    min_value=0,
                    max_value=300,
                    step=10,
                    key=f"time_{tooth}_denture"
                )
                lab_fee = col_lab_fee.number_input(
                    "Lab Fee (£)",
                    min_value=0,
                    step=10,
                    key=f"lab_fee_{tooth}_denture"
                )
                cost = time_required * 5.5 + lab_fee
                col_cost.text_input("Cost", value=f"£{cost:.2f}", disabled=True, key=f"cost_{tooth}_denture")
                total_cost += cost
                selected_treatments.append(("Rehabilitation Phase", map_tooth_code(tooth), treatment_option, cost))
            else:
                # Ask if Stabilisation or Restoration Phase is needed for non-denture teeth
                st.markdown(f"<div style='font-size:16px; font-weight:bold;'>Treatment for {tooth} ({map_tooth_code(tooth)})</div>", unsafe_allow_html=True)
                stab_yes_no, rest_yes_no, spacey = st.columns([1, 1, 3])
                stabilisation_required = stab_yes_no.selectbox(
                    f"Stabilisation Phase",
                    ["No", "Yes"],
                    key=f"stab_{tooth}"
                )
                restoration_required = rest_yes_no.selectbox(
                    f"Restoration Phase",
                    ["No", "Yes"],
                    key=f"rest_{tooth}"
                )

                # Stabilisation Phase
                if stabilisation_required == "Yes":
                    header_cols = st.columns([1])
                    header_cols[0].markdown(f"<div style='font-size:14px; font-weight:bold; color: red;'>Stabilisation Phase</div>", unsafe_allow_html=True)
                    col_treatment, col_time, col_lab_fee, col_cost = st.columns([2, 1, 1, 1])
                    treatment_option = col_treatment.selectbox(
                        "Treatment Required",
                        ["Please select", "Complex extraction", "Core build up", "Crown removal and core", "Extirpation", "Extraction", "Extraction with immediate replacement", "Permanent filling", "Provisional filling", "Temporary crown"],
                        key=f"treatment_{tooth}_stab"
                    )
                    time_required = col_time.number_input(
                        "Time Required (minutes)",
                        min_value=0,
                        max_value=300,
                        step=10,
                        key=f"time_{tooth}_stab"
                    )
                    lab_fee = col_lab_fee.number_input(
                        "Lab Fee (£)",
                        min_value=0,
                        step=10,
                        key=f"lab_fee_{tooth}"
                    )
                    # Determine rate for stabiliation phase
                    if treatment_option == "Complex extraction":
                        xla_rate = 400 / 60
                    else:
                        xla_rate = 5.5
                    cost = time_required * xla_rate + lab_fee
                    col_cost.text_input("Cost", value=f"£{cost:.2f}", disabled=True, key=f"cost_{tooth}_stab")
                    total_cost += cost
                    stabilisation_data.append((tooth, treatment_option, col_lab_fee, time_required, cost))
                    selected_treatments.append(("Stabilisation Phase", map_tooth_code(tooth), treatment_option, cost))

                    # Add second treatment option if Extraction is selected
                    if treatment_option == "Extraction with immediate replacement":
                        st.markdown(":red[• Second Treatment Option]")
                        col_treatment_2, col_time_2, col_lab_fee_2, col_cost_2 = st.columns([2, 1, 1, 1])
                        second_treatment = col_treatment_2.selectbox(
                            "Treatment Required",
                            ["Please select", "Immediate denture", "Rochette bridge"],
                            key=f"second_treatment_{tooth}"
                        )
                        second_time_required = col_time_2.number_input(
                            "Time Required (minutes)",
                            min_value=0,
                            max_value=300,
                            step=10,
                            key=f"second_time_{tooth}"
                        )
                        lab_fee_2 = col_lab_fee_2.number_input(
                            "Lab Fee (£)",
                            min_value=0,
                            step=10,
                            key=f"lab_fee_2_{tooth}"
                        )
                        second_cost = (second_time_required * 5.5) + lab_fee_2
                        col_cost_2.text_input("Cost", value=f"£{second_cost:.2f}", disabled=True, key=f"second_cost_{tooth}")
                        total_cost += second_cost
                        selected_treatments.append(("Stabilisation Phase", map_tooth_code(tooth), second_treatment, second_cost))

                # Restoration Phase
                if restoration_required == "Yes":
                    header_cols = st.columns([1])
                    header_cols[0].markdown(f"<div style='font-size:14px; font-weight:bold; color: blue;'>Restoration Phase</div>", unsafe_allow_html=True)
                    col_treatment_3, col_time_3, col_lab_fee_3, col_cost_3 = st.columns([2, 1, 1, 1])
                    restoration_option = col_treatment_3.selectbox(
                        "Treatment Required",
                        ["Please select", "Bridge", "Complex root canal treatment", "Crown", "Filling", "Implant", "Root canal treatment", "Veneer"],
                        key=f"treatment_{tooth}_rest"
                    )
                    lab_fee_3 = col_lab_fee_3.number_input(
                        "Lab Fee (£)",
                        min_value=0,
                        step=10,
                        key=f"lab_fee_3_{tooth}"
                    )
                    time_required_3 = col_time_3.number_input(
                        "Time Required (minutes)",
                        min_value=0,
                        max_value=300,
                        step=10,
                        key=f"time_{tooth}_rest"
                    )
                    # Determine rate for restoration phase
                    if restoration_option == "Implant":
                        rate = 4000 / 60
                    elif restoration_option == "Complex root canal treatment":
                        rate = 1000 / 60
                    else:
                        rate = 5.5
                    cost_3 = time_required_3 * rate + lab_fee_3
                    col_cost_3.text_input("Cost", value=f"£{cost_3:.2f}", disabled=True, key=f"cost_3_{tooth}_rest")
                    total_cost += cost_3
                    selected_treatments.append(("Restoration Phase", map_tooth_code(tooth), restoration_option, cost_3))

                    # Add second treatment option if Root canal treatment is selected
                    if restoration_option in ["Root canal treatment","Complex root canal treatment"]:
                        st.markdown(":blue[• Second Treatment Option]")
                        col_treatment_4, col_time_4, col_lab_fee_4, col_cost_4 = st.columns([2, 1, 1, 1])
                        second_treatment_2 = col_treatment_4.selectbox(
                            "Treatment Required",
                            ["Please select", "Core", "Crown", "Internal whitening and core", "Onlay"],
                            key=f"second_treatment_2{tooth}"
                        )
                        second_time_required_2 = col_time_4.number_input(
                            "Time Required (minutes)",
                            min_value=0,
                            max_value=300,
                            step=10,
                            key=f"second_time_2{tooth}"
                        )
                        lab_fee_4 = col_lab_fee_4.number_input(
                            "Lab Fee (£)",
                            min_value=0,
                            step=10,
                            key=f"lab_fee_4_{tooth}"
                        )
                        second_cost_2 = (second_time_required_2 * 5.5) + lab_fee_4
                        col_cost_4.text_input("Cost", value=f"£{second_cost_2:.2f}", disabled=True, key=f"second_cost_2{tooth}")
                        total_cost += second_cost_2
                        selected_treatments.append(("Restoration Phase", map_tooth_code(tooth), second_treatment_2, second_cost_2))

# Update total cost box
with header_col2:
    st.markdown(
        """
        <div style="background-color:#ff4b4b; padding: 10px; border-radius: 8px; text-align: center; color: white; font-size: 20px;">
            <strong>Total Cost: £{:.2f}</strong>
        </div>
        """.format(total_cost),
        unsafe_allow_html=True
    )

# Display selected treatments summary
def display_summary_by_phase(phase, treatments, pdf=None):
    if pdf:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=phase, ln=True)
        pdf.set_font("Arial", size=12)
    else:
        st.markdown(f"### {phase}")
    for _, tooth_desc, treatment, cost in treatments:
        if treatment != "Please select":
            additional_note = ""
            additional_note2 = ""
            if treatment in ["Implant","Complex root canal treatment","Complex extraction"]:
                additional_note = "*The price given for this item is a rough estimate only. A definitive treatment plan including cost will be"
                additional_note2 = "issued by the clinician carrying out the treatment following an assessment."
            if pdf:
                pdf.cell(200, 10, txt=f"- {tooth_desc}: {treatment} at a cost of £{cost:.2f}", ln=True)
                if additional_note:
                    pdf.cell(200, 10, txt=additional_note, ln=True)
                if additional_note2:
                    pdf.cell(200, 10, txt=additional_note2, ln=True)
            else:
                st.write(f"- **{tooth_desc}**: {treatment} at a cost of £{cost:.2f}{additional_note}")
                st.write(f"{additional_note2}")
    if pdf:
        pdf.ln(5)

if selected_treatments:
    st.markdown("## Dental Treatment Plan Quotation")
    additional_info = st.text_area("Enter any additional text required for the quotation here.", height=50)
    for phase in ["Stabilisation Phase", "Restoration Phase", "Rehabilitation Phase"]:
        phase_treatments = [t for t in selected_treatments if t[0] == phase]
        if phase_treatments:
            display_summary_by_phase(phase, phase_treatments)
    # Display total cost at the bottom of the summary
    st.write(f"**Total Investment: £{total_cost:.2f}**")

# Create PDF button
if selected_treatments and st.button("Create PDF",type="primary"):
    pdf = FPDF()
    pdf.add_page()
    
    # Add more space at the top before the title
    pdf.set_font("Arial", size=16, style='B')
    pdf.image("Forward-Dental-Care-Logo.png", x=160, y=10, w=40)
    
    # Add vertical space before the title (increase this value to move the title down)
    pdf.ln(20)  # Adjust this value to control how far down the title appears
    
    # Title: Dental Treatment Plan Quotation
    pdf.cell(200, 10, txt="Dental Treatment Plan Quotation", ln=True, align='l')  # Adjusted to 10 instead of 40 for better control
    
    # Reduce gap after title (decrease this value to bring content closer)
    pdf.ln(20)  # Adjust this value to bring up the content closer to the title
    
    # Additional info without bold, size 12
    if additional_info:
        pdf.set_font("Arial", size=12)  # Set font to size 12 and no bold
        pdf.multi_cell(0, 10, txt=additional_info)
        pdf.ln(20)
        
    for phase in ["Stabilisation Phase", "Restoration Phase", "Rehabilitation Phase"]:
        phase_treatments = [t for t in selected_treatments if t[0] == phase]
        if phase_treatments:
            display_summary_by_phase(phase, phase_treatments, pdf=pdf)
            
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt=f"Total Investment: £{total_cost:.2f}", ln=True)
    
    # Save and preview PDF
    pdf_output = "dental_treatment_plan.pdf"
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as file:
        pdf_data = file.read()
    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_output}">Download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
