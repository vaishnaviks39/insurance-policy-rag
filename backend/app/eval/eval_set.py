# Eval set generated from Reliance Critical Illness Policy Wording (policy224.pdf).

import os
DOC_ID = os.environ.get("EVAL_DOC_ID", "REPLACE_WITH_UPLOADED_DOC_ID")

EVAL_SET = [
    {
        "id": "fl_01",
        "category": "factual_lookup",
        "question": "What is the free look period for this policy?",
        "expected_answer": "15 days from the date of receipt of the policy.",
    },
    {
        "id": "fl_02",
        "category": "factual_lookup",
        "question": "What is the grace period for renewal premium payment?",
        "expected_answer": "30 days immediately following the premium due date.",
    },
    {
        "id": "fl_03",
        "category": "factual_lookup",
        "question": "Within how many days must a claim be intimated after an insured event occurs?",
        "expected_answer": "Within 7 days of the occurrence of the insured event.",
    },

    {
        "id": "nl_01",
        "category": "numeric_limit",
        "question": "Within how many days of hospital discharge must claim documents be submitted?",
        "expected_answer": "Within 15 days of discharge from the hospital.",
    },
    {
        "id": "nl_02",
        "category": "numeric_limit",
        "question": "What is the survival period requirement for Category I critical illnesses?",
        "expected_answer": "The insured must survive more than 30 days post diagnosis/occurrence/procedure.",
    },
    {
        "id": "nl_03",
        "category": "numeric_limit",
        "question": "What is the survival period requirement for Category II critical illnesses?",
        "expected_answer": "The insured must survive more than 60 days post diagnosis/occurrence/procedure.",
    },
    {
        "id": "nl_04",
        "category": "numeric_limit",
        "question": "What interest rate applies if a claim payment is delayed by more than 7 days after acceptance?",
        "expected_answer": "2% above the bank rate for the period of delay.",
    },
    {
        "id": "nl_05",
        "category": "numeric_limit",
        "question": "What percentage of the pre-policy medical check-up cost does the company reimburse?",
        "expected_answer": "50% of the cost, for check-ups at the company's designated centre.",
    },
    {
        "id": "nl_06",
        "category": "numeric_limit",
        "question": "What is the maximum no-claim discount available on an annual policy?",
        "expected_answer": "Up to 50%, accumulated at 5% for each continuous claim-free year.",
    },
    {
        "id": "nl_07",
        "category": "numeric_limit",
        "question": "If the policyholder cancels within 1 month of the policy start date, what percentage of premium is refunded?",
        "expected_answer": "75% of the premium.",
    },

    {
        "id": "ex_01",
        "category": "exclusion",
        "question": "Is cosmetic surgery covered under this policy?",
        "expected_answer": "No, cosmetic surgery or treatment (and sex-change treatment/surgery) is excluded.",
    },
    {
        "id": "ex_02",
        "category": "exclusion",
        "question": "Are illnesses related to alcohol or drug abuse covered?",
        "expected_answer": "No, critical illness due to alcohol, smoking, tobacco, or drug abuse is excluded.",
    },
    {
        "id": "ex_03",
        "category": "exclusion",
        "question": "Is a critical illness caused by HIV infection covered?",
        "expected_answer": "No, critical illness acquired as a consequence of HIV infection is excluded.",
    },
    {
        "id": "ex_04",
        "category": "exclusion",
        "question": "Does the policy cover treatment received outside India?",
        "expected_answer": "No, reimbursement for treatment/procedures performed outside India is excluded.",
    },
    {
        "id": "ex_05",
        "category": "exclusion",
        "question": "Are self-inflicted injuries or suicide attempts covered?",
        "expected_answer": "No, excluded under the general exclusions.",
    },

    {
        "id": "cd_01",
        "category": "condition",
        "question": "What happens to a claim if the insured dies within the survival period for their category?",
        "expected_answer": "No claim is payable if the insured dies within the stipulated survival period for that category (30 days for Category I, 60 days for Category II).",
    },
    {
        "id": "cd_02",
        "category": "condition",
        "question": "What documents are required to support a critical illness claim?",
        "expected_answer": "Signed claim form, medical practitioner's referral letter, prescriptions, discharge card, original pathology/diagnostic reports and receipts, indoor case papers, and (if applicable) FIR or post-mortem report.",
    },
    {
        "id": "cd_03",
        "category": "condition",
        "question": "Under what condition is the free-look refund reduced?",
        "expected_answer": "If risk has already commenced when the policy is returned, the refund is reduced for proportionate risk premium and any medical exam/stamp duty costs; no refund at all if a claim has already been made.",
    },

    {
        "id": "cdx_01",
        "category": "category_distinction",
        "question": "If an insured undergoes a kidney transplant, is the benefit paid under Kidney Failure or Major Organ Transplant?",
        "expected_answer": "Under Major Organ Transplant (Category I), not under Kidney Failure Requiring Regular Dialysis.",
    },
    {
        "id": "cdx_02",
        "category": "category_distinction",
        "question": "Is Coma of Specified Severity a Category I or Category II insured event?",
        "expected_answer": "Category II.",
    },
    {
        "id": "cdx_03",
        "category": "category_distinction",
        "question": "Is Cancer of Specified Severity a Category I or Category II insured event?",
        "expected_answer": "Category I.",
    },

    {
        "id": "ms_01",
        "category": "multi_source",
        "question": "If someone ports from another insurer with 2 years of continuous coverage, how does that affect waiting periods, and is there a separate liability cap for portability claims?",
        "expected_answer": "Waiting periods are reduced by the number of years of continuous prior coverage; total liability for portability claims is separately capped at the Portability Sum Insured Limit stated in the Schedule.",
    },
    {
        "id": "ms_02",
        "category": "multi_source",
        "question": "Does the free-look period apply if I'm renewing my policy, and what's the alternative cancellation refund schedule?",
        "expected_answer": "Free look does not apply on renewal or portability; a policyholder-initiated mid-term cancellation instead follows the short-period refund scale (75% up to 1 month, 50% up to 3 months, 25% up to 6 months).",
    },

    {
        "id": "ci_01",
        "category": "conflicting_info",
        "question": "If the Policy Schedule and the Policy Wording disagree on a term, which one prevails?",
        "expected_answer": "The Policy Schedule prevails, per the Overriding Effect of Policy Schedule clause.",
    },

    {
        "id": "oos_01",
        "category": "out_of_scope",
        "question": "Which hospitals near me accept this policy for cashless treatment?",
        "expected_answer": "The provided policy sources do not contain enough information to answer this question.",
    },
    {
        "id": "oos_02",
        "category": "out_of_scope",
        "question": "What is today's USD to INR exchange rate?",
        "expected_answer": "The provided policy sources do not contain enough information to answer this question.",
    },

    {
        "id": "pr_01",
        "category": "paraphrase_robustness",
        "question": "How many days do I have after my premium is due to still pay it without losing coverage?",
        "expected_answer": "30 days (the grace period) — same fact as fl_02.",
    },
    {
        "id": "pr_02",
        "category": "paraphrase_robustness",
        "question": "After being diagnosed with a Category I critical illness, how long do I need to survive for the benefit to be paid?",
        "expected_answer": "More than 30 days — same fact as nl_02.",
    },
]

SELECTED_IDS = {
    "fl_01",
    "nl_02",
    "ex_01",
    "cd_01",
    "cdx_01",
    "ms_01",
    "oos_02",
    "pr_02",
}

EVAL_SET = [case for case in EVAL_SET if case["id"] in SELECTED_IDS]