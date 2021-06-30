from collections.abc import Callable
from DB_connection.mapping_dict import get_breed_dict

def text_contain(row, container):
    """
    row를 텍스트로 가정하고 간단하게 Set에 존재하는지 확인

    Parameters:
        row (string): 검사하고자 하는 텍스트
        container (set): Set에 존재하는지 검사하기 위한 Set

    Returns:
        bool: Set에 존재하는지 검사 여부
    """
    return row in container

def generate_mapping_function(mapping_dict, contain=text_contain):
    """
    Mapping Dictionary를 기반으로 검사를 한 뒤, 매핑된 정보를 리턴하는 함수를 반환

    Parameters:
        mapping_dict (dict[string, set[string]]): 입력에 대해서 키에 해당하는
            데이터가 맞는지 확인하기 위한 Dictionary
        contain (function): 입력을 Dictionary와 비교하기 위한 비교 함수. 입력이
            어떤 형태로 들어올지 모르기 때문에 함수로 추상화한다.
    
    Returns:
        function (function(row) -> bool): Mapping Dictionary에 따라 검사를 하여
            올바른 값에 매핑해주는 함수를 반환한다.
    """
    def mapping_function(row):
        for key, set in mapping_dict.items():
            if contain(row, set):
                return key
        return "Unknown"
    return mapping_function

if __name__ == "__main__":
    mapping_dict = get_breed_dict()
    # mapping_func = generate_mapping_function(mapping_dict)
    # input_list = ["말티즈", "Maltese", "몰티즈", "믹스", "Mix", "포메라니안", "비숀프리제"]
    # mapped_list = list(map(mapping_func, input_list))
    # print(mapped_list)