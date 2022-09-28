# dreamlight-valley-translation-exporter


本工具需要 *Python3.8* 以上的版本


# 使用步驟

1. 將要翻譯的語言文件全部解壓縮到 *src* 資料夾下
2. 執行 *unpack.py* 會將除了 toturial 以外的檔案內的字串取出到 *working* 資料夾內的同名文字檔中
3. 編輯 *working* 內的文字檔進行翻譯
4. 執行 *pack.py* 會將 *working* 資料夾內的文字檔進行編碼儲存到 *temp* 資料夾中，並會在此目錄產生 *LocDB_zh-CN.zip* 的壓縮檔
5. 將 *LocDB_zh-CN.zip* 複製到遊戲內對應資料夾即可測試

# 常見問題
* 遊戲內沒有出現翻譯反而出現一串英文字

    * 請確定working資料夾下的文字檔內有對應的翻譯

# 已知問題
* *toturial.locbin* 內的字串沒有取出，因為該檔案內的有些字串和其他檔案的格式不太一樣，不太確定規則是什麼，雖然可以勉強取出但是沒辦法自動打包，所以乾脆跳過