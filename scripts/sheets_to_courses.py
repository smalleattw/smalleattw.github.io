import csv, json, sys, re
from pathlib import Path

def to_int(x, default=0):
    try:
        return int(str(x).strip())
    except:
        return default

def split_tags(s):
    s = (s or "").strip()
    if not s:
        return []
    return [t.strip() for t in re.split(r"[,\uFF0C]", s) if t.strip()]

def main():
    if len(sys.argv) < 3:
        print("Usage: python sheets_to_courses.py <input.csv> <output.json>")
        sys.exit(1)

    in_csv = Path(sys.argv[1])
    out_json = Path(sys.argv[2])

    courses = []
    with in_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get("status") or "published").strip().lower()
            if status not in ("published", "public", "live"):
                continue

            course = {
                "id": (row.get("id") or "").strip(),
                "title": (row.get("title") or "").strip(),
                "category": (row.get("category") or "").strip(),
                "level": (row.get("level") or "").strip(),
                "minutes": to_int(row.get("minutes")),
                "tags": split_tags(row.get("tags")),
                "summary": (row.get("summary") or "").strip(),
                "cover": (row.get("cover") or "").strip(),
                "flavour": {
                    "salty": to_int(row.get("salty")),
                    "sweet": to_int(row.get("sweet")),
                    "sour": to_int(row.get("sour")),
                    "spicy": to_int(row.get("spicy")),
                    "umami": to_int(row.get("umami")),
                    "numbing": to_int(row.get("numbing")),
                },
                "texture": {
                    "crispy": to_int(row.get("texture_crispy")),
                    "q": to_int(row.get("texture_q")),
                },
                "belonging": split_tags(row.get("belonging")),
            }

            # 基本防呆：沒 id 或 title 的跳過
            if not course["id"] or not course["title"]:
                continue

            courses.append(course)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(courses, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(courses)} courses -> {out_json}")

if __name__ == "__main__":
    main()
