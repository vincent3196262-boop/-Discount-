# Steam-wishlist-and-lowest-recorded-price
這是一個 Steam 願望清單特價與歷史低價通知 Bot，使用 Github Action 定時執行 python，將 Steam 願望清單的特價中遊戲與其歷史最低價做統整，傳送到 Discord。

# 教學
1.新建一個 Github Repositories，並將所有檔案依照原先路徑上傳 

2.將 Steam 的**個人檔案**與**遊戲資料**設為公開，並把 main.py 第31行的網址改成自己的願望清單網址

3.創建 ZenRows 帳號，點選 Dashboard 後選擇 python，複製 client = ZenRowsClient("引號中的內容")

4.在 **Repositories 的 Settings ➔ Secrets and variable ➔ Actions 建立兩個 Secrets**：
  - Name: ***DISCORD_WEBHOOK_URL***, Secret: ***輸入 Discord webhook 網址***
  - Name: ***ZENROWS_PROXY***, Secret: ***輸入 ZenRowsClient 引號中的內容***
    - 範例：**ZenRowsClient("0c0d35a027d4691f086716f7ba3f6###########")**，在 Secret 中輸入 **0c0d35a027d4691f086716f7ba3f6###########**

5.將 schedule.yml 第5行的 **# 字號**刪除，並把自動執行時間改成自己想要的時段 (注意為 UTC 時區)
