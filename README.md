# AT3 NeCA 雙視角冠脈重建簡化復現

彭楚天 D26092110395。私有課程倉庫，包含文獻綜述、簡化復現、實際結果圖及完整可運行源碼。

## 作業文件

- [六篇結構化文獻綜述](AT3-文獻結構化綜述.D26092110395彭楚天.docx)：含CVPR2024與NeurIPS2024正式主會論文。
- [一頁文獻摘要](AT3-一頁文獻摘要.D26092110395彭楚天.docx)。
- [NeCA復現說明與五張結果圖](AT3-NeCA復現說明.D26092110395彭楚天.docx)。
- [完整代碼及實測數據包](AT3-NeCA-code.D26092110395彭楚天.zip)：解壓後為`NeCA-reproduction/`，保留完整源碼目錄、README、23個固定作者文件、數據來源與腳本、投影／三維輸出、指標、圖表和執行記錄。

## 發布狀態

已發布至本私有課程倉庫；完整包中的執行紀錄與JSON回執均記錄相同GitHub地址及私有狀態。源碼在ZIP內保留完整目錄，根目錄run.py先核對SHA256再解壓執行。教師須獲授權後訪問。此次修訂只更新發布說明與包校驗值，未更改實驗輸出或指標。

## 本次實際結果

2026-10-28，NVIDIA A30，公開處理數位案例，64³體積與兩張128²連續模擬投影，seed42，作者迴圈實際5001次更新。三維Dice **0.772727**、IoU **0.629630**、投影MSE **6.260770793×10⁻⁵**，checkpoint重載最大差0。新運行與2026-10-08既有三組形變對照分開保存。

這是簡化單例工程復現；原文128³多例、90°角度、臨床與跨病例泛化均不能由此結果推定。GT只用於離線生成觀測及輸出鎖定後評分，不進入訓練損失。

## 查看與重跑

下載上述ZIP，或clone此倉庫後執行：

```bash
python run.py verify
python -m pip install -r requirements-analysis.txt
python run.py evaluate
python run.py plot
```

真實訓練需Linux、CUDA GPU、相容Toolkit與GCC>=9，安裝條件及實測版本詳見完整包README。配置相容PyTorch後：

```bash
python -m pip install -r requirements-training.txt
python run.py train --epochs 5000 --seed 42 --output results/rerun
```

`run.py`會先檢查完整包SHA256，再將其安全解壓到`NeCA-reproduction/`並呼叫原包入口。評分及繪圖可用CPU；訓練使用作者CUDA hash與ASTRA投影器。固定seed不保證CUDA逐bit確定。執行驗證不會重新訓練模型。

## 原始來源與資料使用

NeCA作者碼固定commit `77246df0826a031c12072f6ea64bb3370a0baf6b`，MIT許可隨包保留：<https://github.com/WangStephen/NeCA>。

Wang Y, Banerjee A, Grau V. *Bioengineering*2024,11(12):1227. <https://doi.org/10.3390/bioengineering11121227>。

公開處理資料來源為DeepCA的CCTA_GT/1.npy，並非醫院原始CTA或真實造影配對。資料取得與衍生步驟隨包記錄；程式MIT許可不自動授予上游資料再分發權，本倉庫維持私有供課堂查核。

AI協助文獻查核、程式封裝、繪圖與文字整理；數值來自真實運行與獨立復算。繪圖流程參照Kassis等Scientific Agent Skills2026，<https://doi.org/10.48550/arXiv.2609.00065>；工具文獻不計入六篇領域文獻。
