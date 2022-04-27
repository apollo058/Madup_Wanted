"""
    작성자: 하정현
    Summary: 테스팅 할 때 사용되는 테스트 관련 툴
"""

def print_err_msg(idx, answer, output) -> str:
    """ 오류 메세지 호출 """
    return f"""
        Topic: {idx},
        Answer: {answer},
        Wrong Output: {output},
    """


def test_loader(test_root: str):
    """
        테스트 돌릴 때 사용하는 데코래이터 함수
        TODO: 구현을 위한 테스팅 추가 설계 필요
    """
    def functional(func: function):
        def wrapper(*args, **kwargs):
            func(*args)
        return wrapper
    return functional