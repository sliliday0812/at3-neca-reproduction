# AT3 NeCA 文獻綜述 技術復現與Agent工作任務

彭楚天 D26092110395｜三部分材料更新日期：2026-11-18。公開課程倉庫（2026-11-18依本人確認由Private改為Public）；老師無需登入或邀請即可查看。

## 訪問狀態與歷史記錄

目前倉庫為Public，任何人都可查看、下載及fork。既有代碼包中的2026-10-28發布記錄、歷史commit及舊版文件所述Private，是當時的發布狀態；不能把它解讀為目前仍需老師獲邀。最新訪問方式及手動事項以本首頁和SUBMISSION_CHECKLIST.md為準。公開不表示第三部分自建來源／validator已獲教師認可。

## 完整提交入口

- [三部分完整提交ZIP](AT3-最终提交.D26092110395彭楚天.zip)：解壓後根目錄集中四份Word，並含第三部分完整證據目錄及提交清單；不含渲染PDF或製作暫存。
- [逐項提交清單及手動事項](SUBMISSION_CHECKLIST.md)。

作業倉庫連結亦附於復現說明與Agent分析首頁。四份Word不能替代第三部分的必交證據檔；若平台收ZIP，提交完整ZIP並貼上本倉庫連結。

## 三部分內容與核對結論

| 部分 | 文件／入口 | 已完成與適用範圍 |
|---|---|---|
| ① 文獻綜述 | [結構化綜述](AT3-文獻結構化綜述.D26092110395彭楚天.docx)、[一頁摘要](AT3-一頁文獻摘要.D26092110395彭楚天.docx) | 6篇論文，含CVPR2024、NeurIPS2024主會；圖譜／表格與批判分析齊全 |
| ② 技術復現 | [復現說明及5張結果圖](AT3-NeCA復現說明.D26092110395彭楚天.docx)、[完整代碼資料包](AT3-NeCA-code.D26092110395彭楚天.zip)、run.py | 真實單例簡化復現，對照與限制已明示；符合原文允許的小資料版本，未冒稱全量論文等效 |
| ③ Agent任務 | [完整證據包](AT3-Agent-evidence.D26092110395彭楚天.zip)、[一頁簡報](final-brief.md)、[兩頁分析](AT3-Agent分析.D26092110395彭楚天.docx)、[比較結果](evaluation.csv)、agent.py | 自建來源／validator版本：3來源、6引用、13項本地檢查通過；課程是否接受此替代版尚需教師確認 |

三部分均以NeCA及雙視角冠脈重建為主線。第三部分沒有新增模型訓練，也沒有把自建檢查寫成教師驗收；它使用與前兩部分相關的NeCA、3DGR-CAR及DeepCA已核對來源摘編。

## 第三部分離線檢查與重放

```bash
python agent.py validate
python agent.py replay
python agent.py selfcheck
```

Python標準庫即可，不需API、GPU、網路或模型下載。agent.py核對完整證據ZIP的SHA256後安全解壓並調用包內入口；完整源碼、來源與兩組軌跡在ZIP中保留目錄。validate應pass=true；replay重放已記錄的真實工具請求，max3仍失敗、max6仍通過，並非新的模型推理。selfcheck還實測六類拒絕案例。

比較只改max_steps=3與6，任務／來源／工具／validator／rubric固定。搜尋、每次單源讀取、寫作及驗證各計一次，因此3步在此工具粒度下不夠，6步完成；不能以此宣稱模型能力提升或一般最優步數。已披露單次配對、順序和會話上下文限制。

## 提交前本人仍需處理

1. 確認課程接受自選來源包及自建validator；如另有正式指定版本，應重跑同一流程。
2. 將此公開GitHub連結貼入課程提交欄；老師無需個別邀請即可查看。
3. 核對課程平台截止日期、格式要求及實際提交完成狀態；本倉庫發布不等於已在課程平台提交。

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

公開處理資料來源為DeepCA的CCTA_GT/1.npy，並非醫院原始CTA或真實造影配對。資料取得與衍生步驟隨包記錄；程式MIT許可不自動授予上游資料再分發權；此次公開訪問由本人明確確認，不代表上游資料授權已重新核定。

AI協助文獻查核、程式封裝、繪圖與文字整理；數值來自真實運行與獨立復算。繪圖流程參照Kassis等Scientific Agent Skills2026，<https://doi.org/10.48550/arXiv.2609.00065>；工具文獻不計入六篇領域文獻。
