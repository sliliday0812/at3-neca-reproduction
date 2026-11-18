# AT4 NeCA：單例復現、形變敏感性與 Agent 來源整理

彭楚天 D26092110395。AT4 延伸既有 AT3 的真實單例復現與歷史形變對照，將可執行源碼、觀測／評分資料、結果與 Agent 證據直接展開。根目錄 `run.py` 直接呼叫源碼，不依賴 ZIP 解壓。

公開課程倉庫：[sliliday0812/at3-neca-reproduction](https://github.com/sliliday0812/at3-neca-reproduction)。依本人確認，倉庫於 **2026-11-18** 從 Private 改為 Public；教師無需登入或個別邀請。本倉庫同時保留AT3提交入口，AT4新增完整論文、展開源碼及真實補充實驗。`docs/AT3-README-20261028-historical.md` 及原始 provenance 中 Private／發布前提醒屬歷史記錄，不代表目前存取狀態。

AT4新增四個條件已於2026-11-18真實完成，見`results/at4/`。`current`與C0/C1/C2保留原日期。完整9頁論文見[paper.pdf](paper.pdf)；文獻為10篇領域論文＋1篇工具參考。

## 直接使用

Python 3.10 及以上可進行 CPU 評分與繪圖；Agent 檢查只用 Python 標準庫。

```bash
python -m pip install -r requirements.txt
python run.py verify
python run.py evaluate --output results/current/cpu-evaluation.json
python run.py plot
python run.py agent-validate
python run.py agent-replay
python run.py agent-selfcheck
```

`verify` 核對固定版本的所有保留作者檔案。`evaluate` 只讀已鎖定輸出並以嚴格 `>0.5` 閾值計算三維 Dice、IoU 及投影 MSE。`plot` 由真實陣列生成五張圖與輸入雜湊記錄，不啟動訓練。重算歷史 C0（C1/C2 同理）：

```bash
python run.py evaluate --run results/historical/C0 --reference results/historical/C0/reference_A.npy --observations results/historical/C0/projections.npy --output results/historical/C0/cpu-evaluation.json
```

## 原始實測與證據邊界

2026-10-28，NVIDIA A30，單例 64³ 體積、兩張 128² 合成投影、seed 42，作者迴圈 epoch 索引 0–5000，**實際 5001 次更新**。Dice **0.772727**、IoU **0.629630**、投影 MSE **6.260770793×10⁻⁵**；當時 checkpoint 重載最大差 0。來源為 `results/current/run.json` 及保存陣列。checkpoint 本體不在此精簡樹中，因此此次 CPU 核驗重算的是輸出數值，沒有重新驗證 checkpoint 載入。

C0/C1/C2 是 **2026-10-08** 的歷史形變敏感性對照，保存在 `results/historical/`，與 2026-10-28 current 分開。C0 靜態、C1 剛體、C2 非剛體均只是一個數位案例；不同觀測擬合後相對 A 參考評分，不能當成臨床跨病例泛化或一般因果結論。

GT 只用於**離線生成觀測和訓練輸出鎖定後評分**；訓練讀取投影與幾何，沒有 GT 損失或 GT 參數。作者單 bin ODL 分區對應的兩視線夾角約 **19.865°**，不是原文 90°。觀測生成與擬合使用同一投影器，因此低投影 MSE 不能獨立證明三維正確或相機幾何正確。

原文使用 128³ 體積、512² 投影、RCA 67／LAD 79 條目，且做小物件後處理。本例使用降採樣 64³／128²、未刪除 <25 體素物件，資料、幾何、病例數和後處理均不等條件。原文 RCA Dice 90.43±7.46% 只能作背景參考；投影 MSE 也不等於原文三維 reMSE。這不是全量論文等效復現，亦無速度或排名優勢證據。


## AT4新增受控結果

| 條件 | 前景體素 | Dice | IoU | 投影MSE |
|---|---:|---:|---:|---:|
| seed 0 / 5001 | 510 | 0.726358 | 0.570300 | 0.00011909366 |
| seed 1 / 5001 | 464 | 0.778481 | 0.637306 | 7.4128871e-05 |
| seed 42 / 1001 | 0 | 0.000000 | 0.000000 | 1.4425556 |
| seed 42 / 3001 | 487 | 0.667353 | 0.500773 | 0.00031385669 |
| seed 42 / 5001 | 484 | 0.772727 | 0.629630 | 6.2607708e-05 |

三個完整預算種子Dice均值0.759189、樣本SD0.028577；n=3是同例計算重複，非患者。seed42/5001沿用2026-10-28，另外四條件為2026-11-18。每種子僅一次，變異亦可能含CUDA非確定性與批次差異，不能純歸因於初始化。三個seed42條件的初始參數雜湊一致。

**1001更新是完成執行後的負結果。** 它保存有限的空前景輸出且重載差0，訓練封裝與評分器的非空品質門檻返回退出1；並非未執行，也未提高預算或更改閾值使其假裝成功。獨立分析程式保留此條件，計算Dice／IoU=0，並核對所有五個唯一條件。

```bash
python run.py analyze-at4
```

這會重建`results/at4/summary.json`、`comparison.csv`與第六張結果圖，不啟動訓練。執行回執與壓縮真實日誌在各條件目錄；較大的checkpoint不隨庫提交，run.json保留其雜湊及當次重載檢查結果。

CPU核驗另以全新工作目錄安裝倉庫聲明的分析依賴，六項入口均已實際執行，版本與結果見[分析環境紀錄](docs/AT4-analysis-environment.json)。訓練與CPU核驗的環境分開記錄。

## AT3原提交入口

- [原三部分提交ZIP](AT3-最终提交.D26092110395彭楚天.zip)
- [原逐項提交清單](SUBMISSION_CHECKLIST.md)
- 舊根目錄`agent.py`仍可使用原證據ZIP；新入口使用`agent/`展開源碼。AT3歸檔及歷史commit保持原有實驗記錄。

## 目錄與依賴

| 路徑 | 用途 |
|---|---|
| `src/` | 可移植訓練封裝、獨立評分、繪圖、資料準備和作者碼校驗 |
| `vendor/NeCA/` | 固定 commit 的作者原檔及 MIT LICENSE；保留檔案逐位元不改 |
| `data/observed/` | 訓練使用的投影與幾何 |
| `data/evaluation_only/` | 僅離線準備／訓練後評分使用的三維參考 |
| `results/current/` | 2026-10-28 真實結果 |
| `results/at4/` | 2026-11-18種子與預算條件、彙總與真實日誌 |
| `results/historical/` | 2026-10-08 C0/C1/C2 歷史結果 |
| `figures/` | 六張結果圖及其來源紀錄，可用CPU重生成 |
| `agent/` | AT3 完整來源、軌跡、兩組結果及驗證程式，維持相對目錄 |
| `docs/` | 上游雜湊、執行記錄、資料來源、恢復來源及 CPU 核驗結果 |

`requirements.txt` 引用 `requirements-analysis.txt`，僅包含 NumPy、Matplotlib、PyYAML 及 scikit-image 的 CPU 分析環境。`requirements-training.txt` 是另一套 CUDA 訓練依賴，不會因安裝分析環境自動安裝大型訓練庫。

## CUDA 訓練

訓練需 Linux、NVIDIA GPU、相容 CUDA Toolkit 和 GCC≥9；作者 hash encoder 與 ASTRA CUDA 投影器不能用本 Mac CPU 替代。本次歷史環境是 Python 3.10.16、PyTorch 2.5.1／CUDA 11.8、A30、NumPy 1.26.2、ODL 0.8.3、ASTRA 2.2.0；這也不是作者舊環境的逐版本重建。先依 PyTorch 官方來源配置相容 PyTorch 與 CUDA，再執行：

```bash
python -m pip install -r requirements-training.txt
export CUDA_HOME=/usr/local/cuda-11.8
export MAX_JOBS=2
export TORCH_CUDA_ARCH_LIST=8.0  # A30；其他 GPU 按實際架構調整
python run.py train --epochs 5000 --seed 42 --output results/rerun
python run.py evaluate --run results/rerun --output results/rerun/evaluation.json
```

預設輸出為 `results/rerun`；使用新的目錄保留歷史。`--epochs 5000` 對應 5001 次更新。固定 seed 不保證 CUDA atomicAdd 逐 bit 確定；當時重載一致只能證明同一 checkpoint 可恢復。

## Agent 的適用範圍

第三部分沿用 AT3 **自建來源／validator，尚未獲教師確認接受**。3 個來源、6 個引用、13 項本地條件檢查不能冒稱官方驗收。`agent-validate` 檢查完成組 max6；`agent-replay` 在臨時目錄重放已記錄的真實工具請求，max3 仍失敗、max6 仍通過，並非新模型推理。`agent-selfcheck` 含六類拒絕案例。

比較只變更 max_steps=3／6；任務、來源、工具粒度和 rubric 固定。1 次搜尋＋3 次單源讀取＋寫作＋驗證需 6 步，因此本例不能用來宣稱模型能力提升或一般最優步數。同一會話先 max3 後 max6，上下文未清空，且只有一次配對，限制保留在 `agent/` 證據中。

## 來源、資料與歷史狀態

作者：[WangStephen/NeCA](https://github.com/WangStephen/NeCA)，固定 commit `77246df0826a031c12072f6ea64bb3370a0baf6b`；[原文 DOI](https://doi.org/10.3390/bioengineering11121227)。作者碼 MIT 許可隨 `vendor/NeCA/LICENSE` 保留，只省略原倉庫舊 Python bytecode。

資料來自 [DeepCA](https://github.com/WangStephen/DeepCA) 公開處理 `CCTA.zip` 的 `CCTA_GT/1.npy`，經 2³ max-pool 降採樣；不是醫院原始 CTA 或真實配對造影。1.6 mm 為工程合成單位，沒有病人 affine／spacing。`data/PROVENANCE.json` 保留當時記錄，資料準備流程見 `docs/data-preparation.md`。程式 MIT 不自動授予上游資料再分發權；本人確認公開的是倉庫存取狀態，不等於重新核定上游資料授權。

既有19份AT3陣列由原完整代碼ZIP原樣恢復，新增四條件則來自2026-11-18的實際訓練輸出。原AT3完整包的SHA256與恢復核對保留於本地審核，公開核驗摘要見`docs/AT4-verification.json`。AT4 整理不改寫原實驗日期、不新增未執行數值。AI 協助源碼封裝、查核、圖表與文字整理；數值來自實際已保存輸出及 CPU 獨立復算。發布倉庫不等於已提交課程平台。
