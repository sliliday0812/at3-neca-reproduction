# AT4 文獻來源與主張稽核

核驗日期：2026-11-18。範圍為已批准之NeCA期末報告的定向延伸比較，非系統性回顧，沒有聲稱窮盡全部領域文獻。共10篇領域論文，另列1篇研究輔助工具預印本，不以工具文獻補足領域數量。沒有修改AT3檔案，沒有進行模型實驗或向外發送訊息。

## 檢索與選取

以既有六篇原始文獻為起點，使用題名定向搜尋並開啟正式出版社、CVF、MICCAI、NeurIPS、作者arXiv原文與作者專案頁。新增文獻依「逐例衰減場基礎→測試時適應→動態冠脈→窄夾角雙視角」補齊比較，不以通用軟體、指標或基礎視覺論文湊數。

可重複的主要查詢詞為：`NeCA neural coronary angiography reconstruction two views`、`3DGR-CAR coronary artery reconstruction`、`SAX-NeRF R2-Gaussian sparse view tomography`、`NAF Neural Attenuation Fields`、`PINER Prior-informed Implicit Neural Representation`、`NeRF-CA Dynamic Reconstruction`、`Multi-Stage NeRF MICCAI 2026`。本次沒有呼叫學術索引API或做全量分頁，故無總檢索數、PRISMA或召回率主張。搜尋引擎結果中的第三方資料僅作導向，科學主張以作者原文為據。

## 逐篇一手來源

| 鍵 | 元資料核驗入口 | 本次閱讀狀態與定位 |
|---|---|---|
| P1 NeCA | [MDPI原刊](https://www.mdpi.com/2306-5354/11/12/1227)；[原文存檔](https://pmc.ncbi.nlm.nih.gov/articles/PMC11673243/) | 出版社題名、三名作者、2024、11(12):1227及DOI核驗；沿用AT3原始JATS及全文，重讀§2.1、§2.2、Tables3/5、§4。舊自動抽取檔曾將編輯列入authors；本次以出版社三位作者為準。 |
| P2 3DGR-CAR | [MICCAI正式頁](https://papers.miccai.org/miccai-2024/005-Paper1015.html) | 2024、七名作者、LNCS15007、pp.14–24、DOI核驗；沿用官方PDF及其全文，重讀§2–3.1、Table1。官方頁的站務姓名不是論文作者。 |
| P3 DeepCA | [CVF正式頁](https://openaccess.thecvf.com/content/WACV2025/html/Wang_DeepCA_Deep_Learning-Based_3D_Coronary_Artery_Tree_Reconstruction_from_Two_WACV_2025_paper.html) | 直接網頁開啟曾403，正式CVF搜尋索引仍返回完整作者/BibTeX/摘要；重讀既有CVF原文§3、§4.1–4.3、補充A–B。CVF頁未展示DOI，本次保留正式URL而不匯入未重新解析的DOI。 |
| P4 AutoCAR | [Nature原刊](https://www.nature.com/articles/s42256-025-01025-7)；[作者專案](https://autocar.zyh.sh/) | 原刊搜尋記錄核實2025-04-21、7:730–742、DOI；作者頁核對六名作者及框架。原刊直接開啟跳往不可讀身分頁，沒有新下載原刊PDF；本次重讀AT3已存原文轉錄的Tables1–2及Methods，明確記為「既有原文＋新元資料」。 |
| P5 SAX-NeRF | [CVF正式頁](https://openaccess.thecvf.com/content/CVPR2024/html/Cai_Structure-Aware_Sparse-View_X-ray_3D_Reconstruction_CVPR_2024_paper.html) | 五名作者、CVPR2024、pp.11174–11183核驗；沿用原文PDF，重讀§3、§4.1與Tables1–2。DOI未由本次一手頁確認，留空。 |
| P6 R²-Gaussian | [NeurIPS正式頁](https://proceedings.neurips.cc/paper_files/paper/2024/hash/4f550cb7b30b59553e50cd08a9dbf068-Abstract-Conference.html) | 六名作者、NeurIPS2024 Main Conference Track及DOI核驗；重讀既有原文§4、§5.1、Tables1–2、AppendixB。 |
| P7 NAF | [Springer章頁](https://link.springer.com/chapter/10.1007/978-3-031-16446-0_42)；[作者原文](https://arxiv.org/abs/2209.14540) | 三名作者、MICCAI2022、LNCS13436、pp.442–452與正式DOI核驗；新下載11頁作者原文，重讀§2與§3.1/Table1。不是ECCV論文。 |
| P8 PINER | [CVF正式頁](https://openaccess.thecvf.com/content/WACV2023/html/Song_PINER_Prior-Informed_Implicit_Neural_Representation_Learning_for_Test-Time_Adaptation_in_WACV_2023_paper.html)；[作者倉庫](https://github.com/efzero/PINER) | 三名作者、WACV2023、pp.1928–1938由CVF正式搜尋記錄核驗；直接瀏覽403後以正式CVF PDF成功下載10頁，重讀§3.2–3.3與§4.1。PDF印刷頁碼不連續，定位優先採章節與本地PDF頁。DOI不憑第三方推入。 |
| P9 NeRF-CA | [作者原文](https://arxiv.org/abs/2408.16355)；[作者機構發表記錄](https://research.tue.nl/en/publications/nerf-ca-dynamic-reconstruction-of-x-ray-coronary-angiography-with/) | 四名作者、TVCG2025、31(10):8782–8795、正式DOI與2024初版／2025修訂區分；新下載14頁v2，重讀§IV-C–E及§V-A。機構頁連到正式版；本地閱讀的是作者v2，不聲稱下載了IEEE版。 |
| P10 NeCA++ | [MICCAI2026正式頁](https://papers.miccai.org/miccai-2026/0697-Paper5185.html)；[Springer章頁](https://link.springer.com/chapter/10.1007/978-3-032-38186-6_55) | 四名作者、正式會議身分、LNCS16889、pp.583–593與章DOI核驗；新下載官方11頁原文，重讀§2.2–2.3、§3.1、Table2。會議頁尚稱DOI unavailable，但出版社已提供正式DOI，故以出版社補齊。 |
| P11 工具／AI輔助 | [作者arXiv頁](https://arxiv.org/abs/2609.00065) | 現行v2（2026-09-02），Timothy Kassis、Vinayak Agarwal、Yuhuan He、Darshil Patel、Aubrey M. Brueckner，2026預印本。僅核元資料及摘要，未作領域科學證據，不列入10篇。 |

## 必須保留的證據邊界

1. NeCA的「不需要三維GT監督」描述訓練／優化資源；其三維效能仍以CCTA分割真值評估。不能寫為「不需要任何三維資料」或「臨床三維效能已驗證」。
2. NeCA本文亦評估臨床樣式非正交角度，不採用後續論文導言中「NeCA只假設正交」的過度簡化。正交實驗另有較高結果，兩者不可混寫。
3. DeepCA臨床8名患者不等於879名臨床患者；879是合成資料的RCA條目。臨床投影配準指標不等於三維Dice。
4. 3DGR-CAR的GCP具有監督訓練成本；不能與完全逐例優化方法宣稱相同先驗預算。
5. NAF/SAX-NeRF/R²-Gaussian/PINER均有稀疏重建相關性，但視角數、幾何、重建維度與冠脈雙視角不同，僅作方法比較，不當作相同任務排行榜。
6. NeRF-CA的四組視角序列包含多個心動期，不是兩張靜態影像。其評估刻意排除不同步／呼吸／對比劑不均勻等部分臨床因素。
7. AutoCAR的臨床1.8 mm為二維對應EPE。讀過原文轉錄不代表本次重新取得出版社PDF。
8. NeCA++實驗用80³與RTX5080、約58秒；不能與NeCA原論文128³約1小時作公平速度倍數比較。其CCTA衍生投影及臨床樣式角度不等於真實ICA三維驗證。
9. NeCA++年份並不一致：MICCAI官方BibTeX為2026；Springer章頁First Online/Published為2026-09-25，但「Cite this paper」用2027版權年。references.json分列year/conference_year=2026、publisher_citation_year=2027，正文標識MICCAI2026，避免將其寫成尚未發表的未來論文。
10. 作者倉庫可達、README有安裝說明，只能證明公開入口／文件狀態；本次未做來源碼完整性或實際執行驗證。尤其NeCA++目前頁面已有安裝和輸入輸出說明，不沿用舊「僅占位」結論。

## 檔案與閱讀狀態

`references.json`保存11條可機讀記錄及逐條主張定位；`related-work.zh-Hant.md`只引用P1–P10，正文836個漢字（不計英文與標點），主張與推論分開。新增四篇PDF與抽取文字均保存在`evidence/`，`evidence_manifest.json`記錄大小與SHA-256。PDF抽取使用本機pypdf；NeRF-CA部分字型有解析警告，但方法／資料段落可讀，並以作者HTML全文交叉核對。沒有以摘要冒充全文閱讀。

## 工具與AI輔助引用（不計入領域文獻數）

Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. arXiv:2609.00065. https://doi.org/10.48550/arXiv.2609.00065

建議方法／聲明文字：文獻定向檢索、引用元資料整理及初稿比較使用AI輔助，研究輔助流程參考P11；科學主張以作者原文及正式出版／會議來源逐項核對。AI輸出不作獨立科學證據。
