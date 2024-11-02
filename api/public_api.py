from DataManager import *


def get_file_md5(file_path):
    """获取文件的 MD5 值。

    参数:
    file_path (str): 文件的路径

    返回:
    str: 文件的 MD5 值
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            # 分批次读取文件数据到缓冲区中（如果文件很大）
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        return "文件未找到，请检查路径是否正确！"
    except Exception as e:
        return f"发生错误: {e}"


def determine_file_type(file_path):
    """
    文件类型	        枚举值
    原图	            1
    高清图	        2,会创建thumb
    缩略图	        3,会创建thumb
    视频	            4,会创建thumb
    文件	            5
    大文件(25M及以上)	7
    语音	            15
    """
    if not os.path.exists(file_path):
        return "文件不存在"
    try:
        # 获取文件大小
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # 转换为MB
        # 获取文件 MIME 类型
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            return 5

        # 判断大文件
        if file_size_mb >= 25:
            return 7

        if mime_type.startswith("image"):
            # 判断图片类型
            with Image.open(file_path) as img:
                width, height = img.size

                # 判断缩略图、高清图和原图的条件可以根据具体要求调整
                if width * height <= 320 * 240:
                    return 3
                elif width * height <= 1920 * 1080:
                    return 2
                else:
                    return 1

        elif mime_type.startswith("video"):
            return 4

        elif mime_type.startswith("audio"):
            return 15

        else:
            return 5

    except Exception as e:
        print(f"发生错误: {e}")
        return 5
