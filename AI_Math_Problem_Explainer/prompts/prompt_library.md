# Prompt Library

Replace `[INSERT PROBLEM]` with one problem from `data/problem_set.csv`. Use the same problem text across tools.

## Prompt 1 — Plain
Solve the following mathematics problem:

[INSERT PROBLEM]

Provide the answer.

## Prompt 2 — Step by step
Act as a mathematics tutor for a college student.

Solve the following problem:

[INSERT PROBLEM]

Requirements:
1. Identify the mathematical concept or formula required.
2. Explain the formula.
3. Show each calculation step clearly.
4. Explain why each step is valid.
5. Provide the final answer.
6. Check that the final answer satisfies the original problem.
7. State assumptions and domain restrictions where needed.

Do not skip important mathematical steps.

## Prompt 3 — Self-verification
Solve the following mathematics problem step by step:

[INSERT PROBLEM]

After solving it:
1. Substitute the answer into the original equation, where applicable.
2. Recalculate the arithmetic.
3. Verify that the correct formula was used.
4. Check for missing solutions, domain restrictions, and integration constants where applicable.
5. Identify and correct any errors in your initial solution.
6. Provide the verified final answer and explain any corrections.

Do not claim that the solution is correct unless the verification supports it.

## Experiment protocol
- Use the same 30 problems for each tool and prompt condition.
- Record tool name, date, and model/version if shown.
- Save the initial answer before asking for verification.
- Score final answer and steps separately.
- For plain answers with no meaningful working, leave step accuracy blank.
- Verify all answers independently against the reference answer and mathematical reasoning.
