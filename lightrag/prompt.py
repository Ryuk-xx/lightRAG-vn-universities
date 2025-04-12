from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "Vietnamese"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "geo", "event", "category", "person"]
# PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "location", "program_major", "event", "certificate_document", "subject_skill", "admission_method", "academic_metric"]


PROMPTS["entity_extraction"] = """
---Mục tiêu---
Cho một tài liệu văn bản và một danh sách các loại thực thể, hãy xác định tất cả các thực thể thuộc các loại đó từ văn bản và tất cả các mối quan hệ giữa các thực thể đã xác định.
Sử dụng {language} làm ngôn ngữ đầu ra.

---Các bước---
1. Xác định tất cả các thực thể. Với mỗi thực thể được xác định, trích xuất thông tin sau:
- entity_name: Tên của thực thể, sử dụng cùng ngôn ngữ với văn bản đầu vào. Nếu là tên riêng, viết hoa tên. (Ví dụ: tên trường: Đại Học Bách Khoa Hà Nội)
- entity_type: Một trong các loại sau: [{entity_types}]
- entity_description: Mô tả toàn diện về các thuộc tính và hoạt động của thực thể
Định dạng mỗi thực thể là ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. Từ các thực thể được xác định ở bước 1, xác định tất cả các cặp (source_entity, target_entity) có *liên quan rõ ràng* đến nhau.
Với mỗi cặp thực thể có liên quan, trích xuất thông tin sau:
- source_entity: tên của thực thể nguồn, như đã xác định ở bước 1
- target_entity: tên của thực thể đích, như đã xác định ở bước 1
- relationship_description: giải thích tại sao bạn nghĩ thực thể nguồn và thực thể đích có liên quan đến nhau
- relationship_strength: điểm số (dạng số) cho biết mức độ mạnh của mối quan hệ giữa thực thể nguồn và thực thể đích
- relationship_keywords: một hoặc nhiều từ khóa cấp cao tóm tắt bản chất bao quát của mối quan hệ, tập trung vào các khái niệm hoặc chủ đề thay vì các chi tiết cụ thể
Định dạng mỗi mối quan hệ là ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Xác định các từ khóa cấp cao tóm tắt các khái niệm, chủ đề chính của toàn bộ văn bản. Chúng cần nắm bắt được các ý tưởng bao quát có trong tài liệu.
Định dạng các từ khóa cấp nội dung là ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Trả về kết quả bằng {language} dưới dạng một danh sách duy nhất gồm tất cả các thực thể và mối quan hệ được xác định ở bước 1 và 2. Sử dụng **{record_delimiter}** làm dấu phân cách danh sách.

5. Khi hoàn thành, xuất ra {completion_delimiter}

######################
---Ví dụ---
######################
{examples}

#############################
---Dữ liệu thực tế---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
"""
Ví dụ 1:
Entity_types: [person, technology, mission, organization, geography]
Văn bản:
```
Giới thiệu: Đại học Bách khoa Hà Nội (HUST) là một trong những trường đại học kỹ thuật hàng đầu của Việt Nam, nổi tiếng về đào tạo các ngành kỹ thuật và công nghệ. 

HUST đặc biệt mạnh về các lĩnh vực Công nghệ thông tin, Điện - Điện tử và Cơ khí. 

Các ngành nổi bật nhất của trường bao gồm Khoa học máy tính (xếp hạng 451-500 thế giới), Kỹ thuật Điện - Điện tử (xếp hạng 351-400 thế giới) và Kỹ thuật Cơ khí (xếp hạng 401-450 thế giới). 

Trường cũng được xếp hạng 360 thế giới về lĩnh vực Kỹ thuật và Công nghệ nói chung. 

HUST thường xuyên nằm trong top đầu các trường đại học Việt Nam về nghiên cứu khoa học và công bố quốc tế, đồng thời có nhiều hợp tác quốc tế với các trường đại học hàng đầu trên thế giới.
```

Đầu ra:
("entity"{tuple_delimiter}"Đại học Bách khoa Hà Nội"{tuple_delimiter}"organization"{tuple_delimiter}"Đại học Bách khoa Hà Nội là một trong những trường đại học kỹ thuật hàng đầu của Việt Nam, nổi tiếng về đào tạo các ngành kỹ thuật và công nghệ."){record_delimiter} 
("entity"{tuple_delimiter}"Việt Nam"{tuple_delimiter}"geo"{tuple_delimiter}"Việt Nam là quốc gia nơi Đại học Bách khoa Hà Nội tọa lạc."){record_delimiter}
("entity"{tuple_delimiter}"Công nghệ thông tin"{tuple_delimiter}"category"{tuple_delimiter}"Lĩnh vực thế mạnh của Đại học Bách khoa Hà Nội."){record_delimiter} 
("entity"{tuple_delimiter}"Điện - Điện tử"{tuple_delimiter}"category"{tuple_delimiter}"Lĩnh vực thế mạnh của Đại học Bách khoa Hà Nội."){record_delimiter} 
("entity"{tuple_delimiter}"Cơ khí"{tuple_delimiter}"category"{tuple_delimiter}"Lĩnh vực thế mạnh của Đại học Bách khoa Hà Nội."){record_delimiter} 
("entity"{tuple_delimiter}"Khoa học máy tính"{tuple_delimiter}"category"{tuple_delimiter}"Ngành nổi bật của trường, xếp hạng 451-500 thế giới."){record_delimiter} 
("entity"{tuple_delimiter}"Kỹ thuật Điện - Điện tử"{tuple_delimiter}"category"{tuple_delimiter}"Ngành nổi bật của trường, xếp hạng 351-400 thế giới."){record_delimiter} 
("entity"{tuple_delimiter}"Kỹ thuật Cơ khí"{tuple_delimiter}"category"{tuple_delimiter}"Ngành nổi bật của trường, xếp hạng 401-450 thế giới."){record_delimiter} 
("entity"{tuple_delimiter}"Kỹ thuật và Công nghệ"{tuple_delimiter}"category"{tuple_delimiter}"Lĩnh vực chung của trường, xếp hạng 360 thế giới."){record_delimiter} 
("entity"{tuple_delimiter}"Hợp tác quốc tế"{tuple_delimiter}"event"{tuple_delimiter}"Hoạt động hợp tác với các trường đại học hàng đầu trên thế giới."){record_delimiter} 

("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội"{tuple_delimiter}"Việt Nam"{tuple_delimiter}"Đại học Bách khoa Hà Nội tọa lạc tại Việt Nam."{tuple_delimiter}"địa điểm"{tuple_delimiter}9){record_delimiter} 
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội"{tuple_delimiter}"Công nghệ thông tin"{tuple_delimiter}"HUST mạnh về lĩnh vực Công nghệ thông tin."{tuple_delimiter}"chuyên môn"{tuple_delimiter}8){record_delimiter} 
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội"{tuple_delimiter}"Kỹ thuật Điện - Điện tử"{tuple_delimiter}"HUST mạnh về lĩnh vực Điện - Điện tử."{tuple_delimiter}"chuyên môn"{tuple_delimiter}8){record_delimiter} 
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội"{tuple_delimiter}"Cơ khí"{tuple_delimiter}"HUST mạnh về lĩnh vực Cơ khí."{tuple_delimiter}"chuyên môn"{tuple_delimiter}8){record_delimiter} 
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội"{tuple_delimiter}"Hợp tác quốc tế"{tuple_delimiter}"HUST thường xuyên có hợp tác quốc tế với các trường đại học hàng đầu."{tuple_delimiter}"hợp tác"{tuple_delimiter}6){record_delimiter} 
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội"{tuple_delimiter}"Khoa học máy tính"{tuple_delimiter}"Khoa học máy tính là ngành nổi bật của HUST, xếp hạng 451-500 thế giới."{tuple_delimiter}"chuyên môn"{tuple_delimiter}8){record_delimiter} 

("content_keywords"{tuple_delimiter}"đào tạo kỹ thuật, cơ khí, công nghệ thông tin, xếp hạng quốc tế, nghiên cứu khoa học, hợp tác quốc tế", "HUST"){completion_delimiter}
#############################""", 



    """Ví dụ 2:
    

Entity_types: ["person", "organization", "geo", "event", "category",  "prize"]
Văn bản:
```
Thông Tin Tuyển Sinh 
Dựa trên thông tin từ các nguồn đáng tin cậy trong năm 2025, Đại học Bách khoa Hà Nội (HUST) sử dụng 3 phương thức xét tuyển chính như sau:

1. Xét tuyển tài năng
a) Xét tuyển thẳng học sinh giỏi:
Đối tượng: Thí sinh tốt nghiệp THPT năm 2025, đạt thành tích cao trong các kỳ thi do Bộ GD&ĐT tổ chức:
Được triệu tập tham dự kỳ thi chọn đội tuyển quốc gia dự thi Olympic quốc tế và khu vực
Đoạt giải Nhất, Nhì, Ba trong kỳ thi học sinh giỏi quốc gia
Trong đội tuyển quốc gia tham dự cuộc thi Khoa học kỹ thuật quốc tế
Đoạt giải Nhất, Nhì, Ba trong cuộc thi Khoa học kỹ thuật cấp quốc gia
b) Xét tuyển dựa trên chứng chỉ quốc tế:
Điểm trung bình học tập mỗi năm lớp 10, 11, 12 đạt từ 8.0 trở lên
Có ít nhất 1 trong các chứng chỉ quốc tế như SAT, ACT,...
c) Xét hồ sơ năng lực kết hợp phỏng vấn:
Đối tượng: Thí sinh tốt nghiệp THPT năm 2025, điểm trung bình học tập mỗi năm lớp 10, 11, 12 đạt từ 8.0 trở lên và đáp ứng 1 trong các điều kiện:
Được chọn tham dự kỳ thi học sinh giỏi quốc gia
Được chọn tham dự cuộc thi Khoa học kỹ thuật quốc gia
Được chọn tham dự cuộc thi Đường lên đỉnh Olympia từ vòng tháng
Học sinh hệ chuyên của các trường THPT chuyên
2. Xét tuyển theo điểm thi Đánh giá tư duy (TSA)
Đối tượng: Thí sinh tham dự kỳ thi Đánh giá tư duy do HUST tổ chức
Điều kiện: Đã tốt nghiệp THPT, đạt ngưỡng điểm TSA do HUST quy định
```

Đầu ra:
("entity"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"organization"{tuple_delimiter}"Trường đại học tổ chức tuyển sinh năm 2025 với nhiều phương thức xét tuyển khác nhau."){record_delimiter}
("entity"{tuple_delimiter}"kỳ thi học sinh giỏi quốc gia"{tuple_delimiter}"event"{tuple_delimiter}"Cuộc thi dành cho học sinh giỏi cấp quốc gia, là điều kiện để được xét tuyển vào HUST."){record_delimiter}
("entity"{tuple_delimiter}"kỳ thi chọn đội tuyển quốc gia dự thi Olympic quốc tế và khu vực"{tuple_delimiter}"event"{tuple_delimiter}"Cuộc thi tuyển chọn học sinh tham dự Olympic quốc tế và khu vực, thuộc diện xét tuyển thẳng."){record_delimiter}
("entity"{tuple_delimiter}"cuộc thi Khoa học kỹ thuật quốc tế"{tuple_delimiter}"event"{tuple_delimiter}"Cuộc thi quốc tế về khoa học kỹ thuật dành cho học sinh, là một trong những tiêu chí xét tuyển thẳng."){record_delimiter}
("entity"{tuple_delimiter}"cuộc thi Khoa học kỹ thuật cấp quốc gia"{tuple_delimiter}"event"{tuple_delimiter}"Cuộc thi cấp quốc gia trong lĩnh vực khoa học kỹ thuật, được dùng để xét tuyển thẳng học sinh."){record_delimiter}
("entity"{tuple_delimiter}"cuộc thi Đường lên đỉnh Olympia"{tuple_delimiter}"event"{tuple_delimiter}"Chương trình thi kiến thức dành cho học sinh THPT, được xem là điều kiện xét tuyển trong hồ sơ năng lực."){record_delimiter}
("entity"{tuple_delimiter}"THPT chuyên"{tuple_delimiter}"category"{tuple_delimiter}"Loại hình trường trung học phổ thông dành cho học sinh giỏi, thuộc diện xét tuyển đặc cách."){record_delimiter}
("entity"{tuple_delimiter}"SAT"{tuple_delimiter}"prize"{tuple_delimiter}"Chứng chỉ quốc tế là một trong những điều kiện để xét tuyển vào HUST."){record_delimiter}
("entity"{tuple_delimiter}"ACT"{tuple_delimiter}"prize"{tuple_delimiter}"Chứng chỉ quốc tế tương tự SAT, dùng để xét tuyển vào HUST."){record_delimiter}
("entity"{tuple_delimiter}"kỳ thi Đánh giá tư duy (TSA)"{tuple_delimiter}"event"{tuple_delimiter}"Kỳ thi do HUST tổ chức, là một trong những phương thức xét tuyển chính."){record_delimiter}
("entity"{tuple_delimiter}"Thành viên đội tuyển quốc gia"{tuple_delimiter}"person"{tuple_delimiter}"Những học sinh được chọn vào đội tuyển quốc gia dự thi Olympic quốc tế hoặc cuộc thi khoa học kỹ thuật."){record_delimiter}
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"THPT chuyên"{tuple_delimiter}"Học sinh thuộc hệ THPT chuyên nằm trong diện được xét tuyển hồ sơ năng lực vào HUST."{tuple_delimiter}"ưu tiên xét tuyển, học sinh chuyên"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"kỳ thi Đánh giá tư duy (TSA)"{tuple_delimiter}"HUST tổ chức kỳ thi TSA để xét tuyển sinh viên."{tuple_delimiter}"tổ chức, tuyển sinh"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"SAT"{tuple_delimiter}"SAT là một trong những điều kiện chứng chỉ quốc tế để xét tuyển vào HUST."{tuple_delimiter}"xét tuyển, chứng chỉ quốc tế"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"cuộc thi Đường lên đỉnh Olympia"{tuple_delimiter}"Thí sinh được chọn vào vòng tháng của Olympia có thể nộp hồ sơ năng lực vào HUST."{tuple_delimiter}"điều kiện xét tuyển, năng lực đặc biệt"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"kỳ thi học sinh giỏi quốc gia"{tuple_delimiter}"cuộc thi Khoa học kỹ thuật quốc tế"{tuple_delimiter}"Cả hai đều là điều kiện để xét tuyển thẳng vào HUST, cho thấy định hướng tuyển sinh đề cao năng lực học thuật."{tuple_delimiter}"xét tuyển thẳng, thành tích học thuật"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Thành viên đội tuyển quốc gia"{tuple_delimiter}"cuộc thi Khoa học kỹ thuật quốc tế"{tuple_delimiter}"Thành viên đội tuyển quốc gia là những học sinh được chọn đi thi quốc tế, đủ điều kiện xét tuyển thẳng vào HUST."{tuple_delimiter}"đại diện quốc gia, thành tích học thuật"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"tuyển sinh, xét tuyển thẳng, học sinh giỏi, chứng chỉ quốc tế, Đánh giá tư duy, HUST"){completion_delimiter}
#############################""",

    """Ví dụ 3:
Entity_types: ["organization", "geo", "event", "category"]
Đoạn văn:
```
Chương Trình Đào Tạo 
Dưới đây là chi tiết các chương trình đào tạo và học phí năm 2025 của Đại học Bách khoa Hà Nội (HUST):
1. Chương trình chuẩn
Học phí: 24-30 triệu đồng/năm (tăng 1 triệu so với năm 2024)
Điều kiện: Xét tuyển dựa trên điểm thi tốt nghiệp THPT hoặc điểm thi đánh giá tư duy
Đào tạo bằng tiếng Việt
2. Chương trình Khoa học dữ liệu và Trí tuệ nhân tạo (IT-E10) 
Học phí: 64-67 triệu đồng/năm (tăng 7-11 triệu so với năm 2024)
Điều kiện: Điểm tuyển sinh rất cao, yêu cầu tiếng Anh tốt
Đào tạo hoàn toàn bằng tiếng Anh
Cơ hội thực tập tại các công ty công nghệ hàng đầu
3. Chương trình Logistics và Quản lý chuỗi cung ứng (EM-E14) 
Học phí: 64-67 triệu đồng/năm (tăng 7-11 triệu so với năm 2024)
Điều kiện: Điểm tuyển sinh cao, yêu cầu tiếng Anh tốt
Đào tạo hoàn toàn bằng tiếng Anh
Cơ hội thực tập tại các tập đoàn đa quốc gia
```

Đầu ra:
("entity"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"organization"{tuple_delimiter}"Một trường đại học kỹ thuật hàng đầu tại Việt Nam, cung cấp nhiều chương trình đào tạo khác nhau trong năm 2025."){record_delimiter}
("entity"{tuple_delimiter}"Chương trình chuẩn"{tuple_delimiter}"category"{tuple_delimiter}"Chương trình đào tạo cơ bản tại HUST với học phí thấp hơn, giảng dạy bằng tiếng Việt."){record_delimiter}
("entity"{tuple_delimiter}"Chương trình Khoa học dữ liệu và Trí tuệ nhân tạo (IT-E10)"{tuple_delimiter}"category"{tuple_delimiter}"Chương trình đào tạo chuyên sâu bằng tiếng Anh, có yêu cầu đầu vào cao, liên quan đến AI và khoa học dữ liệu."){record_delimiter}
("entity"{tuple_delimiter}"Chương trình Logistics và Quản lý chuỗi cung ứng (EM-E14)"{tuple_delimiter}"category"{tuple_delimiter}"Chương trình đào tạo chuyên sâu bằng tiếng Anh, tập trung vào logistics và quản lý chuỗi cung ứng."){record_delimiter}
("entity"{tuple_delimiter}"Các công ty công nghệ hàng đầu"{tuple_delimiter}"organization"{tuple_delimiter}"Nơi cung cấp cơ hội thực tập cho sinh viên chương trình IT-E10."){record_delimiter}
("entity"{tuple_delimiter}"Các tập đoàn đa quốc gia"{tuple_delimiter}"organization"{tuple_delimiter}"Nơi cung cấp cơ hội thực tập cho sinh viên chương trình EM-E14."){record_delimiter}
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"Chương trình chuẩn"{tuple_delimiter}"HUST là đơn vị tổ chức chương trình đào tạo chuẩn với mức học phí 24-30 triệu đồng/năm."{tuple_delimiter}"chương trình đào tạo, học phí, tiếng Việt"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"Chương trình Khoa học dữ liệu và Trí tuệ nhân tạo (IT-E10)"{tuple_delimiter}"HUST tổ chức chương trình IT-E10 đào tạo hoàn toàn bằng tiếng Anh với học phí 64-67 triệu đồng/năm."{tuple_delimiter}"chương trình đào tạo, học phí, chuyên ngành công nghệ, tiếng Anh"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Đại học Bách khoa Hà Nội (HUST)"{tuple_delimiter}"Chương trình Logistics và Quản lý chuỗi cung ứng (EM-E14)"{tuple_delimiter}"HUST tổ chức chương trình EM-E14 đào tạo hoàn toàn bằng tiếng Anh với học phí 64-67 triệu đồng/năm."{tuple_delimiter}"chương trình đào tạo, học phí, chuyên ngành quản trị, tiếng Anh"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Chương trình Khoa học dữ liệu và Trí tuệ nhân tạo (IT-E10)"{tuple_delimiter}"Các công ty công nghệ hàng đầu"{tuple_delimiter}"Sinh viên chương trình IT-E10 có cơ hội thực tập tại các công ty công nghệ lớn."{tuple_delimiter}"cơ hội thực tập, hợp tác doanh nghiệp"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Chương trình Logistics và Quản lý chuỗi cung ứng (EM-E14)"{tuple_delimiter}"Các tập đoàn đa quốc gia"{tuple_delimiter}"Sinh viên chương trình EM-E14 có cơ hội thực tập tại các tập đoàn lớn trên thế giới."{tuple_delimiter}"cơ hội thực tập, hợp tác doanh nghiệp"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"chương trình đào tạo, học phí, cơ hội thực tập, đào tạo tiếng Anh, yêu cầu tuyển sinh"){completion_delimiter}
#############################"""
]

PROMPTS[
    "summarize_entity_descriptions"
] = """Bạn là một trợ lý chịu trách nhiệm tạo ra một bản tóm tắt toàn diện về dữ liệu được cung cấp dưới đây.
Cho một hoặc hai thực thể, và một danh sách các mô tả, tất cả đều liên quan đến cùng một thực thể hoặc nhóm thực thể.
Vui lòng nối tất cả chúng thành một mô tả duy nhất, toàn diện. Đảm bảo bao gồm thông tin được thu thập từ tất cả các mô tả.
Nếu các mô tả được cung cấp mâu thuẫn nhau, vui lòng giải quyết các mâu thuẫn và cung cấp một bản tóm tắt duy nhất, mạch lạc.
Hãy chắc chắn rằng nó được viết ở ngôi thứ ba, và bao gồm tên thực thể để chúng tôi có đầy đủ ngữ cảnh.
Sử dụng {language} làm ngôn ngữ đầu ra.

#######
---Dữ liệu---
Thực thể: {entity_name}
Danh sách mô tả: {description_list}
#######
Đầu ra:
"""

PROMPTS["entity_continue_extraction"] = """
NHIỀU thực thể và mối quan hệ đã bị bỏ sót trong lần trích xuất trước.

---Nhớ lại Các bước---

1. Xác định tất cả các thực thể. Với mỗi thực thể được xác định, trích xuất thông tin sau:
- entity_name: Tên của thực thể, sử dụng cùng ngôn ngữ với văn bản đầu vào. Nếu là tên riêng, viết hoa tên. (Ví dụ: tên trường: Đại Học Bách Khoa Hà Nội)
- entity_type: Một trong các loại sau: [{entity_types}]
- entity_description: Mô tả toàn diện về các thuộc tính và hoạt động của thực thể
Định dạng mỗi thực thể là ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>

2. Từ các thực thể được xác định ở bước 1, xác định tất cả các cặp (source_entity, target_entity) có *liên quan rõ ràng* đến nhau.
Với mỗi cặp thực thể có liên quan, trích xuất thông tin sau:
- source_entity: tên của thực thể nguồn, như đã xác định ở bước 1
- target_entity: tên của thực thể đích, như đã xác định ở bước 1
- relationship_description: giải thích tại sao bạn nghĩ thực thể nguồn và thực thể đích có liên quan đến nhau
- relationship_strength: điểm số cho biết mức độ mạnh của mối quan hệ giữa thực thể nguồn và thực thể đích
- relationship_keywords: một hoặc nhiều từ khóa cấp cao tóm tắt bản chất bao quát của mối quan hệ, tập trung vào các khái niệm hoặc chủ đề thay vì các chi tiết cụ thể
Định dạng mỗi mối quan hệ là ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Xác định các từ khóa cấp cao tóm tắt các khái niệm, chủ đề chính của toàn bộ văn bản. Chúng cần nắm bắt được các ý tưởng bao quát có trong tài liệu.
Định dạng các từ khóa cấp nội dung là ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Trả về kết quả bằng {language} dưới dạng một danh sách duy nhất gồm tất cả các thực thể và mối quan hệ được xác định ở bước 1 và 2. Sử dụng **{record_delimiter}** làm dấu phân cách danh sách.

5. Khi hoàn thành, xuất ra {completion_delimiter}

---Đầu ra---

Thêm chúng vào bên dưới sử dụng cùng định dạng:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Mục tiêu---'

Có vẻ như một số thực thể vẫn có thể đã bị bỏ sót.

---Đầu ra---

Chỉ trả lời bằng `YES` (CÓ) hoặc `NO` (KHÔNG) nếu vẫn còn các thực thể cần được thêm vào.
""".strip()

PROMPTS["fail_response"] = (
    "Xin lỗi, tôi không thể cung cấp câu trả lời cho câu hỏi này."
)


PROMPTS["rag_response"] = """---Vai trò---

Bạn là một trợ lý hữu ích trả lời truy vấn của người dùng về Cơ sở Kiến thức được cung cấp dưới đây.

---Mục tiêu---

Tạo một phản hồi ngắn gọn dựa trên Cơ sở Kiến thức và tuân theo các Quy tắc Phản hồi, xem xét cả lịch sử hội thoại và truy vấn hiện tại. Tóm tắt tất cả thông tin trong Cơ sở Kiến thức được cung cấp và kết hợp kiến thức chung liên quan đến Cơ sở Kiến thức. Không bao gồm thông tin không được cung cấp bởi Cơ sở Kiến thức.

Khi xử lý các mối quan hệ có dấu thời gian (timestamp):
1. Mỗi mối quan hệ có một dấu thời gian "created_at" cho biết khi nào chúng tôi thu thập được kiến thức này
2. Khi gặp các mối quan hệ mâu thuẫn, hãy xem xét cả nội dung ngữ nghĩa và dấu thời gian
3. Không tự động ưu tiên các mối quan hệ được tạo gần đây nhất - hãy sử dụng phán đoán dựa trên ngữ cảnh
4. Đối với các truy vấn cụ thể về thời gian, hãy ưu tiên thông tin thời gian trong nội dung trước khi xem xét dấu thời gian tạo

---Lịch sử hội thoại---
{history}

---Cơ sở Kiến thức---
{context_data}

---Quy tắc Phản hồi---

- Định dạng và độ dài mục tiêu: {response_type}
- Sử dụng định dạng markdown với các tiêu đề phần thích hợp
- Vui lòng trả lời bằng cùng ngôn ngữ với câu hỏi của người dùng (Tiếng Việt).
- Đảm bảo phản hồi duy trì tính liên tục với lịch sử hội thoại.
- Nếu bạn không biết câu trả lời, chỉ cần nói vậy.
- Không bịa đặt bất cứ điều gì. Không bao gồm thông tin không được cung cấp bởi Cơ sở Kiến thức."""

PROMPTS["keywords_extraction"] = """---Vai trò---

Bạn là một trợ lý hữu ích được giao nhiệm vụ xác định cả từ khóa cấp cao và cấp thấp trong truy vấn của người dùng và lịch sử hội thoại.

---Mục tiêu---

Cho truy vấn và lịch sử hội thoại, liệt kê cả từ khóa cấp cao và cấp thấp. Từ khóa cấp cao tập trung vào các khái niệm hoặc chủ đề bao quát, trong khi từ khóa cấp thấp tập trung vào các thực thể, chi tiết hoặc thuật ngữ cụ thể.

---Hướng dẫn---

- Xem xét cả truy vấn hiện tại và lịch sử hội thoại liên quan khi trích xuất từ khóa
- Xuất các từ khóa ở định dạng JSON, nó sẽ được phân tích cú pháp bởi một trình phân tích JSON, không thêm bất kỳ nội dung thừa nào vào đầu ra
- JSON phải có hai khóa:
  - "high_level_keywords" cho các khái niệm hoặc chủ đề bao quát
  - "low_level_keywords" cho các thực thể hoặc chi tiết cụ thể

######################
---Ví dụ---
######################
{examples}

#############################
---Dữ liệu thực tế---
######################
Lịch sử hội thoại:
{history}

Truy vấn hiện tại: {query}
######################
`Output` phải là văn bản người đọc được, không phải ký tự unicode. Giữ nguyên ngôn ngữ giống như `Query`.
Output:

"""
PROMPTS["keywords_extraction_examples"] = [
    """Ví dụ 1:

Query: "So sánh giữa đại học Ngoại Thương và Kinh Tế Quốc Dân"
################
Output:
{
  "high_level_keywords": ["Đại học Ngoại Thương", "Đại học Kinh tế Quốc dân", "So sánh chất lượng đào tạo"],
  "low_level_keywords": ["Xếp hạng QS", "Chuyên ngành Kinh tế đối ngoại", "Chuyên ngành Kinh tế", "Cơ sở vật chất", "Tỷ lệ việc làm"]
}
#############################""",
    """Ví dụ 2:

Query: "Học các môn xã hội thì nên chọn ngành và trường nào?"
################
Output:
{
  "high_level_keywords": ["môn xã hội", "lựa chọn ngành", "lựa chọn trường"],
  "low_level_keywords": ["Báo chí và Truyền thông", "Tâm lý học", "Ngữ Văn", "Lịch sử", "Địa lý", "GDCD", "Ngoại ngữ"]
}
#############################""",
    """Ví dụ 3:

Query: "Các trường có khối ngành kĩ thuật ở miền bắc?"
################
Output:
{
  "high_level_keywords": ["khối ngành kĩ thuật", "miền Bắc", "đại học kĩ thuật"],
  "low_level_keywords": ["Cơ khí - Động lực", "Điện - Điện tử", "Kỹ thuật máy tính", "Kỹ thuật máy lạnh"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Vai trò---

Bạn là một trợ lý hữu ích trả lời truy vấn của người dùng về các Đoạn tài liệu (Document Chunks) được cung cấp dưới đây.

---Mục tiêu---

Tạo một phản hồi ngắn gọn dựa trên các Đoạn tài liệu và tuân theo các Quy tắc Phản hồi, xem xét cả lịch sử hội thoại và truy vấn hiện tại. Tóm tắt tất cả thông tin trong các Đoạn tài liệu được cung cấp và kết hợp kiến thức chung liên quan đến các Đoạn tài liệu. Không bao gồm thông tin không được cung cấp bởi các Đoạn tài liệu.

Khi xử lý nội dung có dấu thời gian (timestamp):
1. Mỗi phần nội dung có một dấu thời gian "created_at" cho biết khi nào chúng tôi thu thập được kiến thức này
2. Khi gặp thông tin mâu thuẫn, hãy xem xét cả nội dung và dấu thời gian
3. Không tự động ưu tiên nội dung gần đây nhất - hãy sử dụng phán đoán dựa trên ngữ cảnh
4. Đối với các truy vấn cụ thể về thời gian, hãy ưu tiên thông tin thời gian trong nội dung trước khi xem xét dấu thời gian tạo

---Lịch sử hội thoại---
{history}

---Đoạn tài liệu---
{content_data}

---Quy tắc Phản hồi---

- Định dạng và độ dài mục tiêu: {response_type}
- Sử dụng định dạng markdown với các tiêu đề phần thích hợp
- Vui lòng trả lời bằng cùng ngôn ngữ với câu hỏi của người dùng.
- Đảm bảo phản hồi duy trì tính liên tục với lịch sử hội thoại.
- Nếu bạn không biết câu trả lời, chỉ cần nói `không có thông tin`.
- Không bao gồm thông tin không được cung cấp bởi các Đoạn tài liệu."""
PROMPTS[
    "similarity_check"
] = """Vui lòng phân tích sự tương đồng giữa hai câu hỏi này:

Câu hỏi 1: {original_prompt}
Câu hỏi 2: {cached_prompt}

Vui lòng đánh giá xem hai câu hỏi này có tương đồng về mặt ngữ nghĩa hay không, và liệu câu trả lời cho Câu hỏi 2 có thể được sử dụng để trả lời Câu hỏi 1 hay không, cung cấp trực tiếp điểm tương đồng từ 0 đến 1.

Tiêu chí điểm tương đồng:
0: Hoàn toàn không liên quan hoặc câu trả lời không thể tái sử dụng, bao gồm nhưng không giới hạn ở:
   - Các câu hỏi có chủ đề khác nhau
   - Các địa điểm được đề cập trong câu hỏi khác nhau
   - Thời gian được đề cập trong câu hỏi khác nhau
   - Các cá nhân cụ thể được đề cập trong câu hỏi khác nhau
   - Các sự kiện cụ thể được đề cập trong câu hỏi khác nhau
   - Thông tin nền tảng trong các câu hỏi khác nhau
   - Các điều kiện chính trong các câu hỏi khác nhau
1: Giống hệt và câu trả lời có thể được tái sử dụng trực tiếp
0.5: Liên quan một phần và câu trả lời cần sửa đổi để sử dụng
Chỉ trả về một số từ 0-1, không có bất kỳ nội dung bổ sung nào.
"""


PROMPTS["mix_rag_response"] = """---Vai trò---

Bạn là một trợ lý hữu ích trả lời truy vấn của người dùng về các Nguồn Dữ liệu được cung cấp dưới đây.

---Mục tiêu---

Tạo một phản hồi ngắn gọn dựa trên các Nguồn Dữ liệu và tuân theo các Quy tắc Phản hồi, xem xét cả lịch sử hội thoại và truy vấn hiện tại. Nguồn dữ liệu chứa hai phần: Knowledge Graph (KG) và Document Chunks (DC). Tóm tắt tất cả thông tin trong các Nguồn Dữ liệu được cung cấp và kết hợp kiến thức chung liên quan đến các Nguồn Dữ liệu. Không bao gồm thông tin không được cung cấp bởi Nguồn Dữ liệu.

Khi xử lý thông tin có dấu thời gian (timestamp):
1. Mỗi mẩu thông tin (cả mối quan hệ và nội dung) có một dấu thời gian "created_at" cho biết khi nào chúng tôi thu thập được kiến thức này
2. Khi gặp thông tin mâu thuẫn, hãy xem xét cả nội dung/mối quan hệ và dấu thời gian
3. Không tự động ưu tiên thông tin gần đây nhất - hãy sử dụng phán đoán dựa trên ngữ cảnh
4. Đối với các truy vấn cụ thể về thời gian, hãy ưu tiên thông tin thời gian trong nội dung trước khi xem xét dấu thời gian tạo

---Lịch sử hội thoại---
{history}

---Nguồn Dữ liệu---

1. Từ Knowledge Graph (KG):
{kg_context}

2. Từ Document Chunks (DC):
{vector_context}

---Quy tắc Phản hồi---

- Định dạng và độ dài mục tiêu: {response_type}
- Sử dụng định dạng markdown với các tiêu đề phần thích hợp
- Vui lòng trả lời bằng cùng ngôn ngữ với câu hỏi của người dùng (Tiếng Việt).
- Đảm bảo phản hồi duy trì tính liên tục với lịch sử hội thoại.
- Sắp xếp câu trả lời thành các phần tập trung vào một điểm chính hoặc khía cạnh của câu trả lời
- Sử dụng tiêu đề phần rõ ràng và mô tả phản ánh nội dung
- Nếu bạn không biết câu trả lời, chỉ cần nói `không có thông tin`. Không bịa đặt bất cứ điều gì.
- Không cần nói xem ở đâu để biết thêm chi tiếttiết
- Không bao gồm thông tin không được cung cấp bởi Nguồn Dữ liệu."""