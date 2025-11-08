import sys
import json
from androguard.misc import AnalyzeAPK

def main():
    if len(sys.argv) < 2:
        sys.stdout.write(json.dumps({"error": "No APK path provided"}))
        sys.stdout.flush()
        return

    apk_path = sys.argv[1]

    try:
        a, d, dx = AnalyzeAPK(apk_path)
        permissions = list(a.get_permissions() or [])
        # Output only JSON to stdout, use sys.stdout.write to avoid extra newlines
        sys.stdout.write(json.dumps({"permissions": permissions}))
        sys.stdout.flush()
    except Exception as e:
        # Output only JSON to stdout
        sys.stdout.write(json.dumps({"error": str(e)}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
