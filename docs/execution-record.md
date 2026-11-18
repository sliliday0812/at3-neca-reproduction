> AT3 historical snapshot (2026-10-28); publication/access statements describe that date. Current status: repository made Public on 2026-11-18 per owner confirmation; see root README.

# 實際執行與修復紀錄

2026-10-28提交版使用Linux／A30和既有隔離Ubuntu22容器重跑。訓練退出0，epoch索引上限5000，實際5001次更新；seed42；耗時585.115秒（訓練器建立、優化及匯出，之前的CUDA擴展編譯不計入）。

- 最終三維Dice=0.7727272727、IoU=0.6296296296；投影MSE=6.26077079302e-05。
- 輸出有限、前景484體素；checkpoint重新載入最大差為0。主機另用NumPy從保存體積與投影獨立復算，與JSON一致。
- 訓練只讀觀測及幾何；GT只於離線生成觀測及訓練後評分。
- 資料準備腳本由原128³公開處理陣列重新執行：參考逐元素一致、雙投影最大絕對差為0.0。
- 歷史2026-10-08的C0／C1／C2另存historical；本次新運行保存current。固定seed不承諾CUDA逐bit確定。

## 已解決的封裝與顯示問題

作者原歸檔含30個舊Python3.8快取。本次傳輸排除快取後，首輪完整清單校驗報不一致，當時未進入模型訓練。改為校驗23個保留的作者檔案，刪除的是預編譯快取，未更改作者網路／投影器／損失／訓練迴圈。之後校驗通過並完成上述新運行。

本地DOCX渲染初次缺中文字形；以作業私有fontconfig指定Noto中文字體後修復，沒有改系統字體。最終文檔再渲染檢查。

## 發布與資料使用

執行記錄不含SSH帳密或私鑰，命令參照README的可移植形式。程式、圖表與文件已完成本地核驗，並於2026-10-28發布至私有課程倉庫：https://github.com/sliliday0812/at3-neca-reproduction 。首次發布commit為`a19080144b4afb2da5454a1990b5f0c8a3868604`；後續文件同步不代表重新訓練。倉庫包含完整課堂代碼ZIP、校驗ZIP後解壓執行的run.py、三份Word及五張結果圖。教師須獲授權後才能訪問私有倉庫。上游資料再分發權未由程式MIT許可推定；目前完整包僅在私有課程倉庫提供。若另行公開發布，須排除未獲再分發授權的原始／參考／投影陣列，改由合法取得來源重建輸入。
