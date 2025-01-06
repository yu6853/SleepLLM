const url = '/getalldata'
const options = {
    method: 'get'
}

var sleep_quality = 0.0

fetch(url, options).then((response)=>{
    response.json().then((result)=>{
        var data = result
        sleep_quality = data["sleep_quality"]
        var heartbeat_list =  data["heartbeat_list"]
        var breath_list = data["breath_list"]
        // var sleep_beg_ed = data["sleep_beg_ed"]
        var onbed_duration = data["onbed_duration"]
        var sleep_duration = data["sleep_duration"]
        var action_num = data["action_num"]
        var snore_num = data["snore_num"]
        var leave_num = data["leave_num"]
        var apnoea_num = data["apnoea_num"]
        var avg_breath_rate = data["avg_breath_rate"]
        var avg_heartbeat_rate = data["avg_heartbeat_rate"]
        var sleep_efficency = data["sleep_efficency"]
        var conversation = data["conversation"]
        filldata(sleep_quality=sleep_quality,
            heartbeat_list=heartbeat_list,
            breath_list=breath_list,
            // sleep_beg_ed=sleep_beg_ed,
            onbed_duration=onbed_duration,
            sleep_duration=sleep_duration,
            action_num=action_num,
            snore_num=snore_num,
            leave_num=leave_num,
            apnoea_num=apnoea_num,
            avg_breath_rate=avg_breath_rate,
            avg_heartbeat_rate=avg_heartbeat_rate,
            sleep_efficency=sleep_efficency,
            conversation=conversation)
    },(error)=>{
        alert("process PromiseResult error!")
    })
},(error)=>{
    //处理错误
    alert("获取数据出错，请重新上传数据!")
})
