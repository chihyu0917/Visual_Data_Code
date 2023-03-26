0308更正之處:
目的: 提升效率(2分半 -> 15秒)
1. 刪除經過整筆資料的for loop -> 內建的pivot table進行運算
2. Bubble Map車流量
	- 原本: 將同路段的車流量相加 -> 問題為sensors多的路段車流量較高，且sensors位置為隨機不固定
	- 新: 保留每筆資料的車流量由於同一路段的sensors經緯度不同，代表同道路不同路段的車流量
		因此更改interval從[100000, 200000, 300000, 400000]到[5000, 10000, 20000, 100000]
3. Heat Map: 沒有Tuesday資料所以從缺，之後補上即可改善

0324更正之處:
1. 增加Pie Chart與其他四圖的互動
	- 問題: 選取後，Bubble Map的color和label對不上 (已解決)
2. 增加Line Chart與其他四圖的互動
3. 增加Bar Chart與Bubble Map互動
4. 資料增加從2018/01到2018/03
	- https://drive.google.com/file/d/1SRxLPOYC-uKStkR6ICF4MRN4_lhq6PBH/view?usp=sharing

0325更正之處:
1. 更新了Dash Board的排版
2. Mapbox的style換了更簡潔的地圖引入
3. Mapbox和Bar Chart的分類顏色更換，以及Heapmap的顏色修改為同顏色漸變
4. figure細調
	- Mapbox的圖例改放在地圖左上方->地圖比例放大
	- title的位置全部置中了
	- title的內容有更動

0326更正之處：
1. 優化了get_roadname function
2. 增加Bar Chart與Bubble Map外的圖的互動
3. 調整了heatmap的y坐標 -> 改為星期的縮寫