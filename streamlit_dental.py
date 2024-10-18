import streamlit as st

# Set the page layout to wide mode
st.set_page_config(layout="wide",page_icon="🪥",page_title="Dental Treatment Plan")

# Header with total cost box
header_col1, header_col2 = st.columns([6, 1])
with header_col1:
    st.header("Dental Treatment Plan")

# Initialize total cost
total_cost = 0

st.divider()

# Define a structure for upper and lower teeth, organized by quadrants
upper_right = ['UR8', 'UR7', 'UR6', 'UR5', 'UR4', 'UR3', 'UR2', 'UR1']
upper_left = ['UL1', 'UL2', 'UL3', 'UL4', 'UL5', 'UL6', 'UL7', 'UL8']
lower_right = ['LR8', 'LR7', 'LR6', 'LR5', 'LR4', 'LR3', 'LR2', 'LR1']
lower_left = ['LL1', 'LL2', 'LL3', 'LL4', 'LL5', 'LL6', 'LL7', 'LL8']

# Create empty dictionary to store treatment status
teeth_status = {}

# Create three columns: one for upper right, one as a spacer, and one for upper left
col1, spacer, col2 = st.columns([2, 0.1, 2])  # Adjust the size of columns: 8 for content, 1 for space

# Display Upper Right Teeth in the first column
with col1:
    st.write("Upper Right Teeth")
    cols = st.columns(8)  # Create 8 columns for the 8 upper right teeth
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
col3, spacer2, col4 = st.columns([2, 0.1, 2])  # Adjust the size of columns: 8 for content, 1 for space

# Display lower Right Teeth in the first column
with col3:
    st.write("Lower Right Teeth")
    cols = st.columns(8)  # Create 8 columns for the 8 lower right teeth
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

# Display options for Stabilisation and Restoration phases
stabilisation_data = []
for tooth, selected in teeth_status.items():
    if selected:
        # Ask if Stabilisation Phase is needed
        st.divider()
        st.subheader(f"Treatment for {tooth}")
        stab_yes_no, rest_yes_no, spacey = st.columns([1,1,3])
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
            header_cols[0].write("Stabilisation Phase")
            col_treatment, col_time, col_cost = st.columns([2, 1, 1])
            treatment_option = col_treatment.selectbox(
                "Treatment Required",
                ["Please select", "Composite", "Extirpation", "GIC", "Specialist XLA", "XLA"],
                key=f"treatment_{tooth}_stab"
            )
            time_required = col_time.number_input(
                "Time Required (minutes)",
                min_value=0,
                max_value=120,
                step=15,
                key=f"time_{tooth}_stab"
            )
            # Determine rate based on treatment option
            if treatment_option == "Specialist XLA":
                rate = 400 / 60
            else:
                rate = 5.5
            cost = time_required * rate
            col_cost.text_input("Cost", value=f"£{cost:.2f}", disabled=True, key=f"cost_{tooth}_stab")
            total_cost += cost
            stabilisation_data.append((tooth, treatment_option, time_required, cost))

            # Add second treatment option if XLA is selected
            if treatment_option == "XLA":
                st.write("Second Treatment Option")
                col_treatment_2, col_time_2, col_lab_fee, col_cost_2 = st.columns([2, 1, 1, 1])
                second_treatment = col_treatment_2.selectbox(
                    "Treatment Required",
                    ["Please select", "Immediate denture", "Rochette Bridge"],
                    key=f"second_treatment_{tooth}"
                )
                second_time_required = col_time_2.number_input(
                    "Time Required (minutes)",
                    min_value=0,
                    max_value=120,
                    step=15,
                    key=f"second_time_{tooth}"
                )
                lab_fee = col_lab_fee.number_input(
                    "Lab Fee (£)",
                    min_value=0.0,
                    step=0.5,
                    key=f"lab_fee_{tooth}"
                )
                second_cost = (second_time_required * 5.5) + lab_fee
                col_cost_2.text_input("Cost", value=f"£{second_cost:.2f}", disabled=True, key=f"second_cost_{tooth}")
                total_cost += second_cost

        # Restoration Phase
        if restoration_required == "Yes":
            header_cols = st.columns([1])
            header_cols[0].write("Restoration Phase")
            col_treatment, col_time, col_cost = st.columns([2, 1, 1])
            restoration_option = col_treatment.selectbox(
                "Treatment Required",
                ["Please select", "Bridge", "Crown", "Filling", "Implant", "RCT"],
                key=f"treatment_{tooth}_rest"
            )
            time_required = col_time.number_input(
                "Time Required (minutes)",
                min_value=0,
                max_value=120,
                step=15,
                key=f"time_{tooth}_rest"
            )
            # Determine rate for restoration phase
            if restoration_option == "Implant":
                rate = 4000 / 60
            elif restoration_option == "RCT":
                rate = 1000 / 60
            else:
                rate = 5.5
            cost = time_required * rate
            col_cost.text_input("Cost", value=f"£{cost:.2f}", disabled=True, key=f"cost_{tooth}_rest")
            total_cost += cost

# Update total cost box
with header_col2:
    st.markdown(
        """
        <div style="background-color:#ff4b4b; padding: 10px; border-radius: 8px; text-align: center; color: white; font-size: 24px;">
            <strong>Total Cost: £{:.2f}</strong>
        </div>
        """.format(total_cost),
        unsafe_allow_html=True
    )
