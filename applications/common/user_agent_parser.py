"""
User-Agent解析工具
用于从User-Agent字符串中提取浏览器和操作系统信息
"""
import re


def parse_browser(user_agent):
    """
    解析浏览器类型
    """
    if not user_agent:
        return 'Unknown'
    
    ua = user_agent.lower()
    
    # Edge
    if 'edg' in ua and 'edge' not in ua:
        return 'Edge'
    # Chrome
    elif 'chrome' in ua and 'edg' not in ua:
        return 'Chrome'
    # Safari
    elif 'safari' in ua and 'chrome' not in ua:
        return 'Safari'
    # Firefox
    elif 'firefox' in ua:
        return 'Firefox'
    # Opera
    elif 'opera' in ua or 'opr' in ua:
        return 'Opera'
    # IE
    elif 'msie' in ua or 'trident' in ua:
        return 'IE'
    # 微信浏览器
    elif 'micromessenger' in ua:
        return 'WeChat'
    # 移动端浏览器
    elif 'mobile' in ua:
        if 'android' in ua:
            return 'Android Browser'
        elif 'iphone' in ua or 'ipad' in ua:
            return 'Safari Mobile'
    else:
        return 'Unknown'


def parse_os(user_agent):
    """
    解析操作系统
    """
    if not user_agent:
        return 'Unknown'
    
    ua = user_agent.lower()
    
    # Windows
    if 'windows' in ua:
        if 'windows nt 10' in ua or 'windows nt 6.3' in ua or 'windows nt 6.4' in ua:
            return 'Windows 10/11'
        elif 'windows nt 6.2' in ua:
            return 'Windows 8'
        elif 'windows nt 6.1' in ua:
            return 'Windows 7'
        elif 'windows nt 6.0' in ua:
            return 'Windows Vista'
        elif 'windows nt 5.1' in ua:
            return 'Windows XP'
        else:
            return 'Windows'
    # macOS
    elif 'mac os x' in ua or 'macintosh' in ua:
        # 提取版本号
        match = re.search(r'mac os x (\d+)[._](\d+)', ua)
        if match:
            return f'macOS {match.group(1)}.{match.group(2)}'
        return 'macOS'
    # iOS
    elif 'iphone' in ua or 'ipad' in ua or 'ipod' in ua:
        match = re.search(r'os (\d+)[._](\d+)', ua)
        if match:
            return f'iOS {match.group(1)}.{match.group(2)}'
        return 'iOS'
    # Android
    elif 'android' in ua:
        match = re.search(r'android (\d+\.\d+)', ua)
        if match:
            return f'Android {match.group(1)}'
        return 'Android'
    # Linux
    elif 'linux' in ua:
        if 'ubuntu' in ua:
            return 'Ubuntu'
        elif 'debian' in ua:
            return 'Debian'
        elif 'fedora' in ua:
            return 'Fedora'
        else:
            return 'Linux'
    # 其他
    else:
        return 'Unknown'


def parse_user_agent(user_agent):
    """
    解析User-Agent，返回浏览器和操作系统信息
    """
    return {
        'browser': parse_browser(user_agent),
        'os': parse_os(user_agent)
    }

