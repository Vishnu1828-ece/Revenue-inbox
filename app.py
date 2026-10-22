import json
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Revenue Intelligence Inbox", page_icon="📊", layout="wide"
)

# --- 1. INITIALIZE SESSION STATE DATA (Mock Database) ---
if "calls_df" not in st.session_state:
  initial_data = [
      {
          "call_id": "CALL-101",
          "rep_name": "Alice Smith",
          "account": "Acme Corp",
          "deal_value": 45000,
          "duration_min": 32,
          "rep_talk_pct": 55,
          "transcript_snippet": (
              "We like the product, but CompetitorX is offering a 20%"
              " discount."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "CALL-102",
          "rep_name": "Bob Jones",
          "account": "Globex Inc",
          "deal_value": 120000,
          "duration_min": 45,
          "rep_talk_pct": 70,
          "transcript_snippet": (
              "Budget is tight right now, too expensive for this quarter."
          ),
          "manual_override_category": None,
      },
      {
          "call_id": "CALL-103",
          "rep_name": "Alice Smith",
          "account": "Stark Industries",
          "deal_value": 85000,
          "duration_min": 20,
          "rep_talk_pct": 40,
          "transcript_snippet": (
              "Let's schedule a technical deep dive for next Tuesday. Send the"
              " proposal."
          ),
          "manual_override_category": None,
      },
  ]
  st.session_state["calls_df"] = pd.DataFrame(initial_data)


# --- 2. RULE-BASED ROUTING & ANALYSIS ENGINE (No AI) ---
def apply_rules(row):
  text = str(row["transcript_snippet"]).lower()

  has_competitor = any(
      w in text for w in ["competitor", "competitorx", "rival", "alternative"]
  )
  has_pricing = any(
      w in text
      for w in ["expensive", "discount", "budget", "cost", "price", "too high"]
  )
  has_action = any(
      w in text for w in ["schedule", "proposal", "deep dive", "follow up"]
  )

  if row["deal_value"] > 100000 and has_pricing:
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
    "Sales Manager dashboard for reviewing call activity, handling routing,"
    " and managing data updates."
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
      df[df["final_category"].isin(["Pricing Pushback", "Competitor Threat"])]
  )

  col1.metric("Total Calls Logged", total_deals)
  col2.metric("Total Pipeline Value", f"${pipeline_val:,.0f}")
  col3.metric("Avg Rep Talk Ratio", f"{avg_talk:.1f}%")
  col4.metric("At-Risk Deals Flagged", risk_calls)

  st.markdown("---")
  st.subheader("Calls Breakdown by Category")
  cat_counts = df["final_category"].value_counts()
  st.bar_chart(cat_counts)

elif tab == "Inbox & Routing":
  st.header("Conversation Routing Inbox")
  st.markdown(
      "Review flagged conversations, inspect transcripts, and apply manual"
      " routing corrections."
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
                  "Complete log of sales calls, automated categories, and"
                  " manual overrides."
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
