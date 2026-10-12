import sys, re, html, subprocess
url = sys.argv[1]
maxc = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
off = int(sys.argv[3]) if len(sys.argv) > 3 else 0
r = subprocess.run(["curl","-sSL","--max-time","40","-A","Mozilla/5.0 (X11; Linux x86_64)","-w","\nHTTP_STATUS:%{http_code}\n",url],capture_output=True)
raw = r.stdout.decode("utf-8","replace")
m = re.search(r"HTTP_STATUS:(\d+)", raw)
status = m.group(1) if m else "?"
raw = raw.replace(m.group(0), "") if m else raw
raw = re.sub(r"(?is)<(script|style|noscript|svg|header|footer|nav).*?</\1>", " ", raw)
raw = re.sub(r"(?s)<[^>]+>", " ", raw)
t = html.unescape(raw)
t = re.sub(r"[ \t\r\f\v]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n", t)
print("STATUS", status, "ERR", r.stderr.decode()[:200])
print(t[off:off+maxc])
