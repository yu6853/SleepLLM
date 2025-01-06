function filldata(sleep_quality,
    heartbeat_list,
    breath_list,
    // sleep_beg_ed,
    onbed_duration,
    sleep_duration,
    action_num,
    snore_num,
    leave_num,
    apnoea_num,
    avg_breath_rate,
    avg_heartbeat_rate,
    sleep_efficency,
    conversation) {
        // $(".sleep_beg_ed").html(sleep_beg_ed)
        $(".onbed_duration").html(onbed_duration)
        $(".sleep_duration").html(sleep_duration)
        $(".action_num").html(action_num)
        $(".snore_num").html(snore_num)
        $(".leave_num").html(leave_num)
        $(".apnoea_num").html(apnoea_num)
        $(".avg_breath_rate").html(avg_breath_rate)
        $(".avg_heartbeat_rate").html(avg_heartbeat_rate)
        $(".sleep_efficency").html(sleep_efficency)
        generate_gradeRating(sleep_quality)
        generate_heartbeat(heartbeat_list)
        generate_breath(breath_list)
        sendMessage(role="user", message=conversation["user"]);
        sendMessage(role="assistant", message=conversation["assistant"]);
    }
