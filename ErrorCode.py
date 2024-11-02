# error_codes.py

ERROR_CODES = {
    10000: "API调用成功",
    10001: "无效的json串",
    10002: "缺少必要的参数或其他",
    10003: "不支持的接口编号",
    10004: "许可已过期",
    0: "无明显异常",
    -1: "请查看desc字段"
    # Note: The '<0' condition implies that any negative error less than 0 should map to this message.
    # In a real-world scenario, ensure each specific negative code that might arise has its entry if needed.
}


def get_error_description(code):
    """
    Returns the error description for a given error code.
    If the code is less than 0 and not specifically listed, it defaults to a general message.
    """
    if code in ERROR_CODES:
        return ERROR_CODES[code]
    elif code < 0:
        return ERROR_CODES[-1]
    else:
        return "Unknown error code"
