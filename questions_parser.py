def parse_block(block_lines):
    if len(block_lines) < 5:
        raise ValueError(f"❌ Incomplete question block (need at least 5 lines):\n" + "\n".join(block_lines))

    # Дополняем до нужного количества строк
    while len(block_lines) < 6:
        block_lines.insert(-1, "X) N/A")  # перед ANSWER добавляем фиктивный вариант

    return {
        "text": block_lines[0].strip(),
        "option_a": block_lines[1][2:].strip() if block_lines[1].startswith("A") else "N/A",
        "option_b": block_lines[2][2:].strip() if block_lines[2].startswith("B") else "N/A",
        "option_c": block_lines[3][2:].strip() if block_lines[3].startswith("C") else "N/A",
        "option_d": block_lines[4][2:].strip() if block_lines[4].startswith("D") else "N/A",
        "correct": block_lines[5].split(":")[1].strip().upper()
    }

def parse_questions_from_txt(file):
    raw = file.read()
    encodings_to_try = ["utf-8", "utf-8-sig", "cp1251", "utf-16"]
    for enc in encodings_to_try:
        try:
            content = raw.decode(enc, errors="replace").splitlines()
            break
        except Exception:
            continue
    else:
        raise ValueError("❌ Cannot decode file. Please use UTF-8, CP1251, or UTF-16 encoding.")

    questions = []
    block = []

    for idx, line in enumerate(content):
        stripped = line.strip()
        if not stripped:
            continue  # просто пропускаем пустые строки

        block.append(stripped)

        if stripped.upper().startswith("ANSWER:"):
            try:
                questions.append(parse_block(block))
            except ValueError as e:
                raise ValueError(f"\n🚫 Error in block ending around line {idx + 1}:\n{e}")
            block = []

    if block:
        raise ValueError("🚫 Unexpected leftover lines at end of file (missing ANSWER:?):\n" + "\n".join(block))

    return questions
