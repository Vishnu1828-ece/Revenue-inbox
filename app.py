import json
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Revenue Intelligence Inbox", page_icon="📊", layout="wide"
)

# --- 1. INITIALIZE SESSION STATE DATA (Enterprise Mock Database) ---
if "calls_df" not in st.session_state:
  initial_data = [
      {
          "call_id": "RI-101",
          "rep_name": "Arun Prakash",
          "account": "Sri Lakshmi Textiles Pvt Ltd - Tiruppur",
          "deal_value": 680000,
          "duration_min": 34,
          "rep_talk_pct": 52,
          "transcript_snippet": (
              "Your solution looks good, but another competitor has quoted"
              " nearly 15 percent less. Can you review the pricing before we"
              " move forward?"
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-102",
          "rep_name": "Keerthana Nair",
          "account": "Malabar Foods India - Kochi",
          "deal_value": 950000,
          "duration_min": 42,
          "rep_talk_pct": 48,
          "transcript_snippet": (
              "Budget is very limited this quarter. If the cost can be"
              " reduced, management may approve the purchase."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-103",
          "rep_name": "Sathish Kumar",
          "account": "Namma Motors Components - Hosur",
          "deal_value": 1250000,
          "duration_min": 39,
          "rep_talk_pct": 57,
          "transcript_snippet": (
              "Please schedule a technical deep dive next Monday. We will"
              " invite our engineering team before final approval."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-104",
          "rep_name": "Divya Ramesh",
          "account": "Cauvery Healthcare Systems - Bengaluru",
          "deal_value": 820000,
          "duration_min": 29,
          "rep_talk_pct": 45,
          "transcript_snippet": (
              "Everything looks good. Kindly send the commercial proposal and"
              " annual maintenance details."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-105",
          "rep_name": "Vignesh Raj",
          "account": "PSG Engineering Solutions - Coimbatore",
          "deal_value": 1580000,
          "duration_min": 47,
          "rep_talk_pct": 60,
          "transcript_snippet": (
              "CompetitorX is giving a larger discount. If you can revise your"
              " pricing, we are ready to finalize the order."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-106",
          "rep_name": "Meghana S",
          "account": "Sri Murugan Agro Industries - Salem",
          "deal_value": 540000,
          "duration_min": 26,
          "rep_talk_pct": 44,
          "transcript_snippet": (
              "Please schedule a product demonstration for our operations team"
              " and share the quotation."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-107",
          "rep_name": "Harish Kumar",
          "account": "Southern Precision Castings - Coimbatore",
          "deal_value": 1100000,
          "duration_min": 36,
          "rep_talk_pct": 53,
          "transcript_snippet": (
              "The price is slightly expensive. Our finance team needs a better"
              " commercial offer before approval."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-108",
          "rep_name": "Aishwarya Menon",
          "account": "Kerala Aqua Technologies - Kochi",
          "deal_value": 760000,
          "duration_min": 31,
          "rep_talk_pct": 46,
          "transcript_snippet": (
              "We compared your product with another alternative in the market."
              " Your support looks better, but pricing is higher."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-109",
          "rep_name": "Karthik B",
          "account": "Madurai Medical Devices - Madurai",
          "deal_value": 890000,
          "duration_min": 37,
          "rep_talk_pct": 49,
          "transcript_snippet": (
              "Kindly follow up with the revised proposal. We plan to complete"
              " the purchase before month end."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-110",
          "rep_name": "Nandhini Ravi",
          "account": "Royal Furniture Industries - Chennai",
          "deal_value": 430000,
          "duration_min": 22,
          "rep_talk_pct": 41,
          "transcript_snippet": (
              "Everything is clear. We will review internally and get back to"
              " you within two weeks."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-111",
          "rep_name": "Praveen Joseph",
          "account": "Travancore Logistics - Kochi",
          "deal_value": 1850000,
          "duration_min": 48,
          "rep_talk_pct": 62,
          "transcript_snippet": (
              "Budget approval is pending because another competitor has"
              " offered a lower price. Please revise your commercial proposal."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-112",
          "rep_name": "Sneha Krishnan",
          "account": "Thanjavur Smart Farms",
          "deal_value": 590000,
          "duration_min": 24,
          "rep_talk_pct": 43,
          "transcript_snippet": (
              "Our technical team is interested. Let's schedule a detailed"
              " product walkthrough next Friday."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-113",
          "rep_name": "Rahul Dev",
          "account": "Bharath Pumps Pvt Ltd - Erode",
          "deal_value": 790000,
          "duration_min": 33,
          "rep_talk_pct": 50,
          "transcript_snippet": (
              "The product quality is excellent. However, the cost is above"
              " our expected budget."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-114",
          "rep_name": "Lakshmi Priya",
          "account": "Green Valley Hospitals - Bengaluru",
          "deal_value": 1420000,
          "duration_min": 41,
          "rep_talk_pct": 54,
          "transcript_snippet": (
              "Please arrange a technical discussion with your implementation"
              " team. We expect to close the deal this month."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "RI-115",
          "rep_name": "Suresh Babu",
          "account": "Ocean Fresh Sea Foods - Mangaluru",
          "deal_value": 610000,
          "duration_min": 28,
          "rep_talk_pct": 47,
          "transcript_snippet": (
              "We don't have any concerns regarding the product. Kindly send"
              " the agreement so that we can begin the onboarding process."
          ),
          "manual_override_category": None,
      },
  ]
  st.session_state["calls_df"] = pd.DataFrame(initial_data)


# --- 2. RULE-BASED ROUTING & ANALYSIS ENGINE (Deterministic) ---
def apply_rules(row):
  text = str(row["transcript_snippet"]).lower()

  has_competitor = any(
      w in text
      for w in ["competitor", "competitorx", "rival", "alternative", "quoted"]
  )
  has_pricing = any(
      w in text
      for w in [
          "expensive",
          "discount",
          "budget",
          "cost",
          "price",
          "too high",
          "reduced",
      ]
  )
  has_action = any(
      w in text
      for w in [
          "schedule",
          "proposal",
          "deep dive",
          "follow up",
          "walkthrough",
          "agreement",
      ]
  )

  if row["deal_value"] > 1000000 and has_pricing:
    category = "High-Value Pricing Risk"
  elif has_competitor:
    category = "Competitor Threat"
  elif has_pricing:
    category = "Pricing Pushback"
  elif has_action:
    category = "Active Deal (Next Steps Set)"
  else:
    category = "Standard Review"

  return category


df = st.session_state["calls_df"].copy()
df["auto_category"] = df.apply(apply_rules, axis=1)
df["final_category"] = df["manual_override_category"].fillna(df["auto_category"])

# --- 3. STREAMLIT USER INTERFACE ---
st.title("📊 Revenue Intelligence Inbox")
st.markdown(
    "Sales Manager dashboard for reviewing regional call activity, automated"
    " routing, and managing pipeline updates."
)

tab = st.sidebar.radio(
    "Navigation",
    ["Dashboard Metrics", "Inbox & Routing", "Import / Update Tests", "Exports"],
)

if tab == "Dashboard Metrics":
  st.header("Executive Summary Metrics")

  col1, col2, col3, col4 = st.columns(4)
  total_deals = len(df)
  pipeline_val = df["deal_value"].sum()
  avg_talk = df["rep_talk_pct"].mean()
  risk_calls = len(
      df[
          df["final_category"].isin(
              ["Pricing Pushback", "Competitor Threat", "High-Value Pricing Risk"]
          )
      ]
  )

  col1.metric("Total Calls Logged", total_deals)
  col2.metric("Total Pipeline Value", f"₹{pipeline_val:,.0f}")
  col3.metric("Avg Rep Talk Ratio", f"{avg_talk:.1f}%")
  col4.metric("At-Risk Deals Flagged", risk_calls)

  st.markdown("---")
  st.subheader("Calls Breakdown by Category")
  cat_counts = df["final_category"].value_counts()
  st.bar_chart(cat_counts)

elif tab == "Inbox & Routing":
  st.header("Conversation Routing Inbox")
  st.markdown(
      "Review flagged enterprise conversations, inspect transcripts, and apply"
      " manual routing corrections."
  )

  selected_cat = st.selectbox(
      "Filter by Routing Queue", ["All"] + list(df["final_category"].unique())
  )
  filtered_df = (
      df if selected_cat == "All" else df[df["final_category"] == selected_cat]
  )

  st.dataframe(filtered_df, use_container_width=True)

  st.subheader("Manual Override & Correction")
  call_to_edit = st.selectbox(
      "Select Call ID to Override", df["call_id"].tolist()
  )
  current_val = df.loc[df["call_id"] == call_to_edit, "final_category"].values[0]

  new_override = st.text_input(
      "Override Category / Tag",
      value=current_val,
      help="Manually adjust routing tag",
  )

  if st.button("Save Override"):
    st.session_state["calls_df"].loc[
        st.session_state["calls_df"]["call_id"] == call_to_edit,
        "manual_override_category",
    ] = new_override
    st.success(f"Successfully updated {call_to_edit}!")
    st.rerun()

elif tab == "Import / Update Tests":
  st.header("Repeated Imports & Update Testing")
  st.markdown(
      "Upload a CSV or simulate a batch update to test deduplication"
      " (UPSERT logic)."
  )

  uploaded_file = st.file_uploader(
      "Upload Call Data CSV (call_id, rep_name, account, deal_value,"
      " duration_min, rep_talk_pct, transcript_snippet)",
      type=["csv"],
  )

  if uploaded_file is not None:
    new_import_df = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:", new_import_df.head())

    if st.button("Process Import (UPSERT / Update Records)"):
      current_data = st.session_state["calls_df"]
      combined_df = pd.concat([current_data, new_import_df]).drop_duplicates(
          subset=["call_id"], keep="last"
      )
      st.session_state["calls_df"] = combined_df
      st.success(
          "Successfully imported and updated records without duplication!"
      )
      st.rerun()

elif tab == "Exports":
  st.header("Organized Data Exports & Manifest")
  st.markdown("Download clean CSV exports along with a JSON manifest file.")

  csv_data = df.to_csv(index=False)
  st.download_button(
      label="Download Full Calls CSV Export",
      data=csv_data,
      file_name="revenue_intelligence_export.csv",
      mime="text/csv",
  )

  manifest_content = {
      "generated_at": datetime.utcnow().isoformat() + "Z",
      "exported_files": [
          {
              "filename": "revenue_intelligence_export.csv",
              "row_count": len(df),
              "format": "CSV",
              "description": (
                  "Complete log of regional sales calls, automated categories,"
                  " and manual overrides."
              ),
          }
      ],
  }
  manifest_json = json.dumps(manifest_content, indent=4)

  st.download_button(
      label="Download JSON Manifest (`manifest.json`)",
      data=manifest_json,
      file_name="manifest.json",
      mime="application/json",
  )
