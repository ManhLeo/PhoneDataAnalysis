Phát biểu bài toán: Phân tích dữ liệu nhằm khảo sát tính khả thi cho việc xây dựng mô hình dự đoán biến mục tiêu (target variable) Y từ các biến/đặc trưng (predictors/features) Xi (i=1..N).Trong trường hợp này, biến mục tiêu Y là giá cả điện thoại (price), một biến số thực, do đó bài toán mô hình hóa thuộc nhóm hồi quy (regression). Các biến đặc trưng bao gồm thương hiệu (brand), tên điện thoại (name) RAM (ram), dung lượng lưu trữ (storage), dung lượng pin (battery), và tốc độ sạc (charging). Mục tiêu của phân tích là đánh giá mối quan hệ giữa các biến đặc trưng này và giá cả, từ đó xác định tính khả thi của việc xây dựng mô hình dự đoán giá điện thoại dựa trên các đặc trưng đã cho.
Thu thập dữ liệu: Dữ liệu được thu thập từ web bán hàng của thế giới di động tại Việt Nam (https://www.thegioididong.com/dtdd)
Cách thức thu thập: Sử dụng Python với thư viện BeautifulSoup để truy cập danh sách sản phẩm trên trang web. Trích xuất thông tin từ các trang chi tiết sản phẩm, bao gồm các thông tin: Thương hiệu, tên điện thoại, giá, chip, RAM, dung lượng lưu trữ, dung lượng pin và công suất sạc. Sau đó lưu vào file csv để phân tích.
Số lượng mẫu: 536 mẫu
Số lượng biến: 6 biến đặc trưng (brand, name, chip, ram, storage, battery, charging) + 1 biến mục tiêu (price)
Crawl dữ liệu:
File getlink.py: Crawl link của từng sản phẩm điện thoại trong danh sách sản phẩm từ html của trang web https://www.thegioididong.com/dtdd, các link được crawl sẽ được lưu vào file phone_links_20250402_175607.json. Dữ liệu được lưu dưới dạng { "link": "name": "type": }
File getinfo.py: Crawl thông tin chi tiết của từng sản phẩm điện thoại, bao gồm các hàm để lấy tên sản phẩm, thương hiệu, giá, chip, RAM, dung lượng lưu trữ, dung lượng pin và công suất sạc.
File main.py: 
Thực hiện quá trình thu thập và lưu trữ thông tin về điện thoại từ trang web TheGioiDiDong. Các phần chính:
scrape_phone_details: Duyệt qua các link sản phẩm và thu thập thông tin chi tiết như giá, chip, RAM, dung lượng lưu trữ, pin và sạc.
get_info: Các hàm con lấy thông tin chi tiết từ trang sản phẩm bằng BeautifulSoup.
save_phone_data: Lưu dữ liệu thu thập được vào file CSV, bao gồm thêm cột STT.
crawl_links: Lấy và lưu danh sách các link sản phẩm từ website.
crawl_details: Thu thập thông tin chi tiết từ các link đã lưu.
argparse: Cho phép người dùng chọn chế độ thực thi (crawl links, details hoặc cả hai) thông qua dòng lệnh.

1.	Làm sạch, chuẩn hóa và encoding dữ liệu (Clean&&Nomalization.ipynb)
2.	Xây dựng và lựa chọn đặc trưng (feature_engineering.ipynb)
3.	Trực quan hóa dữ liệu (Trực_quan_hóa.ipynb)
Kết luận: 
-	Mục tiêu đặt ra ở đầu bài toán là khả thi về dữ liệu, vì:  
•	Dữ liệu có sẵn trên website: Các thông tin như tên, giá, thương hiệu, chip, RAM, dung lượng lưu trữ, pin và sạc đều có sẵn và dễ dàng thu thập từ trang web. 
•	Dữ liệu có cấu trúc: Các thông tin này đều có dạng có cấu trúc, dễ dàng trích xuất thông qua kỹ thuật web scraping với BeautifulSoup.
-	Các đặc trưng có thể dùng để xây dựng mô hình là brand, RAM, storage, charging.
Tài liệu tham khảo:
https://phamdinhkhanh.github.io/2019/01/07/Ky_thuat_feature_engineering.html
https://chatgpt.com/
https://drive.google.com/drive/folders/11MxiyaJ-_4gSS0gfRWNe0HNyxdmE-5Ox
https://drive.google.com/drive/folders/1hhPucYRO9UMv-8i3ekGCXFf_TIyYCZ1A




