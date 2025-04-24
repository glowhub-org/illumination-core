import json, argparse, pandas as pd

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return pd.read_json(f)

def calc(df, w_c=0.5, w_r=0.5):
    c_norm = df["citations"] / df["citations"].max()
    r_norm = df["external_contradictions"] / df["external_contradictions"].max()
    df["illumination"] = w_c * c_norm + w_r * r_norm
    return df[["id", "title", "illumination"]]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/shadow_sample.json")
    parser.add_argument("--wc", type=float, default=0.5)
    parser.add_argument("--wr", type=float, default=0.5)
    args = parser.parse_args()

    df = load(args.data)
    out = calc(df, args.wc, args.wr)
    print(out.to_markdown(index=False))
