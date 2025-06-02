from questions_parser import parse_questions_from_txt

def main():
    try:
        with open("quiz.txt", "rb") as f:
            questions = parse_questions_from_txt(f)
    except Exception as e:
        print("❌ Parsing failed:", e)
        return

    print(f"\n✅ Parsed {len(questions)} questions.\n")
    output_lines = []

    for i, q in enumerate(questions, start=1):
        print(f"{i}. {q['text']}")
        print(f"   A. {q['option_a']}")
        print(f"   B. {q['option_b']}")
        print(f"   C. {q['option_c']}")
        print(f"   D. {q['option_d']}")
        print(f"   ✔ Correct: {q['correct']}\n")

        output_lines.append(f"{i}. {q['text']}")
        output_lines.append(f"A. {q['option_a']}")
        output_lines.append(f"B. {q['option_b']}")
        output_lines.append(f"C. {q['option_c']}")
        output_lines.append(f"D. {q['option_d']}")
        output_lines.append(f"ANSWER: {q['correct']}")
        output_lines.append("")  # Empty line between questions

    with open("parsed_output.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(output_lines))

    print("✅ Output written to parsed_output.txt")

if __name__ == "__main__":
    main()
