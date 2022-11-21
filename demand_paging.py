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
"""


def make_system_info(line: str):
    line = line.split(' ')

    system_info = {}
    system_info["pages"] = int(line[0])  # store N
    system_info["frames"] = int(line[1])  # stroe M
    system_info["window_size"] = int(line[2])  # store W
    system_info["len_page_reference_string"] = int(line[3])  # store K

    return system_info


input = open("input.txt", "r")  # open file

# get first line: N(pages) M(frames) W(window_size) K(len_page_reference_string)
first_line = input.readline()

# get second line: page reference string
page_reference_string = input.readline()

system_info = make_system_info(first_line)

input.close()
