# NeCA基線選擇與臨床推論邊界

彭楚天 D26092110395｜2026-11-18

**結論：**本作業選NeCA作可追溯的逐例重建基線；現有三篇證據不足以支持跨方法臨床優越性排名。

**逐例基線。**NeCA以兩張投影及已知幾何逐例優化隱式血管場，不需隊列預訓練或三維GT監督。[[S1:C1]] NeCA的觀測由分割CCTA模擬；合成評估不能直接當成真實ICA的三維驗證。[[S1:C2]]

**學習先驗。**3DGR-CAR先訓練U-Net預測高斯中心，再逐例優化高斯表示，不能視為完全無預訓練方法。[[S2:C1]] 3DGR-CAR採ImageCAS與ASOCA的CCTA衍生模擬投影；資料與指標不同，不能和NeCA跨文獻直接排名。[[S2:C2]]

**運動與評估。**DeepCA以監督式生成模型處理非同時雙投影；訓練資料的運動模擬主要為剛體旋轉與平移。[[S3:C1]] DeepCA的臨床評估使用二維再投影；這不足以證明任意非剛體補償或三維解剖準確。[[S3:C2]]

**後續建議。**先固定觀測、幾何、三維評分參考與優化預算，再分別測試相機誤差和已知形變；同時檢查三維形態、中心線連通與留出視角。這是由上述證據導出的測試建議，不是本輪新增的重建實驗結果。

**來源與定位**（引用編號對應來源包中的主張欄位）
- S1 NeCA（2024）：§2.1–2.3、Discussion。https://pmc.ncbi.nlm.nih.gov/articles/PMC11673243/
- S2 3DGR-CAR（2024）：§2、§3.1、表1。https://papers.miccai.org/miccai-2024/005-Paper1015.html
- S3 DeepCA（2025）：§3.1–3.2、§4.3–4.4。https://openaccess.thecvf.com/content/WACV2025/html/Wang_DeepCA_Deep_Learning-Based_3D_Coronary_Artery_Tree_Reconstruction_from_Two_WACV_2025_paper.html
