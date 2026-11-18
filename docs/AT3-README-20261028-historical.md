# NeCA 雙視角冠脈三維重建簡化復現

AT3 作業②，彭楚天 D26092110395。此專案使用固定版本 NeCA 作者網路、hash encoder、可微錐束投影、投影 MSE 與原訓練迴圈，完成一個64³公開處理案例的實際優化、輸出與獨立評分。原始碼和輔助封裝分開，GT只供離線生成觀測與訓練後評分。

- 本作業GitHub（私有，已發布）：<https://github.com/sliliday0812/at3-neca-reproduction>；教師須獲授權後訪問。
- 作者碼：<https://github.com/WangStephen/NeCA>
- 固定 commit：`77246df0826a031c12072f6ea64bb3370a0baf6b`
- 原文：Wang, Banerjee, Grau. *Bioengineering*2024,11(12):1227. <https://doi.org/10.3390/bioengineering11121227>
- 本次結果：`results/current/run.json`和`evaluation.json`；先前2026-10-08形變對照：`results/historical/`。兩批不得混寫成同日新實驗。

## 本次實測結果

2026-10-28單例5001次更新，Dice **0.7727**、IoU **0.6296**、投影MSE **6.2607708e-05**，約9.75分鐘，checkpoint重載最大差0。原文RCA Dice90.43±7.46%為67條目128³的不同條件；單例簡化結果不能當成原文全量重現。詳見`docs/execution-receipt.json`和復現DOCX。

## 目錄

- `vendor/NeCA/`：固定作者原碼及MIT LICENSE；只省略舊Python3.8預編譯快取，不改剩餘作者檔案。
- `scripts/train.py`：路徑可移植的封裝，呼叫作者訓練主程式並記錄損失、時間及checkpoint重載。
- `scripts/evaluate.py`：NumPy獨立評分，訓練後才讀GT。
- `scripts/plot_results.py`：重建、三軸誤差投影、投影殘差、損失與歷史對照圖。
- `scripts/verify_upstream.py`：作者碼逐檔SHA256校驗。
- `data/observed/`：雙投影與相機設定，訓練唯一的資料輸入。
- `data/evaluation_only/`：三維數位參考，只在評分階段讀取。
- `figures/`：作業要求的結果圖，含圖說與轉換／輸入雜湊manifest。
- `docs/`：文獻來源、復現差異與執行記錄。

## 執行條件與安裝

真實訓練需Linux、NVIDIA CUDA GPU、相容CUDA Toolkit和GCC>=9。作者hash CUDA擴展及ASTRA CUDA投影不支援此訓練的Mac/CPU替代；CPU可重算已保存結果與畫圖。本次用A30、Ubuntu22/GCC11.4既有容器，不修改宿主機或其他研究環境。

在獨立環境安裝Python3.10、PyTorch2.5.1+CUDA11.8及CUDA11.8 Toolkit。PyTorch的安裝來源應依其官方指示選擇與驅動相容的版本；本作業實測版本見`results/current/run.json`，不是作者Python3.8/PyTorch1.9環境的嚴格重建。

```bash
python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu118
python -m pip install -r requirements-training.txt
export CUDA_HOME=/usr/local/cuda-11.8
export MAX_JOBS=2
# 視實際GPU設定其compute capability；A30為8.0
export TORCH_CUDA_ARCH_LIST=8.0
python scripts/verify_upstream.py
```

## 重跑一例

從專案根目錄執行。預設重新初始化，不讀歷史checkpoint。請先使用新的輸出目錄，以保留已交付結果。

```bash
python scripts/train.py --epochs 5000 --seed 42 --output results/rerun
python scripts/evaluate.py --run results/rerun
```

作者迴圈含epoch索引0，`--epochs5000`實際執行5001次optimizer更新。64³／128²、lr10^-4、16級hash和8層寬256 MLP已固定。不得根據GT選擇epoch、seed、閾值或初始化。`train.py`沒有GT參數，也拒絕包含GT/reference欄位的訓練幾何檔；評分時才讀三維數位參考。

成功標準：程式退出0、`final_volume.npy`有限且閾值0.5下非空、`run.json`重載差<=1e-6、`evaluation.json`可以由NumPy重算。CUDA hash反向採atomicAdd，固定seed不保證每次訓練逐bit一致；重載一致僅驗證同一checkpoint可恢復。

只需檢查已保存結果時，不必啟動GPU：

```bash
python -m pip install -r requirements-analysis.txt
python scripts/evaluate.py --run results/current
python scripts/evaluate.py --run results/historical/C0 \
  --observations results/historical/C0/projections.npy \
  --output results/historical/C0/cpu-evaluation.json
python scripts/plot_results.py
```

繪圖預設讀本次`results/current`；另一次重跑可直接檢查其JSON，若要換成圖中主結果，應先另存原目錄並同步更改圖說與來源日期，不能覆蓋後仍聲稱原日結果。

## 與論文的差異

本次一例數位參考由DeepCA公開處理陣列降採樣而來，體積64³、探測器128²；原NeCA為128³／512²、RCA67與LAD79條目。Max-pool可能加粗分支。原處理陣列沒有患者affine／spacing；1.6mm僅是本工程指定的合成空間單位。

保留作者單bin ODL角度分區，其實際兩視線夾角約19.865°；不能按相機設定文字推成90°或臨床已標定。產生觀測與擬合採同一投影器，因此低MSE不能獨立證明幾何正確。本次未混入獨立幾何修補版。

本次直接對原始輸出做嚴格`>0.5`二值化，沒有刪除<25體素物件；原論文做了該後處理。三維Dice/IoU與投影MSE分開；原文reMSE是三維重建誤差，不能與投影MSE混同。並列原文數字僅交代差距，不構成相同資料和設定下的排名或速度提升證據。

## 資料來源與發布

資料來源、變換與雜湊見`data/PROVENANCE.json`。完整課堂包已發布於上述私有GitHub倉庫，包含已使用的公開衍生案例，以便重算；NeCA程式MIT許可不等於DeepCA資料的再分發許可。若另行公開發布GitHub版本，應排除`data/`及結果中的原始/參考/投影陣列，保留程式、表格、圖與取得步驟；教師獲授權的課堂包可另行提供。

原始資料取得入口：<https://github.com/WangStephen/DeepCA> 的作者CCTA資料說明。取得作者`CCTA.zip`後使用其中`CCTA_GT/1.npy`；本專案提供離線準備腳本，生成觀測與評分參考，詳見`docs/data-preparation.md`。請先確認上游授權；公開來源不自動表示任意再分發。

## 證據與輔助工具

所有數值以保存的實際輸出、日誌及獨立評分為依據。AI協助文獻查核、程式封裝、圖表和文字整理。科學繪圖流程參照Kassis等(2026), *Scientific Agent Skills*, <https://doi.org/10.48550/arXiv.2609.00065>；此工具文獻不計入AT3第一部分領域文獻數量。
