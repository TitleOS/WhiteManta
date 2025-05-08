from flask import Flask, render_template
import requests
import socket
import os

ipaddr = socket.gethostbyname(socket.gethostbyname())

class system_stats:
    disk_available_size = "not filled"
    mountpoint = "not filled"
    partition = "not filled"
    total_size = "not filled"
    disk_used_percent = "not filled"
    disk_used_size = "not filled"
    
    memory_free = "not filled"
    memory_total = "not filled"
    memory_used = "not filled"
    
    def __init__(self):
        system_stats_json = requests.get(f"http://{ipaddr}:14488/api/system-stats").json
        
        self.disk_available_size = [system_stats_json]["disk_stats"]["available_size"]
        self.mountpoint = [system_stats_json]["disk_stats"]["mounted_on"]
        self.partition = [system_stats_json]["disk_stats"]["partition"]
        self.total_size = [system_stats_json]["disk_stats"]["total_size"]
        self.disk_used_percent = [system_stats_json]["disk_stats"]["used_percent"]
        self.disk_used_size = [system_stats_json]["disk_stats"]["used_size"]
        
        self.memory_free = [system_stats_json]["memory_stats"]["free"]
        self.memory_total = [system_stats_json]["memory_stats"]["total"]
        self.memory_used = [system_stats_json]["memory_stats"]["used"]

class analysis_report:
    analyzer_one_name = "not filled"
    analyzer_one_desc = "not filled"
    analyzer_two_name = "not filled"
    analyzer_two_desc = "not filled"
    analyzer_three_name = "not filled"
    analyzer_three_desc = "not filled"
    
    system_arch = "not filled"
    rayhunter_version = "not filled"
    system_os_version = "not filled"
    
    def __init__(self):
        analysis_report_json = requests.get(f"http://{ipaddr}:14488/api/analysis/live").json
        
        self.analyzer_one_name = [analysis_report_json]["analyzers"][0]["name"]
        self.analyzer_one_name = [analysis_report_json]["analyzers"][0]["description"]
        self.analyzer_two_name = [analysis_report_json]["analyzers"][1]["name"]
        self.analyzer_two_name = [analysis_report_json]["analyzers"][1]["description"]
        self.analyzer_three_name = [analysis_report_json]["analyzers"][2]["name"]
        self.analyzer_three_name = [analysis_report_json]["analyzers"][2]["description"]
        
        self.system_arch = [analysis_report_json]["rayhunter"]["arch"]
        self.rayhunter_version [analysis_report_json]["rayhunter"]["rayhunter_version"]
        self.system_os_version [analysis_report_json]["rayhunter"]["system_os"]

def stop_rayhunter_recording():
    requests.post(f"http://{ipaddr}:14488/api/stop-recording")
    
def start_rayhunter_recording():
    requests.post(f"http://{ipaddr}:14488/api/start-recording")
    
def send_webhook():
    data = {'Stingray Detected', 'True'}
    webhook_url = os.getenv("webhook_url")
    
    if webhook_url != None:
        requests.post(webhook_url, data=data)
    else:
        print("Webhook URL not defined, so no POST sent.")


app = Flask(__name__)

@app.route("/")
def main_page():
    stats = system_stats()
    report = analysis_report()
    
    return render_template("index.html", disk_available=stats.disk_available_size, disk_mountpoint=stats.mountpoint, disk_partition=stats.partition, disk_total=stats.total_size, disk_used_percentage=stats.disk_used_percent, disk_used_space=stats.disk_used_size, ram_total=stats.memory_total, ram_free=stats.memory_free, ram_used=stats.memory_used, analyzer_one_name=report.analyzer_one_name, analyzer_one_desc=report.analyzer_one_desc, analyzer_two_name=report.analyzer_two_name, analyzer_two_desc=report.analyzer_two_desc, analyzer_three_name=report.analyzer_three_name, analyzer_three_desc=report.analyzer_three_desc, sys_arch=report.system_arch, ray_version=report.rayhunter_version, os_version=report.system_os_version)

print(f"Local IP Address: {ipaddr}")
start_rayhunter_recording() #Start recording so the live analysis API is populated
app.run(host="0.0.0.0", port=8888, debug=False) #Map container port 8888 to target on host
print("White Manta Web Page bound to local port 8888")