"""
    작성자: 하정현
    Summary: 테스팅 할 때 사용되는 테스트 관련 툴
"""

def print_err_msg(topic, answer, output) -> str:
    """ 오류 메세지 호출 """
    return f"""
        Topic: {topic},
        Answer: {answer},
        Wrong Output: {output},
    """