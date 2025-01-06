function generate_gradeRating(sleep_quality) {
  var name = "";
  if (sleep_quality > 0.75) {name = "极好";}
  else if (sleep_quality > 0.5) {name = "良好";}
  else if (sleep_quality > 0.25) {name = "较差";}
  else {name = "很差";}
  var gradeRating_option = {
     series: [
        {
          type: 'gauge',
          startAngle: 230,
          endAngle: -50,
          center: ['50%', '55%'],
          radius: '90%',
          min: 0,
          max: 1,
          splitNumber: 5,
          axisLine: {
            lineStyle: {
              width: 6,
              color: [
                [0.25, '#FF6E76'],
                [0.5, '#FDDD60'],
                [0.75, '#58D9F9'],
                [1, '#7CFFB2']
              ]
            }
          },
          pointer: {
            icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
            length: '12%',
            width: 20,
            offsetCenter: [0, '-60%'],
            itemStyle: {
              color: 'auto'
            }
          },
          axisTick: {
            length: 12,
            lineStyle: {
              color: 'auto',
              width: 2
            }
          },
          splitLine: {
            length: 20,
            lineStyle: {
              color: 'auto',
              width: 5
            }
          },
          axisLabel: {
            color: '#464646',
            fontSize: 12,
            distance: -45,
            rotate: 'tangential',
            formatter: function (value) {
              if (value === 0.875) {
                return 'Grade A';
              } else if (value === 0.625) {
                return 'Grade B';
              } else if (value === 0.375) {
                return 'Grade C';
              } else if (value === 0.125) {
                return 'Grade D';
              }
              return '';
            }
          },
          title: {
            offsetCenter: [0, '-10%'],
            fontSize: 20,
            color: "#fefefe"
          },
          detail: {
            fontSize: 20,
            offsetCenter: [0, '-35%'],
            valueAnimation: true,
            formatter: function (value) {
              return Math.round(value * 100) + '';
            },
            color: 'inherit'
          },
          data: [
            {
              value: sleep_quality,
              name: name
            }
          ]
        }
      ]
    };
  var gradeRating = echarts.init(document.getElementById('gradeRating'));
  gradeRating.setOption(gradeRating_option)

// function get_sleep_quality() {
//     $.ajax({
//         url: '/get_sleep_quality',
//         success:function(data) {
//             gradeRating_option["series"][0]["data"][0]["value"] = data['sleep_quality']
//             gradeRating.setOption(gradeRating_option)
//         },
//         error:function() {
//             alert("get_sleep_quality error!")
//         }
//     })
// }

// setInterval(get_sleep_quality, 5000)
}
