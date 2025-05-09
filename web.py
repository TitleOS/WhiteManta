from flask import Flask, render_template
import requests
import os
import datetime

ipaddr = os.getenv("ip_address")

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
        system_stats_json = requests.get(f"http://{ipaddr}:14480/api/system-stats").json()
        
        self.disk_available_size = system_stats_json["disk_stats"]["available_size"]
        self.mountpoint = system_stats_json["disk_stats"]["mounted_on"]
        self.partition = system_stats_json["disk_stats"]["partition"]
        self.total_size = system_stats_json["disk_stats"]["total_size"]
        self.disk_used_percent = system_stats_json["disk_stats"]["used_percent"]
        self.disk_used_size = system_stats_json["disk_stats"]["used_size"]
        
        self.memory_free = system_stats_json["memory_stats"]["free"]
        self.memory_total = system_stats_json["memory_stats"]["total"]
        self.memory_used = system_stats_json["memory_stats"]["used"]

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
        response = requests.get(f"http://{ipaddr}:14480/api/analysis/live")
        analysis_report_json = response.json()
        
        if(response.status_code == 503):
            print("No QMDL data is being recorded, starting a new live recording.")
            start_rayhunter_recording()
        
        self.analyzer_one_name = analysis_report_json["analyzers"][0]["name"]
        self.analyzer_one_desc = analysis_report_json["analyzers"][0]["description"]
        self.analyzer_two_name = analysis_report_json["analyzers"][1]["name"]
        self.analyzer_two_desc = analysis_report_json["analyzers"][1]["description"]
        self.analyzer_three_name = analysis_report_json["analyzers"][2]["name"]
        self.analyzer_three_desc = analysis_report_json["analyzers"][2]["description"]
        
        self.system_arch = analysis_report_json["rayhunter"]["arch"]
        self.rayhunter_version = analysis_report_json["rayhunter"]["rayhunter_version"]
        self.system_os_version = analysis_report_json["rayhunter"]["system_os"]

class warnings:
    warning_one_timestamp = "placeholder"
    warning_one_event = "placeholder"
    
    def __init__(self):
        warnings_json = requests.get(f"http://{ipaddr}:14480/api/analysis-report/live", timeout=5).json()
        
        if warnings_json != None:
            self.warning_one_timestamp = warnings_json["warnings"][0]["warning"]["timestamp"]
            self.warning_one_event = warnings_json["warnings"][0]["event"]["message"]
            return self
        return None
        

def stop_rayhunter_recording():
    requests.post(f"http://{ipaddr}:14480/api/stop-recording")
    
def start_rayhunter_recording():
    requests.post(f"http://{ipaddr}:14480/api/start-recording")
    
def send_webhook():
    current_warning = warnings()
    if current_warning.warning_one_event != "placeholder":
        data = {'Stingray Detected', f"Warning: {current_warning.warning_one_event} @ {current_warning.warning_one_timestamp}"}
        webhook_url = os.getenv("webhook_url")
    
        if webhook_url != None:
            response = requests.post(webhook_url, data=data)
            if response.ok:
                print(f"Webhook was fired ({webhook_url} at {datetime.datetime.utcnow()}")
            else:
                print(f"Attempted to fire webhook however server returned a non-OK status code (Code: {str(response.status_code)}")
        else:
            print("Webhook URL not defined, so no POST sent.")


app = Flask(__name__)

@app.route("/")
def main_page():
    stats = system_stats()
    report = analysis_report()
    
    return render_template("index.html", disk_available=stats.disk_available_size, disk_mountpoint=stats.mountpoint, disk_partition=stats.partition, disk_total=stats.total_size, disk_used_percentage=stats.disk_used_percent, disk_used_space=stats.disk_used_size, ram_total=stats.memory_total, ram_free=stats.memory_free, ram_used=stats.memory_used, analyzer_one_name=report.analyzer_one_name, analyzer_one_desc=report.analyzer_one_desc, analyzer_two_name=report.analyzer_two_name, analyzer_two_desc=report.analyzer_two_desc, analyzer_three_name=report.analyzer_three_name, analyzer_three_desc=report.analyzer_three_desc, sys_arch=report.system_arch, ray_version=report.rayhunter_version, os_version=report.system_os_version)

@app.route("/warnings") #Construct a JSON object with the (currently only the first) warning's event message and timestamp of the event so that we can pass it to the HTML page via an endpoint. This also would allow for other entities to query for active warnings without scraping the full web page.
def warnings_page():
    current_warnings = warnings()
    
    banner_struct = {'banner_message': 'The airwaves are clear :)', 'banner_timestamp': datetime.datetime.utcnow(), 'banner_isgrn': 'True'}
    
    if current_warnings.warning_one_event != "placeholder":
        banner_struct["banner_message"] = f"WARNING: {current_warnings.warning_one_event} "
        banner_struct["banner_timestamp"] = f"@ {current_warnings.warning_one_timestamp}"
        banner_struct["banner_isgrn"] = False
    return banner_struct


def main():
    print("White Manta has started, setting up web server.")
    print(f"Local IP Address: {ipaddr}")
    if os.getenv("webhook_url"):
        print(f"Webhook URL Environment Variable Defined.\nWebhooks will be sent to {os.getenv("webhook_url")} upon Rayhunter warnings.")
    
    print("Refreshing rayhunter recorder status...")
    stop_rayhunter_recording() #Stop recording if it is already going, then restart it to ensure fresh information is populated
    start_rayhunter_recording()
    
    print("Starting Flask web server on port 8888...")
    app.run(host="0.0.0.0", port=8888, debug=False) #Map container port 8888 to target on host, run Flask without debug.
    print("White Manta has shut down.")
    
if __name__ == '__main__':
    main()
    