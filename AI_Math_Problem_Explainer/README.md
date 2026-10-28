# AI Math Problem Explainer and Error Checker

A student capstone starter project for evaluating how reliably free AI tools solve mathematics problems and explain their work.

## What's included
- `data/problem_set.csv`: 30 reference problems across algebra, probability, and basic calculus.
- `data/results_template.csv`: a 270-row experiment template (30 problems × 3 tools × 3 prompt conditions).
- `prompts/prompt_library.md`: plain, step-by-step, and self-verification prompts.
- `src/analyze_results.py`: calculates accuracy summaries and creates charts from completed results.
- `src/validate_problem_set.py`: basic checks for the problem-set CSV.
- `presentation/slide_outline.md`: seven-slide presentation outline.
- `reports/report_template.md`: report structure and conclusion template.
- `requirements.txt`: Python dependencies.

## Quick start
1. Extract the ZIP.
2. Open `data/results_template.csv` in Google Sheets or Excel.
3. Run each problem through ChatGPT, Gemini, and Claude under each prompt condition.
4. Enter the AI final answer and scores in the results template.
5. Save the completed file as `data/results.csv`.
6. Install dependencies and run analysis:

```bash
pip install -r requirements.txt
python src/analyze_results.py --input data/results.csv --output-dir outputs
```

The script produces CSV summary tables and PNG charts in `outputs/`.

## Scoring rules
- `final_answer_score`: `1` if the final answer is correct, otherwise `0`.
- `step_accuracy_score`: `1` if all essential shown steps are correct, otherwise `0`.
- For plain-prompt answers with no meaningful working, leave step accuracy blank (not applicable).
- `error_type`: use categories such as `arithmetic`, `formula`, `algebraic`, `probability`, `calculus`, `logical`, `missing_condition`, `confident_wrong_reasoning`, or `none`.
- Do not invent or fill in AI results. Record real outputs and verify them independently.

## Important note
This is a starter kit, not a completed experiment. It does not include fabricated AI results. Model access and free-tier limits may vary. Check all answers independently before submission.
