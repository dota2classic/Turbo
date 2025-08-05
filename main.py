import re

# Путь к файлам
UNITS_FILE = "npc_units.txt"
TARGETS_FILE = "units.txt"
OUTPUT_FILE = "npc_units_modified.txt"

MULTIPLIER = 2

# Загружаем список нужных юнитов
with open(TARGETS_FILE, "r", encoding="utf-8") as f:
    target_units = set(line.strip() for line in f if line.strip())

# Загружаем весь файл как строки
with open(UNITS_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Текущий контекст юнита
current_unit = None
inside_block = False

# Буфер для нового содержимого
modified_lines = []

# Регулярка для параметров
param_pattern = re.compile(r'("Bounty(?:XP|GoldMin|GoldMax)"\s*")(\d+)(")')

for line in lines:
    stripped = line.strip()

    # Начало юнита
    if stripped.startswith('"') and stripped.endswith('{') is False and not inside_block:
        match = re.match(r'"([^"]+)"', stripped)
        if match:
            current_unit = match.group(1)

    # Вход в блок
    if "{" in line:
        inside_block = True

    # Выход из блока
    if "}" in line:
        inside_block = False
        current_unit = None

    # Если в нужном юните — ищем параметры для замены
    if inside_block and current_unit in target_units:
        def repl(m):
            key, val, end = m.group(1), int(m.group(2)), m.group(3)
            return f'{key}{val * MULTIPLIER}{end}'

        modified_line = param_pattern.sub(repl, line)
        modified_lines.append(modified_line)
    else:
        modified_lines.append(line)

# Сохраняем результат
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(modified_lines)
