import os, sys, subprocess, json
from pathlib import Path

def run(args, env=None):
    res = subprocess.run([sys.executable, "-m", "Rick_MK2.rick", *args],
                         capture_output=True, text=True, env=env)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def test_status_with_dict_schema(tmp_path: Path):
    p = tmp_path / "rick.json"
    p.write_text('{"logs":[]}', encoding="utf-8")
    code, out, _ = run(["status", "--json"], env={**os.environ, "RICK_DATA": str(p)})
    assert code == 0
    assert out == '{"total": 0, "last": null}'

def test_status_with_list_schema(tmp_path: Path):
    p = tmp_path / "rick.json"
    p.write_text('[]', encoding="utf-8")
    code, out, _ = run(["status", "--json"], env={**os.environ, "RICK_DATA": str(p)})
    assert code == 0
    assert out == '{"total": 0, "last": null}'

def test_status_with_bom(tmp_path: Path):
    p = tmp_path / "rick.json"
    p.write_bytes(b"\xef\xbb\xbf" + b'{"logs":[]}')
    code, out, _ = run(["status", "--json"], env={**os.environ, "RICK_DATA": str(p)})
    assert code == 0
    assert out == '{"total": 0, "last": null}'
