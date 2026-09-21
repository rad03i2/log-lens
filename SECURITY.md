# Security Policy / سياسة الأمان

Log Lens is local-first: it reads the file you explicitly provide and does not send log content over the network. It has no telemetry, credentials, or remote service configuration.

## Safe use

- Treat logs as potentially sensitive; they may contain tokens, identifiers, paths, or personal data.
- Avoid committing real logs to Git. `.gitignore` excludes `*.log` by default.
- `follow` is read-only; Log Lens never truncates or rewrites the source file.
- Regex input uses Python's backtracking `re` engine. Complex hostile patterns can consume excessive CPU. The CLI limits regex length, but that is not a time limit.
- The normal file reader rejects files over 100 MiB by default. `follow` intentionally streams instead.

For a suspected vulnerability, open a GitHub security report when available rather than publishing sensitive exploit details in an issue.

---

يعمل Log Lens محليًا ولا يرسل محتوى السجلات إلى الشبكة. قد تحتوي السجلات نفسها على معلومات حساسة، لذلك لا ترفع سجلات إنتاج حقيقية إلى Git. وضع المتابعة للقراءة فقط ولا يعدّل الملف. محرك التعبيرات النمطية في Python قد يتأثر بأنماط مكلفة حسابيًا، وحد طول النمط ليس مهلة تنفيذ كاملة.

**Author / المؤلف:** Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2
