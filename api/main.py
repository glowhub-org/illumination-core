# api/main.py  🚀 4‑Axis β backend

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---- 自作モジュール ----------------------------------------------------
from scripts.compute_score import compute_vector
from scripts.fetch_data import get_c, get_r, get_u, get_dh
# -----------------------------------------------------------------------

app = FastAPI()


# ────────────────────────────────────────────────────────────────────────
# シンプルな疎通確認用
@app.get("/ping")
async def ping():
    return {"message": "pong"}


# ────────────────────────────────────────────────────────────────────────
# /score エンドポイント
class ScoreReq(BaseModel):
    url: str | None = None   # DOI / URL
    text: str | None = None  # Raw text

@app.post("/score")
async def score(req: ScoreReq):
    """
    4 軸照度スコアを返す
    • Raw text があれば ΔH のみ計算
    • URL/DOI があれば C/R/U を取得
    """
    try:
        # ---------- Raw text ルート ----------
        if req.text:
            c = r = u = 0
            dh = get_dh(req.text)

        # ---------- URL / DOI ルート ----------
        elif req.url:
            doi = req.url.replace("https://doi.org/", "")
            c  = get_c(doi)
            r  = get_r(doi)
            u  = get_u(req.url)
            dh = 0  # Abstract 未取得（簡易版）

        else:
            raise HTTPException(status_code=400, detail="url か text のどちらかを指定してください")

        return compute_vector(c, r, u, dh)

    except Exception as e:
        # 例外をそのまま投げ返すと Streamlit 側で表示しやすい
        raise HTTPException(status_code=500, detail=str(e))

