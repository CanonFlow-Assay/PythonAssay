"""Effect shell: execute the declared named acceptance selection."""
import sys
from expense import Approved, NeedsReview, Invalid, decide

CASES = [["approved","R5",2500,"USD","lunch",10000,"Approved",2500,""],["negative","R2",-1,"USD","lunch",10000,"Invalid",0,"amount"],["over-limit","R5",10001,"USD","lunch",10000,"NeedsReview",10001,""],["currency","R3",2500,"EUR","lunch",10000,"Invalid",0,"currency"],["empty-memo","R4",2500,"USD","",10000,"Invalid",0,"memo"],["zero-policy","R1",2500,"USD","lunch",0,"Invalid",0,"policy"],["zero-amount","R2",0,"USD","lunch",10000,"Invalid",0,"amount"],["exact-limit","R5",10000,"USD","lunch",10000,"Approved",10000,""],["smallest-amount","R2",1,"USD","lunch",10000,"Approved",1,""],["blank-memo","R4",2500,"USD"," \t",10000,"Invalid",0,"memo"],["negative-policy","R1",2500,"USD","lunch",-1,"Invalid",0,"policy"],["large-amount","R5",2147483647,"USD","lunch",10000,"NeedsReview",2147483647,""]]

def main() -> int:
    selection = sys.argv[1] if len(sys.argv) == 2 else ""
    if selection not in ("baseline", "expanded"):
        return 64
    failures = 0
    for case in CASES[:6] if selection == "baseline" else CASES:
        identifier, _, amount, currency, memo, limit, kind, expected_amount, reason = case
        actual = decide(amount, currency, memo, limit)
        expected = {"Approved": lambda: Approved(expected_amount),
                    "NeedsReview": lambda: NeedsReview(expected_amount),
                    "Invalid": lambda: Invalid(reason)}[kind]()
        passed = actual == expected
        failures += not passed
        print("CASE\t" + identifier + "\t" + ("PASS" if passed else "FAIL"))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
