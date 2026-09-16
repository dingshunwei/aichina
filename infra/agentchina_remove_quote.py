#!/usr/bin/env python3
"""agentchina（总站）去报价：
1) 三个产品页（bearings/crystals/motors）整段移除 <section id="quote"> 及其提交 JS、CSS；
2) 页脚 Contact 链接改为「联系作者」；
3) 首页的询价提示/预填文案改为「联系作者」（保留 20 语言键，值统一为双语中性文案）；
4) 首页 meta 描述去掉 inquiry 措辞。
"""
import re

BASE = "/Users/stan/lobsterai/project/agentchina/"
LABEL = "联系作者 · Contact the author"

# ---------- 1) 三个产品页 ----------
for name in ["bearings.html", "crystals.html", "motors.html"]:
    p = BASE + name
    s = open(p, encoding="utf-8").read()
    o = s
    # 整段报价区块
    s = re.sub(r"\n<section id=\"quote\">\n(?:.*\n)*?</section>\n", "\n", s)
    # 提交 JS
    s = re.sub(r"\ndocument\.getElementById\('qSend'\)\.addEventListener\('click',async function\(\)\{\n(?:.*\n)*?\}\);\n", "\n", s)
    # CSS
    s = re.sub(r"\n\s*#quote\{[^}]*\}", "", s)
    # 页脚
    s = s.replace('Contact: <a href="/#">inquiry form</a>', LABEL + ': <a href="/#">联系作者 →</a>')
    open(p, "w", encoding="utf-8").write(s)
    print(f"{name}: {'已改' if s != o else '未变'}（quote 残留 {s.count('quote')} / qSend {s.count('qSend')}）")

# ---------- 2) 首页 ----------
p = BASE + "index.html"
s = open(p, encoding="utf-8").read()

# 2a) meta / JSON-LD 描述里的 inquiry 措辞
s = s.replace("send a buy-from-China or sell-to-China inquiry with one click. 中国兔兔 · 世界贸易 · 可爱动物环.",
              "contact the author for buy-from-China or sell-to-China sourcing. 中国兔兔 · 世界贸易 · 可爱动物环.")
s = s.replace("Click a ship or plane to send a buy-from-China or sell-to-China inquiry — 13 cute animals, 20 languages.",
              "Click a ship or plane to contact the author — buy from or sell to China. 13 cute animals, 20 languages.")
s = s.replace("13 cute animals, 20 languages — buy from or sell to China with one click inquiry.",
              "13 cute animals, 20 languages — buy from or sell to China. Contact the author directly.")
s = s.replace("Global trade partner hub: buy from China or sell to China via one-click inquiry. 13 countries, 20 languages.",
              "Global trade partner hub: buy from China or sell to China — contact the author directly. 13 countries, 20 languages.")

# 2b) 静态提示条
s = s.replace('<div class="hint" id="hint">👆 点飞机或轮船，向我询价</div>',
              '<div class="hint" id="hint">👆 点飞机或轮船，联系作者</div>')

# 2c) HINT / INQ 字典：保留键，值统一成中性文案
def rewrite_dict(src, var):
    m = re.search(r"const " + var + r"=\{.*?\};", src, re.S)
    if not m:
        print(f"  ⚠ 找不到 {var} 字典")
        return src
    block = m.group(0)
    keys = re.findall(r"([A-Za-z_]+):'", block)
    val = ("'👆 点飞机或轮船，联系作者 · Tap a plane or ship to contact the author'"
           if var == "HINT" else "'联系作者 · Contact the author — '")
    newblock = "const " + var + "={" + ",".join(f"{k}:{val}" for k in keys) + "};"
    return src.replace(block, newblock, 1)

s = rewrite_dict(s, "HINT")
s = rewrite_dict(s, "INQ")

open(p, "w", encoding="utf-8").write(s)
print("index.html: 已改；剩余 inquiry/询价/报价 =>",
      s.count("inquiry"), s.count("Inquiry"), s.count("询价"), s.count("报价"))
