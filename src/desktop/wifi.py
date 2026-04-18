import pywifi
from pywifi import const
import time
import urllib.request
import sys
import json

# 判断网络连接状态
def is_network_available(timeout: int = 3) -> bool:
    """
    检查网络连接状态
    timeout: 超时时间（秒）
    return: 是否有网络连接
    """
    try:
        urllib.request.urlopen('http://www.baidu.com', timeout=timeout)
        return True
    except:
        return False

# 定义允许的加密类型（普通密码登录）
ALLOWED_AKM = [const.AKM_TYPE_WPA2PSK, const.AKM_TYPE_WPAPSK]

# 获取无线网接口对象
def get_wifi_interface() -> object | None:
    """
    获取无线网接口对象 | None
    return: 无线网接口对象
    """
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()  
        return iface[0] if iface else None
    except Exception as e:
        print(f"获取无线网接口失败: {e}")
        return None

# 处理扫描编码问题
def decode_ssid(ssid: str) -> str:
    if not ssid:
        return ""
    try:
        return ssid.encode('raw_unicode_escape').decode('utf-8')
    except UnicodeDecodeError:
        return ssid  # 解码失败

# 扫描周围的Wi-Fi网络 
def scan_available_wifi(verbose: bool = True, timeout: int = 8) -> dict:
    """
    iface: 无线网接口对象
    return: 可连接的wifi列表，格式为{SSID: 信号强度}
    """
    # 获取无线网接口对象
    iface = get_wifi_interface()
    if iface is None:
        if verbose:
            print("未找到无线网卡")
        return {}
    try:
        if verbose:
            print("正在扫描周围的Wi-Fi网络...")

        # 扫描周围网络
        iface.scan()

        # 动态检查扫描状态
        start = time.time()

        last_count = 0
        stable_rounds = 0
        wifis = []
        while time.time() - start < timeout:
            current_results = iface.scan_results()
            current_count = len(current_results)
            if current_count == last_count and current_count > 0:
                stable_rounds += 1
                if stable_rounds >= 4:   # 连续四次数量相同，认为扫描稳定
                    wifis = current_results
                    break
            else:
                stable_rounds = 0
                last_count = current_count
            time.sleep(0.5)
        else:
            # 超时，使用最后一次结果
            wifis = iface.scan_results()
            if verbose:
                print(f"扫描超时（{timeout}秒），使用已获取的结果")


        wifis.sort(key=lambda x: x.signal, reverse=True)  # 按信号强度排序

        # wifi可连列表
        wifi_dict = {}


        for net in wifis:
            # 过滤隐藏的SSID
            if not net.ssid:
                continue
            
            # 处理SSID编码问题
            display_ssid = decode_ssid(net.ssid)

            # 过滤不支持的加密类型
            if not any(akm in ALLOWED_AKM for akm in net.akm):
                continue

            # 过滤重复的SSID
            if display_ssid in wifi_dict:
                continue
            wifi_dict[display_ssid] = net.signal

        if verbose:
            print(f"扫描完成，发现 {len(wifi_dict)} 个网络")

        return wifi_dict
    except Exception as e:
        if verbose:
            print(f"扫描过程发生错误: {e}")
        return {}

# 连接wifi
def connect_wifi(ssid: str, password: str, verbose: bool = True, timeout: int = 10) -> bool:
    """
    ssid: Wi-Fi名称
    password: Wi-Fi密码
    timeout: 连接超时时间（秒）
    return: 是否连接成功
    """

    iface = get_wifi_interface()
    if not iface:
        if verbose:
            print("未找到无线网卡，无法连接Wi-Fi")
        return False

    try:
        # 断开当前连接
        if iface.status() == const.IFACE_CONNECTED:
            iface.disconnect()
            time.sleep(1)

        # 创建连接配置
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        # 删除旧配置
        for pf in iface.network_profiles():
            if pf.ssid == ssid:
                iface.remove_network_profile(pf)
        tmp_profile = iface.add_network_profile(profile)

        # 连接Wi-Fi
        iface.connect(tmp_profile)

        # 等待连接结果
        start = time.time()
        disconnect_count = 0
        while time.time() - start < timeout:
            if iface.status() == const.IFACE_CONNECTED:
                time.sleep(1)
                if iface.status() == const.IFACE_CONNECTED:
                    if verbose:
                        print(f"成功连接到Wi-Fi '{ssid}'")
                    return True
            if iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
                disconnect_count += 1
                if disconnect_count >= 3:
                    if verbose:
                        print(f"连接Wi-Fi '{ssid}' 失败")
                    return False
            time.sleep(0.5)
        if verbose:
            print(f"连接Wi-Fi '{ssid}' 超时")
        return False
    except Exception as e:
        if verbose:
            print(f"连接Wi-Fi发生错误: {e}")
        return False
   

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"可连接的Wi-Fi网络: {scan_available_wifi()}")
        connect_wifi("caixiang", "00000000")
    else:
        operation = sys.argv[1]
        if operation == "scan":
            result = scan_available_wifi(verbose=False)
            print(json.dumps({"success": True, "networks": result}, ensure_ascii=False))
        elif operation == "status":
            result = is_network_available()
            print(json.dumps({"success": True, "connected": result}, ensure_ascii=False))
        elif operation == "connect" and len(sys.argv) >= 4:
            ssid = sys.argv[2]
            password = sys.argv[3]
            success = connect_wifi(ssid, password, verbose=False)
            print(json.dumps({"success": success}, ensure_ascii=False))
        else:
            print(json.dumps({"success": False, "error": "Unknown operation"}, ensure_ascii=False))