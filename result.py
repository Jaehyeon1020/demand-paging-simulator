"""
Class that stores and handles the result of demand paging
"""

class Result:
    def __init__(self, type: str):
        self.type = type
        self.total_page_faults = 0
        self.memory_info = [] # 각 time마다의 reference string, memory state, page fault 여부를 저장하는 리스트를 저장
        self.type = type # 어떤 type의 replacing 기법을 사용하였는지 저장
    
    # 각 time마다 호출할 함수
    def update_result(self, ref_string: str, memory_state: list, is_page_fault: bool):
        self.memory_info.append([ref_string, memory_state.copy(), is_page_fault])

    # page fault가 발생할 때마다 호출할 함수
    def increase_total_page_fault(self):
        self.total_page_faults += 1

    def print_result(self):
        time = 1

        print("\n=============== %s ALGORITHM RESULT ==============="%self.type)
        for result in self.memory_info:
            print("<TIME %d>"%time)
            print("Reference string: %s"%result[0]) # print ref string
            print("Memory state: ", end='')
            print(result[1]) # print memory state
            print("Page fault at time %d : "%time, end='')

            # print whether page fault is at this time
            if result[2]:
                print("YES")
            else:
                print("NO")

            print("----------------------------------------------------")

            time += 1
        
        print("Total Page Fault(s): %d"%self.total_page_faults)
        print("====================================================")
