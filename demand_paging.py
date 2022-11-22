"""
2022-2학기 운영체제 Project 3 <Virtual Memory Management 기법 구현>
2019314891 김재현

구현 기능:
1. MIN page replacement 기법
2. LRU page replacement 기법
3. LFU page replacement 기법
4. WS Memory Management 기법
5. input.txt 분석 함수 (page reference string은 input.txt file로 주어짐)
6. 결과 출력 함수

출력 내용(page replacement 기법 별로 출력):
- 시간별 ref.string, memory state, page fault 여부
- 총 page fault 횟수
"""


from functions import *
from result import *


input = open("input.txt", "r")  # open file

first_line = input.readline() # get first line: N(pages) M(frames) W(window_size) K(len_page_reference_string)
page_reference_string = input.readline() # get second line: page reference string

system_info = get_system_info(first_line) # get system info dictionary

min_result = get_min_result(system_info, page_reference_string) # execute by MIN algorithm and get Result instance
lru_result = get_lru_result(system_info, page_reference_string) # execute by LRU algorithm and get Result instance
lfu_result = get_lfu_result(system_info, page_reference_string) # execute by LFU algorithm and get Result instance
ws_result = None # execute by WS Memory Management algorithm and get Result instance

min_result.print_result()
lru_result.print_result()
lfu_result.print_result()
# ws_result.print_result()

input.close()
