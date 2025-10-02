import csv
from datetime import datetime
from pathlib import Path
from typing import Optional

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
FEEDBACK_CSV = DATA_DIR / "feedback.csv"

def record_feedback(
    text: str,
    user_label: str = "unknown",
    predicted_label: Optional[str] = None,
    probability: Optional[float] = None,
    user_id: Optional[str] = None,
    notes: Optional[str] = None,
) -> None:
    is_new = not FEEDBACK_CSV.exists()
    with FEEDBACK_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp","user_id","text","user_label","predicted_label","probability","notes"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            user_id or "",
            text,
            user_label,
            predicted_label or "",
            "" if probability is None else f"{probability:.6f}",
            notes or "",
        ])