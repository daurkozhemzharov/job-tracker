import sqlite3
from datetime import date, datetime

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


DB_NAME = "job_tracker.db"


# ---------------------------
# Database functions
# ---------------------------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            job_title TEXT NOT NULL,
            location TEXT,
            date_applied TEXT,
            status TEXT,
            salary TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_application(company, job_title, location, date_applied, status, salary, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (company, job_title, location, date_applied, status, salary, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (company, job_title, location, date_applied, status, salary, notes))
    conn.commit()
    conn.close()


def get_all_applications():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM applications ORDER BY date_applied DESC", conn)
    conn.close()
    return df


def update_application(app_id, company, job_title, location, date_applied, status, salary, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE applications
        SET company = ?, job_title = ?, location = ?, date_applied = ?, status = ?, salary = ?, notes = ?
        WHERE id = ?
    """, (company, job_title, location, date_applied, status, salary, notes, app_id))
    conn.commit()
    conn.close()


def delete_application(app_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()


# ---------------------------
# App setup
# ---------------------------
st.set_page_config(page_title="Job Application Tracker", layout="wide")
init_db()

st.title("Job Application Tracker")
st.caption("Track applications, manage statuses, and view analytics.")

status_options = ["Applied", "Interview", "Rejected", "Offer", "Withdrawn"]

tab1, tab2, tab3 = st.tabs(["Add Application", "Manage Applications", "Analytics"])


# ---------------------------
# Tab 1: Add application
# ---------------------------
with tab1:
    st.subheader("Add New Application")

    with st.form("add_form", clear_on_submit=True):
        company = st.text_input("Company")
        job_title = st.text_input("Job Title")
        location = st.text_input("Location")
        date_applied = st.date_input("Date Applied", value=date.today())
        status = st.selectbox("Status", status_options)
        salary = st.text_input("Salary")
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Add Application")

        if submitted:
            if company.strip() and job_title.strip():
                add_application(
                    company.strip(),
                    job_title.strip(),
                    location.strip(),
                    str(date_applied),
                    status,
                    salary.strip(),
                    notes.strip(),
                )
                st.success("Application added.")
            else:
                st.error("Company and Job Title are required.")


# ---------------------------
# Tab 2: Manage applications
# ---------------------------
with tab2:
    st.subheader("Manage Applications")

    df = get_all_applications()

    if df.empty:
        st.info("No applications yet.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_status = st.selectbox(
                "Filter by Status",
                ["All"] + status_options
            )

        with col2:
            company_search = st.text_input("Search Company")

        with col3:
            location_search = st.text_input("Search Location")

        filtered_df = df.copy()

        if filter_status != "All":
            filtered_df = filtered_df[filtered_df["status"] == filter_status]

        if company_search.strip():
            filtered_df = filtered_df[
                filtered_df["company"].str.contains(company_search, case=False, na=False)
            ]

        if location_search.strip():
            filtered_df = filtered_df[
                filtered_df["location"].str.contains(location_search, case=False, na=False)
            ]

        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("---")
        st.subheader("Edit or Delete Application")

        app_ids = filtered_df["id"].tolist()
        if app_ids:
            selected_id = st.selectbox("Select Application ID", app_ids)
            selected_row = filtered_df[filtered_df["id"] == selected_id].iloc[0]

            with st.form("edit_form"):
                edit_company = st.text_input("Company", value=selected_row["company"])
                edit_job_title = st.text_input("Job Title", value=selected_row["job_title"])
                edit_location = st.text_input("Location", value=selected_row["location"])
                edit_date_applied = st.date_input(
                    "Date Applied",
                    value=datetime.strptime(selected_row["date_applied"], "%Y-%m-%d").date()
                    if selected_row["date_applied"]
                    else date.today()
                )
                edit_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(selected_row["status"])
                    if selected_row["status"] in status_options else 0
                )
                edit_salary = st.text_input("Salary", value=selected_row["salary"] if selected_row["salary"] else "")
                edit_notes = st.text_area("Notes", value=selected_row["notes"] if selected_row["notes"] else "")

                c1, c2 = st.columns(2)
                with c1:
                    update_btn = st.form_submit_button("Update Application")
                with c2:
                    delete_btn = st.form_submit_button("Delete Application")

                if update_btn:
                    update_application(
                        selected_id,
                        edit_company.strip(),
                        edit_job_title.strip(),
                        edit_location.strip(),
                        str(edit_date_applied),
                        edit_status,
                        edit_salary.strip(),
                        edit_notes.strip(),
                    )
                    st.success("Application updated.")
                    st.rerun()

                if delete_btn:
                    delete_application(selected_id)
                    st.warning("Application deleted.")
                    st.rerun()


# ---------------------------
# Tab 3: Analytics
# ---------------------------
with tab3:
    st.subheader("Analytics Dashboard")

    df = get_all_applications()

    if df.empty:
        st.info("No data available for analytics.")
    else:
        total_apps = len(df)
        interviews = len(df[df["status"] == "Interview"])
        offers = len(df[df["status"] == "Offer"])
        rejected = len(df[df["status"] == "Rejected"])

        response_rate = ((interviews + offers + rejected) / total_apps * 100) if total_apps > 0 else 0
        offer_rate = (offers / total_apps * 100) if total_apps > 0 else 0

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total", total_apps)
        c2.metric("Interviews", interviews)
        c3.metric("Offers", offers)
        c4.metric("Rejected", rejected)
        c5.metric("Response Rate", f"{response_rate:.1f}%")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Applications by Status")
            status_counts = df["status"].value_counts()

            fig, ax = plt.subplots()
            status_counts.plot(kind="bar", ax=ax)
            ax.set_xlabel("Status")
            ax.set_ylabel("Count")
            ax.set_title("Applications by Status")
            st.pyplot(fig)

        with col2:
            st.subheader("Applications by Location")
            location_counts = df["location"].fillna("Unknown").replace("", "Unknown").value_counts().head(10)

            fig, ax = plt.subplots()
            location_counts.plot(kind="bar", ax=ax)
            ax.set_xlabel("Location")
            ax.set_ylabel("Count")
            ax.set_title("Top Locations")
            st.pyplot(fig)

        st.markdown("---")
        st.subheader("Applications by Month")

        temp_df = df.copy()
        temp_df["date_applied"] = pd.to_datetime(temp_df["date_applied"], errors="coerce")
        temp_df["month"] = temp_df["date_applied"].dt.to_period("M").astype(str)
        month_counts = temp_df["month"].value_counts().sort_index()

        fig, ax = plt.subplots()
        month_counts.plot(kind="line", marker="o", ax=ax)
        ax.set_xlabel("Month")
        ax.set_ylabel("Applications")
        ax.set_title("Applications Over Time")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("Raw Data")
        st.dataframe(df, use_container_width=True)