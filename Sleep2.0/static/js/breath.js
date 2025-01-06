function _generate_heartbeat_series(data) {
  return {
    "name": '呼吸率',
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


function generate_breath(breath_list) {
    breath_option = {
      tooltip: {
        trigger: 'axis',
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
        min: 5,
        max: 25,
        axisTick: { show: false },
        axisLine: { onZero: false },
        axisLabel: {
          formatter: '{value}',
          color: "#fefefe"
        },
        boundaryGap: false
      },
      series: [

      ]
    };

    for (data of breath_list) {
      breath_option["series"].push(_generate_heartbeat_series(data));
    }  
    var breath = echarts.init(document.getElementById('breath'));
  breath.setOption(breath_option)
}