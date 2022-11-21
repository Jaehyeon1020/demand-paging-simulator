"""
Demand Paging 구현에 필요한 함수:
1. MIN page replacement 기법 구현 함수
2. LRU page replacement 기법 구현 함수
3. LFU page replacement 기법 구현 함수
4. WS Memory Management 기법 구현 함수
5. input.txt 분석 함수 (page reference string은 input.txt file로 주어짐)
6. 결과 출력 함수
"""

# input.txt의 첫 번째 줄에 입력된 정보를 dictionary 형태로 저장
def make_system_info(line: str):
    line = line.split(' ')

    system_info = {}
    system_info["pages"] = int(line[0])  # store N
    system_info["frames"] = int(line[1])  # stroe M
    system_info["window_size"] = int(line[2])  # store W
    system_info["len_page_reference_string"] = int(line[3])  # store K

    return system_info