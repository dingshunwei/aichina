#!/usr/bin/env python3
"""全站去报价 + 留言入口统一改成「联系作者 · Contact the author」。

用法：python3 remove_quote_and_relabel.py semi aichina
"""
import glob, os, re, sys

LABEL = "联系作者 · Contact the author"
ROOTS = sys.argv[1:] or ["semi", "aichina"]
BASE = "/Users/stan/lobsterai/project"

for root_name in ROOTS:
    ROOT = os.path.join(BASE, root_name)
    files = sorted(glob.glob(os.path.join(ROOT, "*.html"))) + \
        sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    n_quote = n_label = 0
    for p in files:
        s = open(p, encoding="utf-8").read()
        orig = s

        # ---- A) 去掉产品卡上的报价按钮 / data-quote / 点击处理 / openInquiry / .q 样式 ----
        s = re.sub(r"\n\s*\+'<button class=\"q\" data-i=\"'\+i\+'\">'\+grid\.getAttribute\('data-quote'\)\+'</button>'", "", s)
        s = re.sub(r"\n\s*\+'<button class=\"q\" data-i=\"'\+i\+'\">Request a quote →</button></div></article>';",
                   "\n      +'</div></article>';", s)
        s = re.sub(r'\s*data-quote="[^"]*"', "", s)
        s = re.sub(r"\n\s*grid\.addEventListener\('click',function\(e\)\{\n\s*var b=e\.target\.closest\('\.q'\); if\(!b\) return;\n[^\n]*\n\s*\}\);", "", s)
        s = re.sub(r"\n  function openInquiry\(p\)\{\n(?:[^\n]*\n)*?  \}", "", s)
        s = re.sub(r"\.pcard \.q\{[^}]*\}", "", s)
        s = re.sub(r"\.pcard \.q:hover\{[^}]*\}", "", s)

        # ---- B) 留言入口 → 联系作者（导航按钮 + 弹窗标题 + 「留言 →」链接）----
        new_s, k1 = re.subn(r'(<button class="hlp" onclick="openMsg\(\)">)[^<]*(</button>)',
                            lambda m: m.group(1) + LABEL + m.group(2), s)
        s = new_s
        i = s.find('<div class="msgbox">')
        if i >= 0:
            m = re.search(r"<h3>[^<]*</h3>", s[i:])
            if m:
                s = s[:i + m.start()] + "<h3>" + LABEL + "</h3>" + s[i + m.end():]
                k1 += 1
        new_s, k2 = re.subn(r">\s*留言\s*→\s*</a>", ">" + LABEL + " →</a>", s)
        s = new_s
        k1 += k2

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n_quote += 1 if "data-quote" not in s and 'class="q"' not in s and "openInquiry" not in s else 0
            n_label += k1

    print(f"{root_name}: 处理 {len(files)} 个文件；报价按钮清理生效于 {n_quote} 个文件；留言改名 {n_label} 处")
