"""
Class that stores and handles the result of demand paging
"""

class Result:
    def __init__(self):
        self.total_page_faults = 0
        self.memory_info = [] # 각 time마다의 reference string, memory state, page fault 여부를 저장하는 리스트를 저장
    
    def update_result(self, ref_string: str, memory_state: list, is_page_fault: bool):
        self.memory_info.append([ref_string, memory_state, is_page_fault])

    def incread_total_page_fault(self):
        self.total_page_faults += 1
