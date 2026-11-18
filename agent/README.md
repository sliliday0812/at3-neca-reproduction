# AT3 NeCA 離線來源整理與步數比較

彭楚天 D26092110395｜2026-11-18

本包完成AT3第三部分的自建來源包版本：由Codex主會話實際調用本地工具，查找NeCA、3DGR-CAR和DeepCA的三份已核對來源摘編，撰寫一頁研究簡報，並比較max_steps=3和6。來源與驗證器均為本作業自建，並非教師fixture；課程是否接受替代來源／驗證器尚未獲教師確認。

## 直接查看的交付檔案

- final-brief.md：正式研究簡報，一頁排版預覽已核對。
- task-contract.json：共同任務、來源、六項必要證據、預算及評分規則。
- tool-schema.json：四個工具、參數與安全範圍。
- trajectory.jsonl／tool-results.jsonl：max6正式完成組的六次真實請求及回應。
- evaluation.csv：兩組實際結果及固定條件SHA256。
- error-note.md：短預算失敗、已完成的修復路徑和限制。
- provenance.json：來源、Agent／執行器、模型身分可核實範圍及重跑邊界。
- AT3-Agent分析.D26092110395彭楚天.docx：兩頁分析。

sources/保存三篇原始論文的學生摘編及凍結manifest；每一主張含正文定位、官方URL，並保留原始歸檔文字SHA256。這不是三篇全文的新下載或現場全文通讀，也不把來源摘編冒稱作者原始全文。引用[[S1:C1]]對應S1.json內的C1，其他同理。

runs/max3和runs/max6保留各組完整證據。max3沒有final-brief.md是實際觀察到的預算耗盡結果，不是遺漏正式提交；根目錄正式簡報來自完成的max6。根目錄軌跡為max6副本，不是額外的一次實驗。

## 無API、無GPU離線重跑

Python 3標準庫即可，從此目錄執行：

```bash
python scripts/agent_lab.py validate max6
python scripts/agent_lab.py replay
python scripts/self_check.py
```

validate應為pass=true。replay以真實已記錄請求在臨時目錄重放，max3仍false、max6仍true；它不是新的模型推理。self_check還檢查請求回應一一對應、兩組前三次請求相同及六類拒絕案例。

## 任務執行與比較邊界

這不是預寫fixture冒充模型回答：各次請求由本次Codex會話發起；Python只負責執行工具、記錄及驗證。核心執行未呼叫外部LLM API，亦無模型下載或GPU計算。模型requested欄是使用者偏好，runtime_verified=false表示沒有可用證據確認當前主會話的精確型號與推理檔位，沒有聲稱自動切換。

每次搜尋、單來源讀取、寫作及驗證各計一次工具呼叫；建立／關閉run及外部審計不計入Agent工具預算。最小完整路徑為1搜尋＋3讀取＋1寫作＋1驗證，共6次；這種工具粒度下3次必然不足，因此本比較是流程預算示範，不能當作模型能力或最佳步數的因果證據。同一會話先跑max3、再跑max6，既有上下文並未清空；來源引用仍要求該run內真實讀取證據。

驗證器檢查13個結構／來源／引用／預算條件，不獨立證明所有科學推論正確，也不代表教師評分。主張正確性另外回查既有原文。根目錄validation.json和validation-tests.json是實際執行結果。

## 課程適用範圍

作業文字說「指定來源包」及final-state validator，並未明寫一定由教師提供。本包可完整展示要求的工作及比較；若課程另有指定fixture、來源、認可工具或validator，應將同一工具流程套用其正式材料後重跑，不能聲稱本自建版本已獲教師認可。

前兩部分文件不變。本部分只整理來源與評估工具工作流，未新增NeCA模型訓練或臨床實驗。
