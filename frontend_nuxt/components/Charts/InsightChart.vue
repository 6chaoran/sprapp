<template>
    <div id="chart" style="height: 300px; width: 100%;" ></div>
</template>

<script setup>

import * as echarts from 'echarts/core';
import {
    ToolboxComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
TitleComponent
} from 'echarts/components';
import { BarChart, LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import data from '~/server/chart/timeseries.js';
// Create the echarts instance
setTimeout(() => {

    echarts.use([
        ToolboxComponent,
        TooltipComponent,
        GridComponent,
        LegendComponent,
        TitleComponent,
        BarChart,
        LineChart,
        CanvasRenderer,
        UniversalTransition
    ]);

    var chartDom = document.getElementById('chart');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        // toolbox: {
        //     feature: {
        //         dataView: { show: true, readOnly: false },
        //         magicType: { show: true, type: ['line', 'bar'] },
        //         restore: { show: true },
        //         saveAsImage: { show: true }
        //     }
        // },
        title: {
            text: 'SPR Application Passing Rate'
        },
        grid: {
            left: '15%',
            right: '15%',
            bottom: '60',
            top: '60'
        },
        legend: {
            data: ['# Application', 'Passing Rate'],
            bottom: 10
        },
        xAxis: [
            {
                type: 'category',
                data: data.year,
                axisPointer: {
                    type: 'shadow'
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '# Applications',
                min: 0,
                max: 200,
                interval: 20,
                axisLabel: {
                    formatter: '{value}'
                }
            },
            {
                type: 'value',
                name: 'passing rate',
                min: 0,
                max: 100,
                interval: 10,
                axisLabel: {
                    formatter: '{value}%'
                }
            }
        ],
        series: [
            {
                name: '# Application',
                type: 'bar',
                tooltip: {
                    valueFormatter: function (value) {
                        return value + ' case';
                    }
                },
                data: data.count
            },
            {
                name: 'Passing Rate',
                type: 'line',
                yAxisIndex: 1,
                tooltip: {
                    valueFormatter: function (value) {
                        return value + '%';
                    }
                },
                data: data.pass_rate.map((x) => (x * 100).toFixed(0))
            }
        ]
    };

    option && myChart.setOption(option);



}, 500)

</script>