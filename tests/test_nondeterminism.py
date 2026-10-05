import pytest,pydantic
from ai_api_testing.schemas import ChatCompletion

MIN_PASS_RATE = 0.9

# ---------- 1. Reliability: same factual question, many runs ----------
def test_factual_answer_is_reliable(chat):
    answers=[chat("What is the second capital of Himachal Pradesh?",temperature=0) for _ in range(10)]
    correct = sum("Dharamshala" in  i for i in answers)
    rate=correct/len(answers)
    print(f"correct:{correct}/{len(answers)})({rate:.0%}")
    assert rate >= MIN_PASS_RATE ,f"only {rate:.0%} correct;answers:{answers}"

# ---------- 2. Creative output should vary at high temperature ----------
def test_creative_answer_vary_at_high_temperature(chat):
    answer=chat("Write a short story about Hampi",temperature=1.0)
    words = answer.lower().split()
    distinct = len(set(words))
    print(f"distinct words: {distinct}/{len(words)}")
    assert distinct >= 50, f"suspiciously little variety: {answer}"

# ---------- 4. Accuracy across DIFFERENT questions, each run several times ----------
CASES = [
    ("What is the capital of France? One word.", "paris"),
    ("What is the capital of Japan? One word.", "tokyo"),
    ("What is 7 times 8? Just the number.", "56"),
    ("What is the chemical symbol for gold? Just the symbol.", "au"),
    ("How many days are in a leap year? Just the number.", "366"),
]

def test_accuracy_across_different_questions(chat):
    total=correct=0
    for questions,expected in CASES:
        answers=[chat(questions,temperature=0) for _ in range(3)]
        hits=sum(expected in a.lower() for a in answers)
        print(f"{questions[:45]:45}{hits}/3")
        total+=len(answers)
        correct+=hits
        accuracy=correct/total
        print(f"overall accuracy:{correct/total}({accuracy:.0%})")
        assert accuracy >= MIN_PASS_RATE