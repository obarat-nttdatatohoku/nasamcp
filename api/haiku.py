"""Vercel サーバーレス関数: explanation テキストから俳句を生成"""

import json
import sys
import os
import re
import unicodedata
import random
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# haiku 生成ロジック (Skills/haiku_skill/skill.py と同等)

SMALL_KANA = set(list('ぁぃぅぇぉゃゅょゎァィゥェォャュョヮ'))
FUNNY_ENDING = ['でござる', 'だゼ', 'ニャ', 'だよ', 'かな', 'だよね']
VOWELS = re.compile(r'[aeiouyAEIOUY]+')


def is_japanese(text: str) -> bool:
    return bool(re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', text))


def split_to_moras(text: str):
    if not text:
        return []
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'[\u3000\s]+', ' ', text)
    text = re.sub(r'[！？!\?。、,\.\(\)\[\]「」『』"\'：:；;／\\\-＿\=\+\*<>\t\n\r]', '', text)
    moras = []
    for ch in text:
        if ch == ' ':
            continue
        if ch in SMALL_KANA and moras:
            moras[-1] = moras[-1] + ch
        else:
            moras.append(ch)
    return [m for m in moras if m]


def compose_haiku_from_moras(moras):
    targets = [5, 7, 5]
    lines = []
    idx = 0
    for need in targets:
        acc = []
        count = 0
        while idx < len(moras) and count < need:
            acc.append(moras[idx])
            idx += 1
            count += 1
        if count == need:
            lines.append(''.join(acc))
        else:
            return None
    return '\n'.join(lines)


def generate_haiku_jp(input_text: str) -> str:
    moras = split_to_moras(input_text)
    if len(moras) >= 17:
        haiku = compose_haiku_from_moras(moras)
        if haiku:
            if random.random() < 0.25:
                haiku = haiku + ' ' + random.choice(FUNNY_ENDING)
            return haiku
    pads = ['な', 'か', 'ね', 'よ', 'わ', 'の']
    lines = []
    ptr = 0
    targets = [5, 7, 5]
    for need in targets:
        acc = []
        while len(acc) < need and ptr < len(moras):
            acc.append(moras[ptr]); ptr += 1
        while len(acc) < need:
            acc.append(random.choice(pads))
        lines.append(''.join(acc))
    haiku = '\n'.join(lines)
    if random.random() < 0.25:
        haiku = haiku + ' ' + random.choice(FUNNY_ENDING)
    return haiku


def count_syllables_en(word: str) -> int:
    w = re.sub(r'[^A-Za-z]', '', word).lower()
    if not w:
        return 0
    w = re.sub(r'(?:es|ed)$', '', w)
    m = VOWELS.findall(w)
    return len(m) if m else 1


def build_line_en(target: int, words):
    fillers = ["softly", "quiet", "spark", "tiny", "sleepy", "cosmic", "silly", "strange", "lonely", "cheeky", "noisy", "bouncy"]
    used = []
    pool = list(words) + fillers
    total = 0
    attempts = 0
    while total < target and attempts < 50:
        attempts += 1
        cand = random.choice(pool)
        syl = count_syllables_en(cand)
        if total + syl <= target:
            used.append(cand)
            total += syl
        else:
            small = [w for w in pool if count_syllables_en(w) <= (target - total)]
            if not small:
                break
            s = random.choice(small)
            used.append(s)
            total += count_syllables_en(s)
    while total < target:
        used.append(random.choice(['a', 'oh', 'ha', 'so', 'now', 'sky', 'sun']))
        total += 1
        if len(used) > 20:
            break
    line = ' '.join(used)
    if random.random() < 0.3:
        line = line + ' ' + random.choice(FUNNY_ENDING)
    return line


def generate_haiku_en(input_text: str) -> str:
    words = re.findall(r"[A-Za-z0-9\-']+", input_text)
    uniq = []
    for w in words:
        if w not in uniq:
            uniq.append(w)
    pool = uniq[:20] if uniq else ["cosmos", "tea", "robot", "cat", "star", "moon", "pancake"]
    l1 = build_line_en(5, pool)
    l2 = build_line_en(7, pool)
    l3 = build_line_en(5, pool)
    return '\n'.join([l1, l2, l3])


def generate_haiku(input_text: str) -> str:
    if not input_text or not input_text.strip():
        return '空の入力です。\nテキストを入れて\nください。'
    if is_japanese(input_text):
        try:
            return generate_haiku_jp(input_text)
        except Exception:
            pass
    return generate_haiku_en(input_text)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        text = params.get('text', [''])[0]

        haiku = generate_haiku(text)

        body = json.dumps({"haiku": haiku}, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
