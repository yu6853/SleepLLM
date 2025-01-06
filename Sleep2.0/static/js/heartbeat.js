function _generate_heartbeat_series(data) {
  return {
    "name": '心率',
    "type": 'line',
    "symbol": 'none',
    "lineStyle": {
      "width": 3,
    },
    "areaStyle": {},
    "color": data[0],
    "data": data[1]
  }
}

function generate_heartbeat(heartbeat_list) {
  heartbeat_option = {
    tooltip: {
      trigger: 'axis',
      // formatter: 'Temperature : <br/>{b}km : {c}°C'
    },
    grid: {
      top: '4%',
      left: '3%',
      right: '3%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'time',
      show: false,
    },
    yAxis: {
      type: 'value',
      max: 20,
      min: 100,
      axisTick: { show: false },
      axisLine: { onZero: false },
      axisLabel: {
        formatter: '{value}',
        color: "#fefefe"
      },
      boundaryGap: false,
    },
    series: [

    ]
  };
  // console.log(heartbeat_list);
  for (data of heartbeat_list) {
    heartbeat_option["series"].push(_generate_heartbeat_series(data));
  }
  var heartbeat = echarts.init(document.getElementById('heartbeat'));
  heartbeat.setOption(heartbeat_option)
}
