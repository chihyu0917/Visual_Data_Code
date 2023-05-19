0428更正之處:
1. 增加Choropleth Map: 呈現臺北市各行政區車量大小
	- 問題: 速度超慢，這邊只有先用前50000筆資料。另外，互動還沒完成。
	- 新module: shapely
2. Geojson file: 
	- taipei_districts.json: 只有臺北市
	- taipei_newTaipei_districts.json : 臺北市和新北市
	- 因為json load的問題，建議不要在cmd/terminal執行，直接用python內建"Run without debugging" -> 已解決 
0519更正之處:
1. 增加所有圖表的交集: 現在可圈選/按的圖表有Bubble Map, Heat Map, Line Chart, Pie Chart
	- 問題1 : Line Chart需最後操作且隔幾秒後會回到未圈選狀態，因為Line Chart會自己更新成空集合
	- 問題2 : Bar Chart中的集合(Pie Chart and Line Chart and Bar Chart)無法正常運作，理由為問題1
2. 增加兩文字欄位: Total Volume與Average Speed
3. 更改寫法: 
	- 原Bubble Map的selectedData用路名選擇造成部分點不在圈選範圍內，改用邊界再次檢查
	- 原Bubble Map的Bar Chart與Bubble Map上不同步，所以用interval找出在範圍內的RoadTotal值
	