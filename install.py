#!/usr/bin/env python3
"""
html-slide-builder-lite Skill 安裝腳本（研習簡易版）
用法：python install.py

簡易版只做兩件事：
  1. 檢查 Python / git（gh 為選配，只有要部署 GitHub Pages 才需要）
  2. 把 skill/ 複製到你的 Agent 技能資料夾

不需要：OpenAI API Key、draw 技能、Pillow、Firebase。
"""
import sys
import shutil
from pathlib import Path

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"; C = "\033[96m"; B = "\033[1m"; X = "\033[0m"
def ok(m):   print(f"  {G}✔{X}  {m}")
def warn(m): print(f"  {Y}⚠{X}  {m}")
def err(m):  print(f"  {R}✘{X}  {m}")
def info(m): print(f"  {C}→{X}  {m}")
def head(m): print(f"\n{B}{m}{X}")


def find_skills_dir() -> Path:
    """偵測常見 Agent 的技能資料夾；找不到就用 Claude 預設位置並建立。"""
    home = Path.home()
    candidates = [
        home / ".claude" / "skills",                 # Claude Code
        home / ".claude-skills",                      # Claude Code（舊）
        home / ".config" / "opencode" / "skills",     # OpenCode
        home / ".agents" / "skills",                  # Codex
    ]
    for p in candidates:
        if p.exists():
            return p
    default = home / ".claude" / "skills"
    default.mkdir(parents=True, exist_ok=True)
    return default


def check_requirements() -> dict:
    head("【1】 檢查元件（簡易版）")
    r = {}

    vi = sys.version_info
    if vi >= (3, 8):
        ok(f"Python {vi.major}.{vi.minor}.{vi.micro}")
        r["python"] = True
    else:
        err(f"Python 版本過舊（{vi.major}.{vi.minor}），需要 3.8+")
        r["python"] = False

    git = shutil.which("git")
    if git:
        ok(f"git：{git}")
        r["git"] = True
    else:
        err("git 未安裝（版本控制必要）")
        r["git"] = False

    gh = shutil.which("gh")
    if gh:
        ok(f"GitHub CLI (gh)：{gh}（選配：部署 GitHub Pages 才需要）")
        r["gh"] = True
    else:
        warn("GitHub CLI (gh) 未安裝 —— 沒關係，簡易版預設用瀏覽器直接開簡報，不需要部署")
        r["gh"] = False

    return r


def install_skill(skills_dir: Path) -> bool:
    head("【2】 安裝 Skill")
    src = Path(__file__).parent / "skill"
    dst = skills_dir / "html-slide-builder-lite"
    if dst.exists():
        overwrite = input(f"\n  目標已存在：{dst}\n  覆蓋安裝？[y/N]：").strip().lower()
        if overwrite != "y":
            warn("取消安裝")
            return False
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    ok(f"Skill 已安裝至：{dst}")
    return True


def main():
    print(f"""
{B}{C}╔══════════════════════════════════════════════╗
║  html-slide-builder-lite 安裝程式（研習版）  ║
║  教材 → 零金鑰 HTML 互動簡報                 ║
╚══════════════════════════════════════════════╝{X}
""")
    r = check_requirements()
    if not r.get("python"):
        err("Python 版本不符，無法安裝。"); sys.exit(1)
    if not r.get("git"):
        err("git 未安裝，請先安裝 git。"); sys.exit(1)

    skills_dir = find_skills_dir()
    info(f"技能資料夾：{skills_dir}")
    success = install_skill(skills_dir)

    head("【3】 安裝完成")
    if success:
        print(f"""
  {G}{B}✔ html-slide-builder-lite 已安裝！{X}

  {B}使用方式：{X}對你的 Agent 說：
    「幫我把這份教材做成 HTML 互動簡報」

  {B}本版特性：{X}
    {G}✔{X}  零 API Key（不需 OpenAI / Firebase）
    {G}✔{X}  零額外技能（不需 draw / Pillow）
    {G}✔{X}  產出單一 index.html，雙擊用瀏覽器即可播放
    {'%s✔%s' % (G,X) if r.get('gh') else '%s⚠ 選配%s' % (Y,X)}  GitHub Pages 部署（需 gh + GitHub 帳號）
""")
    else:
        warn("安裝未完成。")


if __name__ == "__main__":
    main()
