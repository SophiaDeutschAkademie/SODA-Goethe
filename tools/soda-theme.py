#!/usr/bin/env python3
"""SODA Modelltest: 다크 모드 스위치와 목차 버튼을 HTML 파일에 넣습니다.

Lehrwerk의 다른 앱과 같은 부품입니다.
  - 오른쪽 위 다크 모드 스위치 (기본 다크, 선택은 localStorage 'soda-theme' 하나를 모든 앱이 함께 씁니다)
  - 목차 페이지(index.html)에는 스위치 왼쪽에 'Lehrwerk 목차로 돌아가기' 버튼
  - 접속 횟수 집계 태그(GoatCounter, 쿠키 없음)를 head에 넣음

사용법 (저장소 어디서 실행해도 됩니다)
  python3 tools/soda-theme.py zertifikat/goethe-b2/index.html  --kind index
  python3 tools/soda-theme.py zertifikat/goethe-b2/digital.html --kind exam

몇 번을 실행해도 결과가 같습니다(이미 들어 있는 블록은 지우고 다시 넣습니다).
build-digital.py와 build-index.py는 파일을 쓴 뒤 이 도구를 자동으로 부릅니다.
"""
import argparse
import re
import sys

D ='html[data-theme="dark"]'

THEME_JS = r"""<script id="soda-theme-js">
(function(){
  var KEY='soda-theme', d=document.documentElement, t='dark';
  try{var s=localStorage.getItem(KEY); if(s==='light'||s==='dark') t=s;}catch(e){}
  function apply(v){
    d.setAttribute('data-theme',v); d.style.colorScheme=v;
    var m=document.querySelector('meta[name="color-scheme"]'); if(m) m.setAttribute('content',v);
    var c=document.querySelector('meta[name="theme-color"]'); if(c) c.setAttribute('content',v==='dark'?'#14181E':'#FAFAF8');
  }
  apply(t);
  var SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>';
  function mount(){
    if(document.getElementById('soda-theme-btn')) return;
    var b=document.createElement('button'); b.type='button'; b.id='soda-theme-btn'; b.className='soda-theme-btn';
    function paint(){ var dk=d.getAttribute('data-theme')==='dark'; b.innerHTML=dk?SUN:MOON; b.setAttribute('aria-pressed',dk?'true':'false'); b.setAttribute('aria-label','다크 모드 '+(dk?'끄기':'켜기')); b.title='다크 모드 '+(dk?'켜짐':'꺼짐')+' · 누르면 '+(dk?'라이트':'다크')+'로 바뀌어요'; }
    b.addEventListener('click',function(){ var n=d.getAttribute('data-theme')==='dark'?'light':'dark'; apply(n); try{localStorage.setItem(KEY,n);}catch(e){} paint(); });
    paint(); document.body.appendChild(b);
    __TOC__
  }
  if(document.body) mount(); else document.addEventListener('DOMContentLoaded',mount);
})();
</script>"""

TOC_JS = (
    "if(!document.getElementById('soda-toc-btn')){ var a=document.createElement('a'); a.id='soda-toc-btn'; "
    "a.className='soda-toc-btn'; a.href='__HREF__'; a.setAttribute('aria-label','목차로 돌아가기'); "
    "a.innerHTML='<svg viewBox=\"0 0 20 20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" "
    "stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M12 4l-6 6 6 6\"/></svg>목차'; document.body.appendChild(a); }"
)

# 스위치와 목차 버튼 (Lehrwerk 공통 블록과 같은 모양)
BUTTON_CSS = """
.soda-theme-btn{position:fixed;top:max(10px,env(safe-area-inset-top));right:max(10px,env(safe-area-inset-right));z-index:2147482000;width:38px;height:38px;padding:0;border-radius:50%;border:1px solid rgba(110,118,130,.35);background:rgba(250,250,248,.92);color:#384568;display:grid;place-items:center;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.12);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);-webkit-tap-highlight-color:transparent}
.soda-theme-btn svg{width:20px;height:20px}
html[data-theme="dark"] .soda-theme-btn{background:rgba(27,32,40,.94);color:#E3E6F0;border-color:#3A4350;box-shadow:0 2px 12px rgba(0,0,0,.5)}
.soda-theme-btn:focus-visible{outline:3px solid #9DA6C6;outline-offset:2px}
.soda-toc-btn{position:fixed;top:max(10px,env(safe-area-inset-top));right:calc(max(10px,env(safe-area-inset-right)) + 46px);z-index:2147482000;height:38px;padding:0 14px 0 10px;border-radius:999px;border:1px solid rgba(110,118,130,.35);background:rgba(250,250,248,.92);color:#384568;display:inline-flex;align-items:center;gap:4px;font:600 13px/1 "Pretendard SODA","Pretendard Variable","Pretendard","Noto Sans KR",system-ui,sans-serif;text-decoration:none;white-space:nowrap;box-shadow:0 2px 10px rgba(0,0,0,.12);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);-webkit-tap-highlight-color:transparent}
.soda-toc-btn svg{width:16px;height:16px;flex:none}
html[data-theme="dark"] .soda-toc-btn{background:rgba(27,32,40,.94);color:#E3E6F0;border-color:#3A4350;box-shadow:0 2px 12px rgba(0,0,0,.5)}
.soda-toc-btn:focus-visible{outline:3px solid #9DA6C6;outline-offset:2px}
@media print{.soda-theme-btn,.soda-toc-btn{display:none!important}}
"""

# ───────── 목차 페이지(index.html): 모든 화면이 같은 색 변수를 씁니다 ─────────
INDEX_CSS = """
html[data-theme="dark"]{--navy:#AEB9DD;--navy-2:#C8D0EA;--ivory:#14181E;--mist:#222831;--line:#2A313B;--ochre:#C9964F;--ochre-ink:#DDAA68;--red:#E08C80;--ink:#ECEAE4;--ink-2:#C9CCD3;--ink-3:#A9B0BA}
html[data-theme="dark"] .mode{background:#1B2028}
html[data-theme="dark"] .mode:hover{box-shadow:0 10px 28px rgba(0,0,0,.45)}
html[data-theme="dark"] .start,html[data-theme="dark"] .btn:not(.ghost),html[data-theme="dark"] .it .go{color:#14181E}
html[data-theme="dark"] .it .p:hover,html[data-theme="dark"] .btn.ghost:hover{border-color:var(--ink-3)}
@media (max-width:700px){.page>.brand{padding-right:132px}.page>.brand b{font-size:16px}}
"""

# ───────── 디지털 시험 화면(digital.html) ─────────
EXAM_ACC = {
    # --acc는 버튼·표시의 배경(흰 글자), --acc-2는 글자색으로 쓰이므로 밝게, hover는 따로
    "green": dict(acc="#277F6A", acc2="#6FCDB0", accw="#1E2E2B", accline="#2F5A4E", hover="#33977F"),
    "blue": dict(acc="#2F6DB5", acc2="#8DB7EE", accw="#1C2738", accline="#35557F", hover="#3A7BC8"),
}

EXAM_CSS = """
.top{padding-right:60px}
.pgm{padding-top:60px}
@media (max-width:560px){.top{padding-right:54px}}
html[data-theme="dark"]{color-scheme:dark;--bg:#14181E;--panel:#1B2028;--bar:#171C23;--line:#363F4B;--line-2:#2A313B;--ink:#ECEAE4;--ink-2:#C9CCD3;--muted:#9BA4AF;--acc:__ACC__;--acc-2:__ACC2__;--acc-w:__ACCW__;--acc-line:__ACCLINE__;--warn:#EE8D84;--warn-w:#3A2321;--mark:#6B5A12;--soft:#222831;--soft-2:#2A313B}
/* 흰 바탕 */
S .top,S .hlp,S .fz,S .vol,S .timer,S .tab .pr,S .tab[aria-selected="true"],S .tbtn,S .abar,S .ph .sub button,S .card,S .q .qn,S .opt,S .opt .rb,S .selw select,S .grid th,S .cell .rb,S .sz button,S textarea.ed,S .foot,S .chip,S .btn,S .modal,S .tip,S .sheet,S .post2,S .gp{background:var(--panel)}
S .ph{background:var(--bar)}
S .ctx,S .q.ex,S .grid tr.ex td,S .facts span,S .score .bx,S .tparts span,S table.rv .tp td,S .wtask pre,S .post2 .ph2,S .post .pt,S .bank,S .hlist,S .wbox{background:var(--soft)}
S .exs,S .gapx{background:var(--soft-2)}
S .gapx:hover{background:#34425A}
S .cell:hover{background:var(--acc-w)}
/* 상태 표시(위의 흰 바탕 규칙보다 우선) */
S .tab.done .pr{background:var(--acc-w);border-color:var(--acc-line);color:var(--acc-2)}
S .ph .sub button[aria-current="true"],S .q.ans .qn,S .chip.ans,S .btn.pri,S .gp.on{background:var(--acc);border-color:var(--acc);color:#fff}
S .btn:hover{background:var(--soft-2)}
S .btn.pri:hover{background:__HOVER__}
S .opt.on{background:var(--acc-w);border-color:var(--acc-line)}
S .opt:hover{background:var(--acc-w);border-color:var(--line)}
S .opt.dis:hover{background:var(--panel)}
S .q.ex .opt{background:transparent}
S .q.ex .opt.on{background:var(--soft-2);border-color:#4A5668}
S .gapx.filled{background:var(--acc-w);border-bottom-color:var(--acc)}
S .timer.low{background:var(--warn-w);border-color:var(--warn)}
S .score .bx.ok{background:var(--acc-w);border-color:var(--acc-line)}
S .score .bx.no{background:var(--warn-w);border-color:#6B3A35}
S .tbtn[aria-pressed="true"]{background:#4A4012;border-color:#8A7A25;color:#F2E3A0}
S .stm.used .sl2{background:var(--acc)}
S .mdl,S pre.mdl{background:var(--acc-w)}
/* 글자색: 배경으로 쓰는 --acc는 어두워서, 글자로 쓰는 곳은 밝은 색으로 */
S .grid tr.ans td.no,S .sheet .ey,S .tip .stp,S table.rv tr.ok td.m,S .bank .bi.used .bl{color:var(--acc-2)}
/* 진한 ink 배경 + 흰 글자였던 곳 */
S .post2 .pl,S .stm .sl2,S .txs .tn b,S .al{background:#4A5668}
S .ad.used .al,S .pic.used .al{background:var(--acc)}
S .board .bh{border-bottom:1px solid var(--line)}
S .toast{background:#2F3A4A;color:#fff;border:1px solid #4A5668}
S .toast.w{background:#B63C33;border-color:#B63C33}
@keyframes sodaflash{0%,40%{background:#4A4012}100%{background:transparent}}
S .q.flash{animation:sodaflash 1.2s ease}
S .modal,S .tip{box-shadow:0 18px 50px rgba(0,0,0,.6)}
S .hole{outline-color:#ECEAE4}
"""


def expand(css, acc):
    """'S '를 다크 모드 접두사로 바꾸고 색 자리표시자를 채웁니다."""
    css = css.replace("S .", D + " .").replace("S textarea", D + " textarea").replace("S table", D + " table").replace("S pre", D + " pre")
    for k, v in (("__ACC__", acc["acc"]), ("__ACC2__", acc["acc2"]), ("__ACCW__", acc["accw"]),
                 ("__ACCLINE__", acc["accline"]), ("__HOVER__", acc["hover"])):
        css = css.replace(k, v)
    return css


# Lehrwerk 목차 주소: 앱이 별도 저장소에 있어서 전체 주소를 씁니다
LEHRWERK_TOC = "https://sophiadeutschakademie.github.io/SODA-Lehrwerk/#inhalt"


def build_blocks(kind, toc_href):
    toc = TOC_JS.replace("__HREF__", toc_href) if kind == "index" else ""
    js = THEME_JS.replace("__TOC__", toc)
    return js


# 접속 횟수 집계(GoatCounter 공식 태그, 쿠키 없음). Lehrwerk의 모든 페이지와 같은 사이트 코드를 씁니다
ANALYTICS_TAG = ('<script id="soda-analytics" data-goatcounter="https://sodadeutsch.goatcounter.com/count" '
                 'async src="https://gc.zgo.at/count.js"></script>\n')


def patch(html, kind, toc_href=LEHRWERK_TOC):
    # 이전 블록 제거
    html = re.sub(r'<script id="soda-theme-js">.*?</script>\s*', "", html, flags=re.S)
    html = re.sub(r'<style id="soda-dark">.*?</style>\s*', "", html, flags=re.S)
    html = re.sub(r'<script id="soda-analytics"[^>]*></script>\s*', "", html)

    js = build_blocks(kind, toc_href)
    if kind == "index":
        css = BUTTON_CSS + expand(INDEX_CSS, EXAM_ACC["green"])
    else:
        m = re.search(r"--acc:\s*(#[0-9a-fA-F]{6})", html)
        acc = EXAM_ACC["blue"] if (m and m.group(1).lower() == "#1f5a9e") else EXAM_ACC["green"]
        css = BUTTON_CSS + expand(EXAM_CSS, acc)
    style = '<style id="soda-dark">' + css + "</style>\n"

    # 스크립트는 <meta charset> 바로 뒤에, 스타일은 </head> 앞에
    m = re.search(r"<meta\s+charset=[^>]*>", html, flags=re.I)
    if not m:
        sys.exit("<meta charset>을 찾지 못했습니다")
    html = html[: m.end()] + "\n" + js + "\n" + html[m.end():]
    i = html.lower().rfind("</head>")
    if i < 0:
        sys.exit("</head>를 찾지 못했습니다")
    html = html[:i] + ANALYTICS_TAG + style + html[i:]
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--kind", choices=["index", "exam"], required=True)
    ap.add_argument("--toc", default=LEHRWERK_TOC, help="Lehrwerk 목차로 가는 주소(index 전용)")
    a = ap.parse_args()
    src = open(a.file, encoding="utf-8").read()
    out = patch(src, a.kind, a.toc)
    open(a.file, "w", encoding="utf-8").write(out)
    print(f"다크 모드 적용: {a.file} ({a.kind})")


if __name__ == "__main__":
    main()
