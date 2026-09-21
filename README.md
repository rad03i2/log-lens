# Log Lens

A small, local-first command-line tool for searching, filtering, summarizing, tailing, and following plain-text application logs without uploading them anywhere.

**Author:** Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — GitHub: [@rad03i2](https://github.com/rad03i2)

## English

### Why it exists

Large text logs are easy to generate and awkward to inspect repeatedly with ad-hoc commands. Log Lens provides a predictable cross-platform interface for common inspection tasks while remaining read-only and dependency-light.

### Features

- Detects common severity labels: TRACE, DEBUG, INFO, WARN/WARNING, ERROR, CRITICAL/FATAL.
- Searches by severity, literal text, Python regular expression, or combinations of them.
- Optional case-insensitive and inverted matching.
- Summarizes severity counts and the first/last detected ISO-like timestamp.
- Tails the final N lines and follows newly appended lines.
- JSON search/summary output for scripts and CI.
- Returns exit code `1` when a search has no matches and `2` for invalid input/read errors.
- Reusable Python API.
- Local-only processing; no telemetry or network calls.
- Standard-library runtime: no third-party runtime dependency.

### Requirements

Python 3.10 or newer.

### Installation

```bash
git clone https://github.com/rad03i2/log-lens.git
cd log-lens
python -m pip install -e .
```

For an isolated environment:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
```

### Usage

```bash
log-lens search examples/sample.log.txt --level ERROR
log-lens search examples/sample.log.txt --contains timeout -i
log-lens search examples/sample.log.txt --regex "timeout|latency" --json
log-lens summary examples/sample.log.txt
log-lens summary examples/sample.log.txt --json
log-lens tail examples/sample.log.txt -n 3
log-lens follow path/to/application.log
```

`search` prints at most 200 matches by default. Use `--limit`, up to 10,000. Text reading defaults to UTF-8 with replacement for malformed bytes; choose another Python codec with `--encoding`.

### Python API

```python
from log_lens import filter_records, read_records, summarize
from pathlib import Path

records = read_records(Path("examples/sample.log.txt"))
errors = list(filter_records(records, level="ERROR"))
print(errors[0].text)
```

### Configuration

No environment variables, account, API key, or config file is required. All behavior is selected explicitly through CLI options. Therefore this project intentionally has no `.env.example`.

### Preview guidance

For a portfolio screenshot, open a terminal and place `log-lens summary examples/sample.log.txt` beside `log-lens search examples/sample.log.txt --level ERROR`. No GUI is implemented, so screenshots should represent the actual terminal interface.

### Project structure

```text
src/log_lens/core.py   parsing, filtering, summaries, safe file reading
src/log_lens/cli.py    command-line interface
src/log_lens/__init__.py public API
tests/                 unit and CLI integration tests
examples/              synthetic sample input
.github/workflows/     cross-platform CI
```

### Testing

```bash
python -m pip install -e .
python -m compileall -q src tests
python -m unittest discover -s tests -v
log-lens --version
```

CI runs these checks on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

### Security & privacy

Log Lens is read-only and local-first. It does not transmit logs. Real logs can contain credentials or personal information, so do not commit them; `*.log` is ignored by default. Normal file reads have a 100 MiB safety limit. Python regular expressions can still exhibit catastrophic backtracking with hostile patterns; pattern length is limited but there is no regex execution timeout. See [SECURITY.md](SECURITY.md).

### Limitations

- Designed for line-oriented text logs, not binary journals, compressed archives, ETW, Windows Event Log, or systemd journal databases.
- Severity and timestamp recognition is intentionally heuristic, not a schema-specific parser.
- Multiline stack traces are treated as individual lines.
- `follow` tracks appends to one open file and does not automatically reopen after log rotation.
- Python `re` syntax is used; PCRE-only constructs are unsupported.

### Optional roadmap

Future work may add opt-in JSON-lines parsing, multiline grouping, rotation-aware following, and configurable parsing profiles. These are not claimed as current features.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused, tested, local-first, and documented in both languages.

### License

MIT — see [LICENSE](LICENSE).

### Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**

---

## العربية

### نظرة عامة

**Log Lens** أداة سطر أوامر محلية لفحص ملفات السجلات النصية والبحث فيها وتصفيتها وتلخيصها وعرض آخر الأسطر ومتابعة الأسطر الجديدة، من دون رفع محتوى السجل إلى أي خدمة خارجية.

### لماذا يوجد المشروع؟

تتضخم سجلات التطبيقات بسرعة، وتكرار أوامر مختلفة لفحصها يصبح مزعجًا وغير موحد بين الأنظمة. يوفر المشروع واجهة واضحة ومتعددة المنصات للمهام الشائعة مع إبقاء التعامل مع الملف للقراءة فقط.

### الميزات

- اكتشاف TRACE وDEBUG وINFO وWARN/WARNING وERROR وCRITICAL/FATAL مع توحيد الأسماء البديلة.
- تصفية حسب المستوى أو نص حرفي أو تعبير نمطي، ويمكن دمج الشروط.
- بحث غير حساس لحالة الأحرف وعكس نتيجة المطابقة.
- ملخص لعدد الأسطر وتوزيع مستويات السجل وأول/آخر طابع زمني معروف.
- عرض آخر N سطر ومتابعة الأسطر التي تضاف إلى الملف.
- إخراج JSON للبحث والملخص لاستخدامه في الأتمتة وCI.
- رموز خروج مفيدة: `1` عند عدم وجود نتائج و`2` للمدخلات أو القراءة غير الصالحة.
- واجهة Python قابلة لإعادة الاستخدام.
- معالجة محلية دون Telemetry أو اتصالات شبكية.
- لا توجد تبعيات تشغيل خارج مكتبة Python القياسية.

### المتطلبات والتثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/log-lens.git
cd log-lens
python -m pip install -e .
```

### أمثلة الاستخدام

```bash
log-lens search examples/sample.log.txt --level ERROR
log-lens search examples/sample.log.txt --contains timeout -i
log-lens search examples/sample.log.txt --regex "timeout|latency" --json
log-lens summary examples/sample.log.txt
log-lens tail examples/sample.log.txt -n 3
log-lens follow path/to/application.log
```

### الإعداد

لا يحتاج المشروع إلى حساب أو مفتاح API أو متغيرات بيئة أو ملف إعداد. الخيارات تمرر مباشرة إلى CLI، ولذلك لا يوجد `.env.example` غير ضروري.

### بنية المشروع

الكود الأساسي موجود في `src/log_lens/core.py`، وواجهة الأوامر في `src/log_lens/cli.py`، والاختبارات في `tests/`، والمثال الآمن في `examples/`، وإعداد CI في `.github/workflows/ci.yml`.

### الاختبارات

```bash
python -m pip install -e .
python -m compileall -q src tests
python -m unittest discover -s tests -v
log-lens --version
```

تختبر GitHub Actions المشروع على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

### الخصوصية والأمان

الأداة محلية وللقراءة فقط ولا ترسل السجلات عبر الشبكة. قد تحتوي سجلات الإنتاج على أسرار أو بيانات شخصية، لذلك لا ينبغي رفعها إلى Git، ويستثني `.gitignore` ملفات `*.log`. القراءة العادية محددة افتراضيًا بـ100 MiB. تستخدم التعبيرات النمطية محرك Python `re` الذي لا يوفر مهلة تنفيذ داخلية؛ لذلك يجب تجنب الأنماط غير الموثوقة شديدة التعقيد. راجع [SECURITY.md](SECURITY.md).

### القيود

- مخصصة للسجلات النصية سطرًا بسطر وليست قارئًا لـWindows Event Log أو systemd journal أو الملفات الثنائية والمضغوطة.
- اكتشاف المستوى والطابع الزمني عام وليس محللًا خاصًا بكل صيغة سجل.
- stack traces متعددة الأسطر تعامل كأسطر منفصلة.
- `follow` لا يعيد فتح الملف تلقائيًا بعد log rotation.
- التعبيرات النمطية تتبع Python وليست PCRE.

### التطوير المستقبلي الاختياري

يمكن مستقبلًا إضافة JSON Lines وتجميع الأسطر المتعددة ومتابعة واعية بتدوير السجلات وملفات تعريف قابلة للضبط. هذه ليست ميزات حالية.

### المساهمة والترخيص

راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص برخصة MIT الموجودة في [LICENSE](LICENSE).

### المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **[@rad03i2](https://github.com/rad03i2)**
