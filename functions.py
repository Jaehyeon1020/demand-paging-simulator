"""
Demand Paging 구현에 필요한 functions:
1. MIN page replacement 기법 구현 함수
2. LRU page replacement 기법 구현 함수
3. LFU page replacement 기법 구현 함수
4. WS Memory Management 기법 구현 함수
5. input.txt 분석 함수 (page reference string은 input.txt file로 주어짐)
"""

from result import *

# input.txt의 첫 번째 줄에 입력된 정보를 dictionary 형태로 저장
def get_system_info(line: str):
    line = line.split(' ')

    system_info = {}
    system_info["pages"] = int(line[0])  # store N
    system_info["frames"] = int(line[1])  # stroe M
    system_info["window_size"] = int(line[2])  # store W
    system_info["len_page_reference_string"] = int(line[3])  # store K

    return system_info

# frame에 page를 할당: 할당된 개수보다 많은 page를 memory에 올리려고 시도할 시 첫 번째 반환값으로 false 반환, 그 외 memory 저장 후 true 반환
# 교체가 아닌 삽입만이 필요한 상황인지 여부를 두 번째 반환값으로 반환
# WS algorithm에서는 사용 X
def append_to_frame(allocated_page_frames: list, page: str, limit: int):
    # 이미 사용하고자 하는 페이지가 할당되어있는 경우
    if page in allocated_page_frames:
        return True, False
    # 이미 할당 가능한 최대 개수의 page frame이 할당되어있는 경우
    elif len(allocated_page_frames) == limit:
        return False, False
    # 새롭게 할당 가능한 경우 -> 교체가 아닌 삽입만 필요
    else:
        allocated_page_frames.append(page)
        return True, True

# 할당되어있는 페이지들 중 time으로부터 가장 오랫동안 참조되지 않을 페이지의 index를 반환
def get_min_index(allocated_page_frames: list, time: int, references: list):
    distance = 0 # 앞으로 얼만큼의 시간동안 참조되지 않는지를 count
    page_distances = [-1 for i in range(len(allocated_page_frames))]

    for i in range(time, len(references)):
        for j in range(0, len(allocated_page_frames)):
            if (references[i] == allocated_page_frames[j]) and (page_distances[j] == -1):
                page_distances[j] = distance
        distance += 1

    change_need_idx = page_distances.index(max(page_distances))

    # distance saving list에 -1이 남아있다: 현재 시점부터는 참조되지 않음 -> 교체
    for idx in range(0, len(page_distances)):
        if page_distances[idx] == -1:
            change_need_idx = idx
            break
    
    return change_need_idx


# MIN 기법을 사용했을 때의 동작 구현
def get_min_result(system_info: dict, references: list):
    result = Result("MIN") # saving result: type MIN

    frames = system_info["frames"]  # 할당 page frame 개수
    reference_len = system_info["len_page_reference_string"] # page reference string 길이
    allocated_page_frames = []  # 현재 할당된 page frame: 정해진 개수 넘어서 저장 불가능

    # reference string의 길이와 같은 횟수를 실행
    # 각 time마다 Result 객체를 업데이트 해주어야 함
    for time in range(0, reference_len):
        is_page_fault = False # 각 time마다 page fault의 여부 저장 (기본 false)

        appending_result = append_to_frame(allocated_page_frames, references[time], frames)
        # frame에 올리는게 실패하는 경우: page fault -> page replacement needed
        if appending_result[0] is False:
            del allocated_page_frames[get_min_index(allocated_page_frames, time, references)] # 가장 오래 참조되지 않을 페이지 지우기
            append_to_frame(allocated_page_frames, references[time], frames) # 필요한 page를 frame에 할당
            result.increase_total_page_fault() # 총 page fault 횟수 +
            is_page_fault = True
        
        # 교체가 아닌 삽입만이 필요한 상황
        if appending_result[1] is True:
            result.increase_total_page_fault()
            is_page_fault = True
        
        result.update(references[time], allocated_page_frames, is_page_fault)
    
    return result

# 할당되어있는 페이지 리스트에서 가장 오래전에 참조되었던 페이지의 index를 반환
def get_lru_index(allocated_page_frames: list, last_references_time: list):
    last_references_time_allocated = [] # 현재 할당되어있는 page에 대한 마지막 참조 시점 list 생성

    for page in allocated_page_frames:
        last_references_time_allocated.append(last_references_time[int(page)])
    
    referenced_minimum = min(last_references_time_allocated)

    return last_references_time_allocated.index(referenced_minimum) # allocated_page_frames에서 가장 적게 참조된 page가 있는 index 반환

# LRU(Least Recently Used) 기법을 사용했을 때의 동작 구현
def get_lru_result(system_info: dict, references: list):
    result = Result("LRU")

    pages = system_info["pages"] # process가 갖는 page 개수
    frames = system_info["frames"] # 최대 할당 가능 page frame 개수
    reference_len = system_info["len_page_reference_string"] # page reference string 길이
    allocated_page_frames = [] # 현재 할당된 page frame
    last_references_time = [-1 for i in range(pages)] # 모든 page의 마지막 참조 시점 저장

    for time in range(0, reference_len):
        is_page_fault = False # time마다 page fault 여부 저장
        last_references_time[int(references[time])] = time # 현재 참조하는 page의 참조 시점 저장

        appending_result = append_to_frame(allocated_page_frames, references[time], frames)
        if appending_result[0] is False:
            del allocated_page_frames[get_lru_index(allocated_page_frames, last_references_time)]
            append_to_frame(allocated_page_frames, references[time], frames)
            is_page_fault = True
            result.increase_total_page_fault()

        if appending_result[1] is True:
            is_page_fault = True
            result.increase_total_page_fault()

        result.update(references[time], allocated_page_frames, is_page_fault)
    
    return result

# 할당되어있는 페이지 리스트에서 가장 적게 참조된 페이지의 index를 반환
def get_lfu_index(allocated_page_frames: list, reference_frequents: list):
    reference_frequents_allocated = [] # 현재 할당되어있는 page에 대한 참조 횟수 list 생성

    for page in allocated_page_frames:
        reference_frequents_allocated.append(reference_frequents[int(page)])

    referenced_minimum = min(reference_frequents_allocated)

    return reference_frequents_allocated.index(referenced_minimum)
    
# LFU(Least Frequently Used) 기법을 사용했을 때의 동작 구현
def get_lfu_result(system_info: dict, references: list):
    result = Result("LFU")

    pages = system_info["pages"] # process가 갖는 page 개수
    frames = system_info["frames"] # 최대 할당 가능 page frame 개수
    reference_len = system_info["len_page_reference_string"] # page reference string 길이
    allocated_page_frames = [] # 현재 할당된 page frame
    reference_frequents = [0 for i in range(pages)] # 모든 page의 참조 횟수 저장

    for time in range(0, reference_len):
        is_page_fault = False
        reference_frequents[int(references[time])] += 1 # 현재 time에 참조하는 page의 참조 횟수 +1

        appending_result = append_to_frame(allocated_page_frames, references[time], frames)
        if appending_result[0] is False:
            del allocated_page_frames[get_lfu_index(allocated_page_frames, reference_frequents)]
            append_to_frame(allocated_page_frames, references[time], frames)
            is_page_fault = True
            result.increase_total_page_fault()
        
        if appending_result[1] is True:
            is_page_fault = True
            result.increase_total_page_fault()

        result.update(references[time], allocated_page_frames, is_page_fault)
    
    return result

# WS(Working Set Memory Management) 기법을 사용했을 때의 동작 구현
def get_ws_result(system_info: dict, references: list):
    result = Result("WS")

    window_size = system_info["window_size"] # window 크기
    reference_len = system_info["len_page_reference_string"] # page reference string 길이
    allocated_page_frames = [] # 현재 할당된 page frame

    for time in range(0, reference_len):
        is_page_fault = False # page fault flag
        current_window = references[time - window_size : time + 1] # 현재 reference string에서 frame에 올라갈 수 있는 부분(Working Set)
        deleted_page = reset_ws(current_window, allocated_page_frames, window_size, time) # reset working set
        is_new_allocate = ws_append_to_frame(allocated_page_frames,references[time]) # 현재 시점에 필요한 page를 frame에 할당

        # 새로운 frame이 할당된 경우: page fault 발생 기록 / 총 page fault +1
        if is_new_allocate:
            is_page_fault = True
            result.increase_total_page_fault()
        
        result.ws_update(references[time], allocated_page_frames, is_page_fault, deleted_page)

    return result

# WS algorithm에서 frame에 page를 할당 시도
# frame에 할당되어있지 않던 page를 새롭게 추가한 경우 True, 원래 frame에 해당 페이지가 존재했던 경우 False 반환
def ws_append_to_frame(allocated_page_frames: list, page: str):
    if page in allocated_page_frames:
        return False
    else:
        allocated_page_frames.append(page)
        return True

# 현재 Working Set에서 할당가능하지 않은 page를 frame에서 제거하고 제거된 페이지 반환
# time이 working set size만큼 지나지 않았다면 별도로 페이지 삭제하지 않음
def reset_ws(current_window: str, allocated_page_frames: list, window_size: int, time: int):
    is_deleted_page = False # 삭제된 페이지 있는지 flag
    
    if time > window_size:
        for page in allocated_page_frames:
            # 현재 Working Set에 해당 페이지가 없다면 삭제
            if page not in current_window:
                is_deleted_page = True
                deleted_page = allocated_page_frames[allocated_page_frames.index(page)]
                del allocated_page_frames[allocated_page_frames.index(page)]
    
    if is_deleted_page:
        return deleted_page
    else:
        return None
