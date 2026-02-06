# process_context.py
# 这个模块将为每个进程提供一个独立的上下文存储。

from multiprocessing import current_process

# 我们将把特定于进程的上下文存储在这里。
# 因为每个进程都有自己独立的内存空间，所以每个进程访问这个变量时，
# 访问的都是它自己的那一份拷贝，彼此之间不会冲突。
_context_storage = {}

def set_context(key, value):
    """在当前进程的上下文中设置一个值。"""
    _context_storage[key] = value
    # print(f"[{current_process().name}] 设置上下文: {key} = {value}") # 用于调试

def get_context(key, default=None):
    """从当前进程的上下文中获取一个值。"""
    value = _context_storage.get(key, default)
    # print(f"[{current_process().name}] 获取上下文: {key} -> {value}") # 用于调试
    if value is None and default is None:
        raise NameError(f"在当前进程上下文中未找到 '{key}'。请确保在进程入口点已设置。")
    return value

# 为了方便，我们可以为 result_dir 创建专门的 getter
def get_current_result_dir():
    """获取当前进程专属的 result_dir。"""
    return get_context('current_result_dir')

def set_current_result_dir(example_result_dir):
    set_context("current_result_dir", example_result_dir)