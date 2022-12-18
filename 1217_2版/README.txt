1217_2版內含檔案：
Dash.py -> Dashboard的program
Test.csv -> 測試資料，資料筆數為800000
Sample.txt -> 地圖中選居後的SelectedData的資料範例
DashBoard.pdf -> 期中時所設計的DashBoard板面
Default.png -> 默認狀態下的DashBoard
任意選取.png -> 使用套索工具選取地圖上的Bubble後的DashBoard
方框選取.png -> 使用方框選取工具選取地圖上的Bubble後的DashBoard

最新版本：
所有Figure正確顯示
根據地圖和其他的Figure的interactive已完成
	-> 地圖選取資料時，其他的Figure會更新Data

目前問題：
資料筆數過多載入時間過長
目前筆數的數據在互動時其他Figure更新的速度很慢，大約等2分鐘全部Figure才會更新完資料
	Figure更新速度：Bar Chart > Pie > Heat Map > Line Chart
	猜測原因：Figure在繪圖前的算法runtime較長 -> 後期可能要做計算的優化

----------------------------------------------------------

Mapbox：
顯示每個路段的總流量，以Bubble形式表示其路段的車流量大小

Bar Chart：
預設為地圖上所有Color Bubble的數量統計，當地圖SelectData不為None時，Bar Chart會對SelectData中所包含的Bubble數量進行統計並顯示結果

Heat Map：
預設為所有資料在每個星期中，早午晚三個時段的總車流量大小的密集程度，當地圖SelectData不為None時，Heat Map會計算SelectData中所包含的路段的總車流量大小的密集程度並顯示結果

/* 以上三個Figure的Label Color相同 */
/* 少 -> 多： Blue，Green，Yellow，Orange，Red */

Pie Chart：
預設為地圖上所有資料的車輛比例，當地圖SelectData不為None時，Pie Chart會計算SelectData中所包含的路段中各車輛佔比並顯示結果

Line Chart：
預設為所有資料中各車輛每一日的平均速度，當地圖SelectData不為None時，Line Chart會計算SelectData中所包含的路段中各車輛每一日的平均速度並顯示結果

/* 以上兩個Figure的Label Color相同 */
/* Orange： Big Car*/
/* Yellow： Car */
/* Green： Motor */