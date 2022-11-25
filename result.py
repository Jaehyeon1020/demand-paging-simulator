"""
Class that stores and handles the result of demand paging
"""

class Result:
    def __init__(self, type: str):
        self.type = type
        self.total_page_faults = 0
        self.memory_info = [] # 각 time마다의 reference string, memory state, page fault 여부를 저장하는 리스트를 저장
        self.type = type # 어떤 type의 replacing 기법을 사용하였는지 저장
        self.deleted = None # Working Set에서 벗어나 제거된 페이지 저장 (WS 기법에서만 사용)
    
    # 각 time마다 호출할 함수: result 객체 정보 업데이트
    def update_result(self, ref_string: str, memory_state: list, is_page_fault: bool):
        self.memory_info.append([ref_string, memory_state.copy(), is_page_fault])

    # (WS algorithm ONLY) 각 time마다 호출할 함수: result 객체 정보 업데이트
    def ws_update_result(self, ref_string: str, memory_state: list, is_page_fault: bool, deleted: str):
        self.memory_info.append([ref_string, memory_state.copy(), is_page_fault, deleted])

    # page fault가 발생할 때마다 호출할 함수
    def increase_total_page_fault(self):
        self.total_page_faults += 1

    """
    # print result(s)
    def print_result(self):
        time = 1

        print("\n=============== %s ALGORITHM RESULT ==============="%self.type)
        for result in self.memory_info:
            print("<TIME %d>"%time)
            print("Reference string: %s"%result[0]) # print ref string
            print("Memory state(Pages in memory): ", end='')
            print(result[1]) # print memory state
            print("Page fault at time %d : "%time, end='')

            # print whether page fault is at this time
            if result[2]:
                print("YES")
            else:
                print("NO")

            print("----------------------------------------------------")

            time += 1
        
        print("Total page fault(s): %d"%self.total_page_faults)
        print("====================================================")
    """

    # print result(s)
    def print_result(self):
        time = 1
        print("\n========================================================")
        print("================= %s ALGORITHM RESULT ================="%self.type)
        print("========================================================")
        print("{:<8} {:<20} {:<15} {:<10}".format("Time", "Reference String", "Memory State", "Page Fault"))
        for result in self.memory_info:
            is_page_fault = "F" if result[2] else ""
            print("{:<8} {:<20} {:<15} {:<10}".format(time, result[0], ",".join(result[1]), is_page_fault))

            time += 1
        
        print("\nTotal page fault(s): %d"%self.total_page_faults)
        print("========================================================\n")

    # (WS Algorithm ONLY) print result(s)
    def ws_print_result(self):
        time = 1
        print("\n=======================================================================================================")
        print("========================================= %s ALGORITHM RESULT ========================================="%self.type)
        print("=======================================================================================================")
        print("{:<8} {:<20} {:<15} {:<14} {:<19} {:<20}".format("Time", "Reference String", "Memory State", "Page Fault", "Deleted From WS", "# of Frames Allocated"))
        for result in self.memory_info:
            is_page_fault = "F" if result[2] else ""
            is_no_deleted = "" if result[3] is None else result[3]
            print("{:<8} {:<20} {:<15} {:<14} {:<19} {:<20}".format(time, result[0], ",".join(result[1]), is_page_fault, is_no_deleted, len(result[1])))

            time += 1
        
        print("\nTotal page fault(s): %d"%self.total_page_faults)
        print("=======================================================================================================\n")

    """
    # (WS Algorithm ONLY) print result(s)
    def ws_print_result(self):
        time = 1

        print("\n======= %s MEMORY MANAGEMENT ALGORITHM RESULT ======"%self.type)
        for result in self.memory_info:
            print("<TIME %d>"%time)
            print("Reference string: %s"%result[0]) # print ref string
            print("Memory state(Pages in memory): ", end='')
            print(result[1]) # print memory state
            print("Page fault at time %d : "%time, end='')

            # print whether page fault is at this time
            if result[2]:
                print("YES")
            else:
                print("NO")

            print("Deleted from working set: %s"%result[3])
            print("Number of frames allocated: %d"%len(result[1]))

            print("----------------------------------------------------")

            time += 1
        
        print("Total page fault(s): %d"%self.total_page_faults)
        print("====================================================")
    """
    