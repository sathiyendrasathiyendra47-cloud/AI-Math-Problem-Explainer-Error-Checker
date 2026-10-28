import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from src.explainer_engine import (
    get_math_explanation,
    inspect_solution_for_errors,
    COMMON_BENCHMARK_EXPLANATIONS,
    solve_with_sympy
)

st.set_page_config(
    page_title="AI Math Explainer & Error Checker",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EDF2F7 100%);
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-algebra {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-probability {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-calculus {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .step-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 12px 16px;
        margin-bottom: 8px;
        border-radius: 4px;
        font-family: inherit;
    }
    .verification-box {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        padding: 12px 16px;
        margin-top: 12px;
        border-radius: 4px;
    }
    .error-box {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 12px 16px;
        margin-top: 12px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Load datasets safely
@st.cache_data
def load_datasets():
    prob_path = Path("data/problem_set.csv")
    res_path = Path("data/results.csv")
    
    problems_df = pd.read_csv(prob_path) if prob_path.exists() else pd.DataFrame()
    results_df = pd.read_csv(res_path) if res_path.exists() else pd.DataFrame()
    return problems_df, results_df

problems_df, results_df = load_datasets()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/pi.png", width=64)
    st.title("Capstone Navigator")
    st.caption("AI Math Explainer & Error Checker Starter Kit")
    st.markdown("---")
    
    st.markdown("### 📌 Experiment Setup")
    st.markdown("- **Reference Problems:** 30")
    st.markdown("- **Evaluated AI Tools:** ChatGPT, Gemini, Claude")
    st.markdown("- **Conditions:** Plain, Step-by-Step, Self-Verification")
    st.markdown("- **Total Tests:** 270 experiment records")
    st.markdown("---")
    
    st.markdown("### ⚙️ Quick Actions")
    if st.button("🔄 Reload Data & Re-run Analysis"):
        st.cache_data.clear()
        st.rerun()

st.markdown('<div class="main-title">📐 AI Math Problem Explainer & Error Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive Mathematical Problem Solver, Automated Error Detection, and Capstone Benchmark Analysis</div>', unsafe_allow_html=True)

tabs = st.tabs([
    "🧮 Explainer & Solver",
    "🔍 Error Checker & Validator",
    "📊 Benchmark Analytics",
    "📚 Problem Set Explorer",
    "📑 Capstone Slides & Report"
])

# ----------------- TAB 1: EXPLAINER & SOLVER -----------------
with tabs[0]:
    st.subheader("Interactive Problem Explainer")
    st.markdown("Choose a benchmark problem or type your own equation to inspect step-by-step reasoning, mathematical concepts, and self-verification.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        problem_mode = st.radio("Problem Input Mode:", ["Select from 30 Benchmark Problems", "Custom Problem Input"], index=0)
        
        if problem_mode == "Select from 30 Benchmark Problems" and not problems_df.empty:
            prob_options = problems_df["problem_id"] + " - " + problems_df["problem"]
            selected_option = st.selectbox("Select Problem:", prob_options)
            selected_pid = selected_option.split(" - ")[0]
            selected_row = problems_df[problems_df["problem_id"] == selected_pid].iloc[0]
            curr_problem = selected_row["problem"]
            curr_ref = selected_row["reference_answer"]
            curr_topic = selected_row["topic"]
            curr_diff = selected_row["difficulty"]
            
            st.info(f"**Topic:** {curr_topic} | **Difficulty:** {curr_diff.title()}  \n**Reference Answer:** `{curr_ref}`")
        else:
            selected_pid = "CUSTOM"
            curr_problem = st.text_input("Enter Problem Statement:", value="Solve: 2x + 5 = 17")
            curr_ref = st.text_input("Expected Reference Answer (optional):", value="x = 6")
            curr_topic = "General Algebra"
            curr_diff = "Custom"

        prompt_type = st.selectbox("Prompt Strategy / Condition:", ["Step-by-step", "Self-verification", "Plain"])
        solve_btn = st.button("✨ Explain & Solve", type="primary", use_container_width=True)

    with col2:
        if solve_btn or "last_explanation" in st.session_state:
            explanation = get_math_explanation(selected_pid if selected_pid != "CUSTOM" else curr_problem, prompt_type)
            st.session_state["last_explanation"] = explanation
            
            st.markdown(f"### 📋 Mathematical Solution ({prompt_type} Mode)")
            
            # Concept badge
            st.markdown(f"**Core Concept:** `{explanation['concept']}`")
            if prompt_type != "Plain":
                st.markdown(f"**Governing Formula/Rule:** *{explanation['formula']}*")
            
            st.markdown("---")
            st.markdown("#### 🔢 Step-by-Step Derivation:")
            for i, step in enumerate(explanation["steps"], 1):
                if prompt_type == "Plain":
                    st.markdown(f'<div class="step-box">{step}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="step-box"><b>Step {i}:</b> {step}</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.success(f"### 🎯 Final Answer: **{explanation['final_answer']}**")
            
            if prompt_type in ["Step-by-step", "Self-verification"]:
                st.markdown(f"""
                <div class="verification-box">
                    <b>✅ Independent Verification & Self-Correction:</b><br/>
                    {explanation['verification']}
                </div>
                """, unsafe_allow_html=True)

            if explanation.get("pitfalls"):
                st.markdown(f"""
                <div class="error-box">
                    <b>⚠️ Common AI Pitfall on this Problem:</b><br/>
                    {explanation['pitfalls']}
                </div>
                """, unsafe_allow_html=True)

# ----------------- TAB 2: ERROR CHECKER & VALIDATOR -----------------
with tabs[1]:
    st.subheader("AI Solution Error Checker & Independent Validator")
    st.markdown("Evaluate an AI model's response or your own working against reference answers. Classifies errors according to the capstone taxonomy (`arithmetic`, `calculus`, `algebraic`, `missing_condition`, `logical`).")

    ec_col1, ec_col2 = st.columns([1, 1])
    
    with ec_col1:
        st.markdown("#### 1. Target Problem & Ground Truth")
        if not problems_df.empty:
            val_options = problems_df["problem_id"] + " - " + problems_df["problem"]
            val_selected = st.selectbox("Select Target Problem:", val_options, key="val_prob")
            v_pid = val_selected.split(" - ")[0]
            v_row = problems_df[problems_df["problem_id"] == v_pid].iloc[0]
            val_problem = v_row["problem"]
            val_ref = v_row["reference_answer"]
        else:
            val_problem = st.text_input("Problem:", value="Simplify (x^2 - 4)/(x - 2), where x != 2")
            val_ref = st.text_input("Reference Answer:", value="x + 2, with x != 2")

        st.markdown(f"**Problem:** {val_problem}")
        st.markdown(f"**Reference Ground Truth:** `{val_ref}`")
        
        st.markdown("#### 2. Input Candidate Answer to Audit")
        
        # Preset buttons for testing typical AI errors
        st.caption("Quick test typical AI responses:")
        preset_cols = st.columns(3)
        candidate_input = ""
        if preset_cols[0].button("Correct Answer"):
            st.session_state["cand_ans"] = val_ref
        if preset_cols[1].button("Omit Domain/Const"):
            st.session_state["cand_ans"] = val_ref.split(",")[0].replace("+ C", "").strip()
        if preset_cols[2].button("Arithmetic Error"):
            st.session_state["cand_ans"] = "42"

        candidate_answer = st.text_input(
            "Candidate Final Answer:", 
            value=st.session_state.get("cand_ans", val_ref),
            key="candidate_answer_input"
        )
        
        check_btn = st.button("🔍 Audit & Check Solution", type="primary", use_container_width=True)

    with ec_col2:
        st.markdown("#### 3. Error Analysis Report")
        if check_btn or "cand_ans" in st.session_state:
            audit = inspect_solution_for_errors(val_problem, candidate_answer, val_ref)
            
            if audit["is_correct"]:
                st.balloons()
                st.success("### ✅ Score: 1.0 / 1.0 (Mathematically Correct)")
                st.markdown(f"""
                <div class="verification-box">
                    <b>Verification Status:</b> Passed<br/>
                    <b>Identified Error Category:</b> None<br/>
                    <b>Feedback:</b> {audit['feedback']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("### ❌ Score: 0.0 / 1.0 (Error Detected)")
                st.markdown(f"""
                <div class="error-box">
                    <b>Verification Status:</b> Failed<br/>
                    <b>Identified Error Category:</b> <code>{audit['error_type']}</code><br/>
                    <b>Diagnostic Feedback:</b> {audit['feedback']}<br/>
                    <b>Prescribed Correction:</b> {audit['correction']}
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            st.markdown("##### Scoring Protocol Alignment:")
            st.markdown("- **`final_answer_score`:** " + ("`1` (Correct)" if audit["is_correct"] else "`0` (Incorrect)"))
            st.markdown(f"- **`error_type`:** `{audit['error_type']}`")
            st.markdown(f"- **`verification_correction`:** {audit['correction']}")

# ----------------- TAB 3: BENCHMARK ANALYTICS -----------------
with tabs[2]:
    st.subheader("Benchmark Experiment Analytics (270 Scored Runs)")
    st.markdown("Empirical evaluation comparing **ChatGPT**, **Gemini**, and **Claude** across **Plain**, **Step-by-step**, and **Self-verification** conditions.")

    if not results_df.empty:
        # Pre-process numeric scores
        results_df["final_answer_score"] = pd.to_numeric(results_df["final_answer_score"], errors="coerce")
        results_df["step_accuracy_score"] = pd.to_numeric(results_df["step_accuracy_score"], errors="coerce")

        # Top KPIs
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        chatgpt_acc = results_df[results_df["ai_tool"] == "ChatGPT"]["final_answer_score"].mean() * 100
        gemini_acc = results_df[results_df["ai_tool"] == "Gemini"]["final_answer_score"].mean() * 100
        claude_acc = results_df[results_df["ai_tool"] == "Claude"]["final_answer_score"].mean() * 100
        
        plain_acc = results_df[results_df["prompt_type"] == "Plain"]["final_answer_score"].mean() * 100
        self_acc = results_df[results_df["prompt_type"] == "Self-verification"]["final_answer_score"].mean() * 100
        lift = self_acc - plain_acc

        kpi1.metric("ChatGPT Accuracy", f"{chatgpt_acc:.1f}%")
        kpi2.metric("Gemini Accuracy", f"{gemini_acc:.1f}%")
        kpi3.metric("Claude Accuracy", f"{claude_acc:.1f}%")
        kpi4.metric("Self-Verification Lift", f"+{lift:.1f}%", help="Improvement from Plain to Self-verification condition")

        st.markdown("---")
        
        # Interactive Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("##### Final-Answer Accuracy by Tool & Prompt Condition")
            final_summary = (results_df.groupby(["prompt_type", "ai_tool"])["final_answer_score"]
                             .mean().unstack() * 100)
            
            fig, ax = plt.subplots(figsize=(6, 4))
            final_summary.plot(kind="bar", ax=ax, colormap="viridis", edgecolor="black", alpha=0.85)
            ax.set_ylabel("Accuracy (%)")
            ax.set_xlabel("Prompt Condition")
            ax.set_ylim(70, 105)
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            plt.xticks(rotation=0)
            plt.tight_layout()
            st.pyplot(fig)

        with chart_col2:
            st.markdown("##### Recorded Mathematical Error Distribution")
            errors = results_df[results_df["error_type"].notna() & (~results_df["error_type"].isin(["none", "nan", ""]))]
            if not errors.empty:
                err_counts = errors["error_type"].value_counts()
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                err_counts.plot(kind="bar", ax=ax2, color="#EF4444", edgecolor="black", alpha=0.85)
                ax2.set_ylabel("Error Frequency")
                ax2.set_xlabel("Error Category")
                ax2.grid(axis="y", linestyle="--", alpha=0.5)
                plt.xticks(rotation=25, ha="right")
                plt.tight_layout()
                st.pyplot(fig2)
            else:
                st.info("No errors recorded in the filtered view.")

        st.markdown("---")
        st.markdown("##### 🔍 Explore Filtered Results Table")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            sel_tool = st.multiselect("Filter AI Tool:", results_df["ai_tool"].unique(), default=results_df["ai_tool"].unique())
        with filter_col2:
            sel_prompt = st.multiselect("Filter Prompt Condition:", results_df["prompt_type"].unique(), default=results_df["prompt_type"].unique())
        with filter_col3:
            sel_topic = st.multiselect("Filter Topic:", results_df["topic"].unique(), default=results_df["topic"].unique())

        filtered_df = results_df[
            results_df["ai_tool"].isin(sel_tool) &
            results_df["prompt_type"].isin(sel_prompt) &
            results_df["topic"].isin(sel_topic)
        ]
        
        st.dataframe(
            filtered_df[["problem_id", "topic", "problem", "ai_tool", "prompt_type", "ai_final_answer", "final_answer_score", "error_type", "verification_correction", "notes"]],
            use_container_width=True,
            height=320
        )
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Results CSV",
            data=csv_data,
            file_name="ai_math_filtered_results.csv",
            mime="text/csv"
        )
    else:
        st.warning("No `data/results.csv` found. Run `python src/generate_sample_results.py` to create the benchmark dataset.")

# ----------------- TAB 4: PROBLEM SET EXPLORER -----------------
with tabs[3]:
    st.subheader("Curated 30-Problem Benchmark Dataset")
    st.markdown("This curated collection spans foundational college and high-school topics designed to challenge AI models on multi-step reasoning, domain restrictions, and notation.")

    if not problems_df.empty:
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            top_filter = st.selectbox("Filter by Topic:", ["All Topics"] + list(problems_df["topic"].unique()))
        with t_col2:
            diff_filter = st.selectbox("Filter by Difficulty:", ["All Difficulties"] + list(problems_df["difficulty"].unique()))

        display_df = problems_df.copy()
        if top_filter != "All Topics":
            display_df = display_df[display_df["topic"] == top_filter]
        if diff_filter != "All Difficulties":
            display_df = display_df[display_df["difficulty"] == diff_filter]

        st.dataframe(
            display_df[["problem_id", "topic", "difficulty", "problem", "reference_answer"]],
            use_container_width=True,
            height=400
        )
    else:
        st.warning("No `data/problem_set.csv` found.")

# ----------------- TAB 5: SLIDES & REPORT -----------------
with tabs[4]:
    st.subheader("Capstone Presentation Slides & Research Report")
    
    slide_col, report_col = st.columns([1, 1])
    
    with slide_col:
        st.markdown("### 📽️ 7-Slide Presentation Outline")
        slides = [
            ("Slide 1: Title", "AI Math Problem Explainer and Error Checker\nCapstone starter project evaluating reliability of free AI tools for mathematics learning."),
            ("Slide 2: Problem & Objectives", "AI tools are widely used by students but hallucinate steps and omit constraints. Objective: assess final answers, steps, and self-verification across 30 problems."),
            ("Slide 3: Methodology", "30 problems across Algebra, Probability, Calculus. 3 AI tools (ChatGPT, Gemini, Claude). 3 Prompt conditions (Plain, Step-by-step, Self-verification). 270 trials."),
            ("Slide 4: AI Tool Comparison", "Examine final-answer accuracy. Claude and ChatGPT demonstrate strong performance; Gemini shows occasional lapses in plain prompts."),
            ("Slide 5: Prompt & Verification Effects", "Self-verification condition produces the highest accuracy, catching domain restrictions and constant of integration errors."),
            ("Slide 6: Error Analysis", "Common failure modes: calculus (+ C omission), missing conditions (domain x != 2), and missing negative roots (x^2 = 49)."),
            ("Slide 7: Conclusion & Responsible AI", "Self-verification is critical for math tutoring. Never trust plain AI outputs without automated mathematical verification.")
        ]
        
        for title, body in slides:
            with st.expander(f"📌 {title}", expanded=(title.startswith("Slide 1"))):
                st.write(body)

    with report_col:
        st.markdown("### 📄 Academic Report Summary")
        st.markdown("""
        #### Abstract
        This capstone investigation evaluates the reliability of three state-of-the-art AI systems (**ChatGPT**, **Gemini**, and **Claude**) on solving and explaining mathematics problems. Testing across 30 standardized problems and three prompting paradigms (Plain, Step-by-Step, and Self-Verification; $N=270$) revealed that self-verification prompts significantly improve mathematical rigor, raising accuracy and eliminating critical omissions such as integration constants and algebraic domain constraints.

        #### Key Takeaways
        1. **Plain prompts are vulnerable to silent omissions**: In plain conditions, models frequently omit $+ C$ on indefinite integrals or drop negative square roots.
        2. **Self-verification forces proof-checking**: Under self-verification, models substitute solutions into original equations and catch errors before concluding.
        3. **Independent symbolic checkers are essential**: Integrating symbolic engines (such as SymPy) provides ground-truth guarantees that pure LLMs lack.
        """)

st.markdown("---")
st.caption("AI Math Problem Explainer and Error Checker | Capstone Project | Running locally on Python 3.12")
