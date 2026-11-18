> AT3 historical snapshot (2026-10-28); publication/access statements describe that date. Current status: repository made Public on 2026-11-18 per owner confirmation; see root README.

# 資料取得與離線準備

1. 前往DeepCA作者官方庫 <https://github.com/WangStephen/DeepCA>，按作者資料說明取得CCTA.zip，先確認使用及再分發條件。課堂本地包已包含實際用過的64³衍生輸入與評分參考；這不構成上游再分發授權證明。
2. 在README所列CUDA訓練環境、專案根目錄執行：

```bash
python scripts/prepare_data.py /path/to/CCTA.zip --output data/reprepared
python scripts/train.py --epochs 5000 --seed 42 \
  --projections data/reprepared/observed/projections.npy \
  --geometry data/reprepared/observed/geometry.yaml \
  --output results/reprepared
python scripts/evaluate.py --run results/reprepared \
  --observations data/reprepared/observed/projections.npy \
  --reference data/reprepared/evaluation_only/reference_A.npy
```

準備腳本取CCTA_GT/1.npy（128³二值作者處理陣列），2×2×2 max-pool為64³，使用固定作者幾何產生兩張128²連續線積分。數位參考不是原始CT灰階；陣列沒有病人原始affine／spacing。1.6mm為本次指定的合成單位。此離線準備階段可以讀GT；訓練入口只接收投影與幾何，不接收GT。評分在訓練輸出保存後才讀參考。

公開發布時保留此取得說明與準備腳本，資料檔案及包含參考體／觀測的結果陣列由.gitignore排除。讀取已授權本地包的教師仍可重算完整結果，無需重新下載。
