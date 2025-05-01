import time
import threading
from datetime import datetime
import sys

def extract_reminder_details(user_input):
    """
    从用户输入中提取提醒时间和内容。
    示例输入：提醒我1分钟之后喝水
    返回：{"delay": 60, "message": "喝水"}
    """
    try:
        triggers = ["提醒我", "定时"]
        for trigger in triggers:
            if trigger in user_input:
                # 提取时间部分
                time_details = user_input.split(trigger)[1].strip()
                
                # 定义支持的时间单位
                time_units = {
                    "分钟之后": 60,
                    "小时之后": 3600,
                    "分钟后": 60,
                    "小时后": 3600,
                }
                
                for unit, multiplier in time_units.items():
                    if unit in time_details:
                        time_value = int(time_details.split(unit)[0].strip())
                        delay_seconds = time_value * multiplier
                        message = time_details.split(unit)[1].strip()
                        return {"delay": delay_seconds, "message": message}
        return None
    except (ValueError, IndexError) as error:
        print(f"无法解析提醒内容，可能是输入格式不正确：{error}")
        return None

def send_reminder_after_delay(delay, message):
    """
    等待指定的时间后发送提醒。
    :param delay: 延迟时间（秒）
    :param message: 提醒的核心内容
    """
    time.sleep(delay)
    
    # 生成真人化的提醒内容
    prompt = (
        "提醒时间到了！\n"
        "你好呀，我是你的贴心小助手，刚刚提醒钟响了！\n"
        f"你让我提醒的内容是：{message}\n"
        "希望这条提醒对你有帮助！加油完成任务吧！💪"
    )
    
    # 记录日志
    log_entry = (
        f"提醒触发时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{prompt}\n"
    )
    with open("reminder_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
    
    # 在控制台打印提醒内容
    print(prompt)

def start_reminder_task(user_input):
    """
    根据用户输入启动一个提醒任务。
    :param user_input: 用户输入的文本，例如“提醒我1分钟之后喝水”
    """
    reminder_details = extract_reminder_details(user_input)
    if reminder_details:
        delay = reminder_details["delay"]
        message = reminder_details["message"]
        print(f"提醒已设置：将在 {delay} 秒后提醒你 - 内容是：{message}")
        
        # 启动新线程来处理提醒
        reminder_thread = threading.Thread(target=send_reminder_after_delay, args=(delay, message))
        reminder_thread.daemon = True  # 设置为守护线程，确保程序退出时线程随之结束
        reminder_thread.start()
    else:
        print("未识别有效的提醒内容，请检查输入格式。")

def main():
    """
    主函数，支持从命令行读取用户提醒内容。
    """
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        start_reminder_task(user_input)
    else:
        print("请提供提醒内容，例如：'提醒我1分钟之后喝水'。")

if __name__ == "__main__":
    main()
