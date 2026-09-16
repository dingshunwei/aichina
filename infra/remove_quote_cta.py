#!/usr/bin/env python3
"""从 aichina 全站移除「获取报价 / Request a quote / Get a quote」入口。

覆盖：index.html（+ 24 个语言目录的 index.html）、liquid-cooling.html
内容：卡片上的报价按钮、pgrid 的 data-quote 属性、点击处理器、openInquiry()、
      以及 film 区块的「Get a quote · 获取报价」CTA 与其样式。
保留：Leave a message（留言表单）、询价弹窗本身（其它地方可能仍需要）。
"""
import glob, os, re, sys

ROOT = "/Users/stan/lobsterai/project/aichina"
files = ["index.html", "liquid-cooling.html"] + sorted(
    os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "*", "index.html")))

changed = []
for rel in files:
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    orig = s

    # 1) 卡片里的报价按钮
    s = re.sub(r"\n\s*\+'<button class=\"q\" data-i=\"'\+i\+'\">'\+grid\.getAttribute\('data-quote'\)\+'</button>'", "", s)
    s = re.sub(r"\n\s*\+'<button class=\"q\" data-i=\"'\+i\+'\">Request a quote →</button></div></article>';",
               "\n      +'</div></article>';", s)
    # 2) pgrid 的 data-quote 属性
    s = re.sub(r'\s*data-quote="[^"]*"', "", s)
    # 3) 点击处理器（整段）
    s = re.sub(r"\n\s*grid\.addEventListener\('click',function\(e\)\{\n\s*var b=e\.target\.closest\('\.q'\); if\(!b\) return;\n[^\n]*\n\s*\}\);", "", s)
    # 4) openInquiry 函数
    s = re.sub(r"\n  function openInquiry\(p\)\{\n(?:[^\n]*\n)*?  \}", "", s)
    # 5) .q 相关 CSS
    s = re.sub(r"\.pcard \.q\{[^}]*\}", "", s)
    s = re.sub(r"\.pcard \.q:hover\{[^}]*\}", "", s)
    # 6) film 区块的 Get a quote 按钮与样式（liquid-cooling）
    s = re.sub(r"\n    <div class=\"filmcta\">\n(?:.*\n)*?    </div>", "", s)
    s = re.sub(r"\.filmcta[^{]*\{[^}]*\}", "", s)

    if s != orig:
        open(p, "w", encoding="utf-8").write(s)
        changed.append(rel)

print(f"改动文件 {len(changed)} 个")
for c in changed[:6]:
    print("  ", c)
print("   ..." if len(changed) > 6 else "")
