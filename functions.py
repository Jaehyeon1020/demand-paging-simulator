"""
Demand Paging 구현에 필요한 functions:
1. MIN page replacement 기법 구현 함수
2. LRU page replacement 기법 구현 함수
3. LFU page replacement 기법 구현 함수
4. WS Memory Management 기법 구현 함수
5. input.txt 분석 함수 (page reference string은 input.txt file로 주어짐)
6. 결과 출력 함수
"""

# input.txt의 첫 번째 줄에 입력된 정보를 dictionary 형태로 저장
def get_system_info(line: str):
    line = line.split(' ')

    system_info = {}
    system_info["pages"] = int(line[0])  # store N
    system_info["frames"] = int(line[1])  # stroe M
    system_info["window_size"] = int(line[2])  # store W
    system_info["len_page_reference_string"] = int(line[3])  # store K

    return system_info

# frame에 page를 할당: 할당된 개수보다 많은 page를 memory에 올리려고 시도할 시 false 반환, 그 외 memory 저장 후 true 반환
def add_to_frame(allocated_page_frames: list, page: int, limit: int):
    if len(allocated_page_frames) == limit:
        return False
    else:
        allocated_page_frames.append(page)
        return True

# 할당되어있는 페이지들 중 가장 오랫동안 참조되지 않을 페이지의 index를 반환
def min_check(allocated_page_frames: list, time: int, references: str):
    distance = 0 # 앞으로 얼만큼의 시간동안 참조되지 않는지를 count
    page_distances = [-1 for i in range(len(allocated_page_frames))]

    for i in range(time, len(references)):
        for j in range(0, len(allocated_page_frames)):
            if (references[i] == allocated_page_frames[j]) and (page_distances[j] == -1):
                page_distances[j] = distance
        distance += 1
    
    change_need_idx = page_distances.index(max(page_distances))
    
    return change_need_idx


# MIN 기법을 사용했을 때의 세부사항 출력
def min(system_info: dict, references: str):
    pages_num = system_info["pages"]  # process가 갖는 page 개수
    frames_num = system_info["frames"]  # 할당 page frame 개수
    # page reference string 길이
    reference_len = system_info["len_page_reference_string"]
    allocated_page_frames = []  # 현재 할당된 page frame: 정해진 개수 넘어서 저장 불가능
    replace = None # 교체될 페이지 저장

    # reference string의 길이와 같은 횟수를 실행
    for time in range(0, reference_len):
        # frame에 올리는게 실패하는 경우: page replacement 필요
        if ~(add_to_frame(allocated_page_frames, references[time], frames_num)):
            pass
