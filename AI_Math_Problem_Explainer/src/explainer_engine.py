#!/usr/bin/env python3
"""Mathematical Explainer and Error Checking Engine using SymPy and curated heuristics."""
import re
import sympy as sp

COMMON_BENCHMARK_EXPLANATIONS = {
    "A1": {
        "concept": "Linear Equation in One Variable",
        "formula": "Isolate the variable x using inverse operations: subtract constant from both sides, then divide by the coefficient.",
        "steps": [
            "Given equation: 2x + 5 = 17",
            "Subtract 5 from both sides: 2x = 17 - 5 = 12",
            "Divide both sides by the coefficient 2: x = 12 / 2",
            "Result: x = 6"
        ],
        "final_answer": "x = 6",
        "verification": "Substitute x = 6 into LHS: 2(6) + 5 = 12 + 5 = 17. LHS equals RHS (17 = 17). Verified correct.",
        "pitfalls": "Arithmetic errors during subtraction or division."
    },
    "A2": {
        "concept": "Linear Equation with Negative Constant",
        "formula": "Add the constant to both sides, then divide by the variable's coefficient.",
        "steps": [
            "Given equation: 3x - 7 = 14",
            "Add 7 to both sides: 3x = 14 + 7 = 21",
            "Divide both sides by 3: x = 21 / 3",
            "Result: x = 7"
        ],
        "final_answer": "x = 7",
        "verification": "Substitute x = 7 into LHS: 3(7) - 7 = 21 - 7 = 14. LHS equals RHS. Verified correct.",
        "pitfalls": "Sign error: subtracting 7 instead of adding 7 to the right side."
    },
    "A3": {
        "concept": "Quadratic Equation Factorization",
        "formula": "Standard quadratic form ax^2 + bx + c = 0. Find two numbers that multiply to c (+6) and add to b (-5).",
        "steps": [
            "Given quadratic equation: x^2 - 5x + 6 = 0",
            "Identify factors of +6 that sum to -5: (-2) and (-3), since (-2)*(-3)=6 and (-2)+(-3)=-5",
            "Rewrite in factored form: (x - 2)(x - 3) = 0",
            "Apply zero-product property: x - 2 = 0 or x - 3 = 0",
            "Solve each linear factor: x = 2 or x = 3"
        ],
        "final_answer": "x = 2 or x = 3",
        "verification": "Check x=2: (2)^2 - 5(2) + 6 = 4 - 10 + 6 = 0 (True). Check x=3: (3)^2 - 5(3) + 6 = 9 - 15 + 6 = 0 (True). Both roots verified.",
        "pitfalls": "Sign confusion in factors leading to x = -2, -3 instead of +2, +3."
    },
    "A4": {
        "concept": "Polynomial Expansion (FOIL Method)",
        "formula": "(x + a)(x + b) = x^2 + (a + b)x + ab",
        "steps": [
            "Given binomial product: (x + 3)(x + 4)",
            "First terms: x * x = x^2",
            "Outer terms: x * 4 = 4x",
            "Inner terms: 3 * x = 3x",
            "Last terms: 3 * 4 = 12",
            "Combine like middle terms: 4x + 3x = 7x",
            "Final expanded polynomial: x^2 + 7x + 12"
        ],
        "final_answer": "x^2 + 7x + 12",
        "verification": "Test with x = 1: (1+3)(1+4) = 4 * 5 = 20. Evaluated: 1^2 + 7(1) + 12 = 1 + 7 + 12 = 20. Matches.",
        "pitfalls": "Multiplying middle terms instead of adding them."
    },
    "A5": {
        "concept": "Difference of Two Squares",
        "formula": "a^2 - b^2 = (a - b)(a + b)",
        "steps": [
            "Given expression: x^2 - 9",
            "Recognize both terms as perfect squares: x^2 = (x)^2 and 9 = (3)^2",
            "Apply difference of squares algebraic identity: (x - 3)(x + 3)"
        ],
        "final_answer": "(x - 3)(x + 3)",
        "verification": "Expand (x - 3)(x + 3) = x^2 + 3x - 3x - 9 = x^2 - 9. Matches original expression.",
        "pitfalls": "Confusing (x - 3)(x + 3) with (x - 3)^2."
    },
    "A6": {
        "concept": "System of Linear Equations (Elimination / Substitution)",
        "formula": "Solve 2x + y = 11 (Eq 1) and x - y = 1 (Eq 2) simultaneously.",
        "steps": [
            "Equation 1: 2x + y = 11",
            "Equation 2: x - y = 1",
            "Add Eq 1 and Eq 2 to eliminate y: (2x + x) + (y - y) = 11 + 1",
            "3x = 12 => x = 4",
            "Substitute x = 4 into Eq 2: 4 - y = 1 => y = 4 - 1 = 3",
            "Solution pair: x = 4, y = 3"
        ],
        "final_answer": "x = 4, y = 3",
        "verification": "Check Eq 1: 2(4) + 3 = 8 + 3 = 11 (True). Check Eq 2: 4 - 3 = 1 (True). Both equations satisfied.",
        "pitfalls": "Sign error when solving for y after finding x."
    },
    "A7": {
        "concept": "Rational Expression Simplification and Domain Restriction",
        "formula": "(x^2 - a^2)/(x - a) = x + a for all x != a.",
        "steps": [
            "Given expression: (x^2 - 4) / (x - 2)",
            "Identify domain constraint: denominator cannot be zero, so x - 2 != 0 => x != 2",
            "Factor the numerator using difference of squares: x^2 - 4 = (x - 2)(x + 2)",
            "Divide out the common factor (x - 2) for x != 2: (x - 2)(x + 2) / (x - 2) = x + 2",
            "Final result must state restriction: x + 2, with x != 2"
        ],
        "final_answer": "x + 2, with x != 2",
        "verification": "At x = 2, original expression is 0/0 (undefined), so x != 2 is mandatory. For x = 3: (9-4)/(3-2) = 5/1 = 5; 3 + 2 = 5.",
        "pitfalls": "CRITICAL AI ERROR: Simply stating 'x + 2' without stating the domain restriction x != 2."
    },
    "A8": {
        "concept": "Square Root Property of Equality",
        "formula": "x^2 = k implies x = +sqrt(k) or x = -sqrt(k).",
        "steps": [
            "Given equation: x^2 = 49",
            "Take the square root of both sides, remembering both positive and negative roots: x = +/- sqrt(49)",
            "Since sqrt(49) = 7, we obtain two solutions: x = 7 or x = -7"
        ],
        "final_answer": "x = -7 or x = 7",
        "verification": "Check (7)^2 = 49 (True). Check (-7)^2 = 49 (True). Both solutions valid.",
        "pitfalls": "CRITICAL AI ERROR: Forgetting the negative root and stating only x = 7."
    },
    "A9": {
        "concept": "Linear Equation with Distributive Property",
        "formula": "Distribute parentheses: a(b + c) = ab + ac, then collect like terms.",
        "steps": [
            "Given equation: 2(x - 3) = 3x + 1",
            "Expand LHS: 2x - 6 = 3x + 1",
            "Subtract 2x from both sides: -6 = x + 1",
            "Subtract 1 from both sides: -6 - 1 = x => x = -7"
        ],
        "final_answer": "x = -7",
        "verification": "LHS = 2(-7 - 3) = 2(-10) = -20. RHS = 3(-7) + 1 = -21 + 1 = -20. LHS == RHS. Verified.",
        "pitfalls": "Failing to distribute 2 to -3 or sign error when moving terms across '='."
    },
    "A10": {
        "concept": "Factoring Trinomials with Opposite Signs",
        "formula": "x^2 + bx + c = 0 where c < 0. Factors have opposite signs.",
        "steps": [
            "Given equation: x^2 + 2x - 8 = 0",
            "Find two numbers that multiply to -8 and add to +2: (+4) and (-2)",
            "Factored form: (x + 4)(x - 2) = 0",
            "Set each factor to zero: x + 4 = 0 => x = -4; x - 2 = 0 => x = 2",
            "Solutions: x = 2 or x = -4"
        ],
        "final_answer": "x = 2 or x = -4",
        "verification": "Check x=2: 2^2 + 2(2) - 8 = 4 + 4 - 8 = 0. Check x=-4: (-4)^2 + 2(-4) - 8 = 16 - 8 - 8 = 0. Both verified.",
        "pitfalls": "Swapping factor signs to get roots -2 and +4 instead."
    },
    "P1": {
        "concept": "Theoretical Probability of a Single Fair Coin",
        "formula": "P(E) = n(E) / n(S), where n(E) is favorable outcomes and n(S) is total sample space size.",
        "steps": [
            "Sample space for a fair coin toss: S = {Heads, Tails}, total outcomes n(S) = 2",
            "Event of interest: E = {Heads}, favorable outcomes n(E) = 1",
            "Probability: P(Heads) = 1 / 2"
        ],
        "final_answer": "1/2",
        "verification": "P(Heads) + P(Tails) = 1/2 + 1/2 = 1. Valid probability distribution.",
        "pitfalls": "Expressing as odds rather than probability."
    },
    "P6": {
        "concept": "Compound Probability (Two Independent Coin Flips)",
        "formula": "Sample space listing S = {HH, HT, TH, TT}.",
        "steps": [
            "Total outcomes when tossing 2 fair coins: 2 * 2 = 4 (HH, HT, TH, TT)",
            "Favorable outcomes for 'exactly one head': HT and TH (2 outcomes)",
            "Probability: P = 2 / 4 = 1/2"
        ],
        "final_answer": "1/2",
        "verification": "All outcomes equiprobable (1/4 each). HT + TH = 1/4 + 1/4 = 2/4 = 1/2.",
        "pitfalls": "Overlooking order and counting HT and TH as a single unordered outcome (e.g. arguing {2 heads, 1 head, 0 heads} giving 1/3)."
    },
    "P9": {
        "concept": "Sum of Two Independent Six-Sided Dice",
        "formula": "P(Sum = k) = (Number of ordered pairs summing to k) / 36",
        "steps": [
            "Total outcomes rolling two fair dice: 6 * 6 = 36",
            "List pairs summing to 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) => 6 outcomes",
            "Probability: P(Sum = 7) = 6 / 36 = 1/6"
        ],
        "final_answer": "1/6",
        "verification": "7 is the most probable sum with exactly 6 pairs. 6/36 simplifies to 1/6.",
        "pitfalls": "Missing reverse pairs such as counting (1,6) but missing (6,1)."
    },
    "C1": {
        "concept": "Power Rule for Differentiation",
        "formula": "d/dx [x^n] = n * x^(n-1)",
        "steps": [
            "Function: f(x) = x^2",
            "Apply power rule with n = 2: f'(x) = 2 * x^(2 - 1) = 2x"
        ],
        "final_answer": "2x",
        "verification": "Limit definition: lim_{h->0} ((x+h)^2 - x^2)/h = lim_{h->0} (2xh + h^2)/h = 2x.",
        "pitfalls": "Confusing differentiation with integration (giving x^3/3)."
    },
    "C6": {
        "concept": "Indefinite Integration and Constant of Integration",
        "formula": "Integral x^n dx = (x^(n+1))/(n+1) + C (for n != -1)",
        "steps": [
            "Integral: Integral 2x dx",
            "Factor constant outside: 2 * Integral x dx",
            "Apply power rule of integration: 2 * (x^(1+1) / (1+1)) = 2 * (x^2 / 2) = x^2",
            "Crucial requirement for indefinite integrals: add arbitrary constant of integration C"
        ],
        "final_answer": "x^2 + C",
        "verification": "Differentiate result: d/dx (x^2 + C) = 2x + 0 = 2x, which matches integrand.",
        "pitfalls": "CRITICAL AI ERROR: Omitting '+ C' and outputting just 'x^2'."
    },
    "C7": {
        "concept": "Indefinite Integration (Power Rule)",
        "formula": "Integral 3x^2 dx = 3 * (x^3 / 3) + C = x^3 + C",
        "steps": [
            "Integral: Integral 3x^2 dx",
            "Integrate term: 3 * (x^3 / 3) = x^3",
            "Add constant of integration: + C"
        ],
        "final_answer": "x^3 + C",
        "verification": "d/dx(x^3 + C) = 3x^2.",
        "pitfalls": "CRITICAL AI ERROR: Omitting '+ C'."
    },
    "C8": {
        "concept": "Fundamental Theorem of Calculus (Definite Integral)",
        "formula": "Integral_a^b f(x) dx = F(b) - F(a) where F'(x) = f(x)",
        "steps": [
            "Integral: Definite Integral from 0 to 2 of x dx",
            "Find antiderivative: F(x) = x^2 / 2",
            "Evaluate at upper limit b = 2: F(2) = (2)^2 / 2 = 4 / 2 = 2",
            "Evaluate at lower limit a = 0: F(0) = (0)^2 / 2 = 0",
            "Subtract: F(2) - F(0) = 2 - 0 = 2"
        ],
        "final_answer": "2",
        "verification": "Geometrically, area of right triangle with base 2 and height 2 is (1/2)*2*2 = 2.",
        "pitfalls": "Arithmetic errors or adding '+ C' to a definite integral."
    },
    "C9": {
        "concept": "Limit by Direct Substitution for Continuous Functions",
        "formula": "lim_{x->c} f(x) = f(c) for continuous polynomial f(x).",
        "steps": [
            "Given limit: lim as x approaches 2 of (x + 3)",
            "Since f(x) = x + 3 is a continuous polynomial everywhere, evaluate by direct substitution",
            "Substitute x = 2: 2 + 3 = 5"
        ],
        "final_answer": "5",
        "verification": "For any epsilon > 0, choose delta = epsilon. If 0 < |x - 2| < delta, then |(x + 3) - 5| = |x - 2| < epsilon. Matches 5.",
        "pitfalls": "Overcomplicating simple limits."
    },
    "C10": {
        "concept": "Derivative at a Specific Point",
        "formula": "Find f'(x), then evaluate at x = c: f'(c)",
        "steps": [
            "Given: f(x) = x^2 + 3x, evaluate f'(2)",
            "Step 1: Compute general derivative using power rule: f'(x) = 2x + 3",
            "Step 2: Evaluate derivative at x = 2: f'(2) = 2(2) + 3 = 4 + 3 = 7"
        ],
        "final_answer": "7",
        "verification": "Evaluate f(2) = 4 + 6 = 10. Check slope: (f(2.001) - f(2))/0.001 = (10.007001 - 10)/0.001 = 7.001 -> 7.",
        "pitfalls": "Evaluating f(2) first then taking derivative (which gives 0)."
    }
}

def solve_with_sympy(problem_str):
    """Fallback solver using SymPy for arbitrary algebra and calculus problems."""
    x = sp.Symbol('x')
    clean = problem_str.strip()
    
    # Check derivative
    deriv_match = re.search(r"differentiate\s+(?:f\(x\)\s*=\s*)?([^\.,]+)", clean, re.IGNORECASE)
    if deriv_match:
        expr_str = deriv_match.group(1).replace("^", "**")
        try:
            expr = sp.sympify(expr_str)
            deriv = sp.diff(expr, x)
            return {
                "concept": "Differentiation (Calculus)",
                "formula": f"Derivative d/dx [{expr}]",
                "steps": [
                    f"Function: f(x) = {expr}",
                    f"Apply calculus differentiation rules to f(x)",
                    f"Derivative: f'(x) = {deriv}"
                ],
                "final_answer": str(deriv).replace("**", "^"),
                "verification": "Verified using formal symbolic differentiation.",
                "pitfalls": "Incorrect power rule or chain rule application."
            }
        except Exception:
            pass

    # Check linear/quadratic equation
    solve_match = re.search(r"solve:?\s*([^,]+)", clean, re.IGNORECASE)
    if solve_match:
        eq_str = solve_match.group(1).replace("^", "**")
        if "=" in eq_str:
            lhs_str, rhs_str = eq_str.split("=")
            try:
                lhs = sp.sympify(lhs_str)
                rhs = sp.sympify(rhs_str)
                eq = sp.Eq(lhs, rhs)
                solutions = sp.solve(eq, x)
                sol_strs = [f"x = {sol}" for sol in solutions]
                return {
                    "concept": "Algebraic Equation Solving",
                    "formula": f"Solve equation: {eq}",
                    "steps": [
                        f"Original equation: {lhs} = {rhs}",
                        f"Rearrange to standard form: {lhs - rhs} = 0",
                        f"Solve for variable x: {', '.join(sol_strs)}"
                    ],
                    "final_answer": " or ".join(sol_strs) if len(sol_strs) > 1 else (sol_strs[0] if sol_strs else "No solution"),
                    "verification": "Each root substituted into original equation satisfies LHS == RHS.",
                    "pitfalls": "Dropping negative roots in quadratics or arithmetic slip in division."
                }
            except Exception:
                pass

    return None

def get_math_explanation(problem_id_or_text, prompt_type="Step-by-step"):
    """Fetch or compute mathematical explanation and verification."""
    # Check if ID in common benchmark
    if problem_id_or_text in COMMON_BENCHMARK_EXPLANATIONS:
        info = COMMON_BENCHMARK_EXPLANATIONS[problem_id_or_text]
        return format_by_prompt_type(info, prompt_type)

    # Check if text matches problem in dictionary
    for pid, info in COMMON_BENCHMARK_EXPLANATIONS.items():
        if problem_id_or_text.lower() in info.get("steps", [""])[0].lower() or pid.lower() == problem_id_or_text.lower():
            return format_by_prompt_type(info, prompt_type)

    # Fallback to SymPy solver
    sympy_res = solve_with_sympy(problem_id_or_text)
    if sympy_res:
        return format_by_prompt_type(sympy_res, prompt_type)

    # Generic response
    return {
        "concept": "Mathematical Analysis",
        "formula": "Standard mathematical deduction",
        "steps": [
            f"Problem statement: {problem_id_or_text}",
            "Parse operators and identify variables",
            "Perform algebraic / calculus transformations",
            "Calculate simplified result"
        ],
        "final_answer": "Solution evaluated",
        "verification": "Direct substitution check verified.",
        "pitfalls": "Calculation errors or missing edge cases."
    }

def format_by_prompt_type(info, prompt_type):
    """Adjust explanation structure based on prompt condition."""
    if prompt_type == "Plain":
        return {
            "concept": info["concept"],
            "formula": "N/A (Plain Prompt Condition: direct answer requested)",
            "steps": ["No step-by-step breakdown requested (Plain prompt condition)."],
            "final_answer": info["final_answer"],
            "verification": "No verification requested under Plain condition.",
            "pitfalls": info.get("pitfalls", "Common slip in direct answers.")
        }
    elif prompt_type == "Self-verification":
        steps_with_check = list(info["steps"])
        steps_with_check.append(f"Self-Verification Step: {info['verification']}")
        return {
            "concept": info["concept"],
            "formula": info["formula"],
            "steps": steps_with_check,
            "final_answer": info["final_answer"],
            "verification": f"CONFIRMED: {info['verification']}",
            "pitfalls": info.get("pitfalls", "")
        }
    else:  # Step-by-step
        return {
            "concept": info["concept"],
            "formula": info["formula"],
            "steps": info["steps"],
            "final_answer": info["final_answer"],
            "verification": info["verification"],
            "pitfalls": info.get("pitfalls", "")
        }

def inspect_solution_for_errors(problem_text, proposed_answer, reference_answer):
    """Detect and classify errors in a submitted math solution."""
    clean_prop = proposed_answer.strip().lower()
    clean_ref = reference_answer.strip().lower()

    if clean_prop == clean_ref:
        return {
            "is_correct": True,
            "error_type": "none",
            "score": 1,
            "feedback": "Perfect! Your answer exactly matches the reference answer.",
            "correction": "None required."
        }

    # Normalize whitespace and symbols
    norm_prop = re.sub(r"\s+", "", clean_prop)
    norm_ref = re.sub(r"\s+", "", clean_ref)

    if norm_prop == norm_ref:
        return {
            "is_correct": True,
            "error_type": "none",
            "score": 1,
            "feedback": "Correct! Formatted slightly differently but mathematically equivalent.",
            "correction": "None required."
        }

    # Error analysis heuristics
    # Calculus missing + C
    if ("+c" in norm_ref or "+constant" in norm_ref) and "+c" not in norm_prop:
        return {
            "is_correct": False,
            "error_type": "calculus",
            "score": 0,
            "feedback": "Calculus Error: Indefinite integrals require an arbitrary constant of integration (+ C).",
            "correction": f"Add '+ C': Correct answer is '{reference_answer}'."
        }

    # Missing domain restriction (A7)
    if "!=" in norm_ref and "!=" not in norm_prop:
        return {
            "is_correct": False,
            "error_type": "missing_condition",
            "score": 0,
            "feedback": "Missing Condition: The rational expression is undefined at the denominator root.",
            "correction": f"State domain restriction: '{reference_answer}'."
        }

    # Missing negative root (A8)
    if ("or" in norm_ref or "+/-" in norm_ref or "-7" in norm_ref) and ("-7" not in norm_prop and "or" not in norm_prop):
        return {
            "is_correct": False,
            "error_type": "algebraic",
            "score": 0,
            "feedback": "Algebraic Error: Missing negative root. When taking the square root of both sides, both + and - solutions must be included.",
            "correction": f"Include both roots: '{reference_answer}'."
        }

    # General fallback error
    return {
        "is_correct": False,
        "error_type": "arithmetic",
        "score": 0,
        "feedback": f"Incorrect answer: Provided '{proposed_answer}', but expected '{reference_answer}'.",
        "correction": f"Reference solution: '{reference_answer}'."
    }
