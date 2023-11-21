<template>
    <div id="chart-hist" style="height: 300px; width: 100%;"></div>
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
import data from '@/assets/chart/hist.js';
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

    var chartDom = document.getElementById('chart-hist');
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
        grid: {
            left: '15%',
            right: '15%',
            bottom: '60',
            top: '60'
        },
        title: {
            text: 'Application Duration'
        },
        legend: {
            data: ['pass', 'rejected'],
            bottom: 10
        },
        xAxis: [
            {
                type: 'category',
                name: 'duration',
                data: data.label,
                axisPointer: {
                    type: 'shadow'
                },
                axisLabel: {
                    formatter: '{value} day'
                },
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '# pass case',
                min: 0,
                max: 200,
                interval: 20,
                axisLabel: {
                    formatter: '{value}'
                }
            },
            // {
            //     type: 'value',
            //     name: '# rejected case',
            //     min: 0,
            //     max: 200,
            //     interval: 20,
            //     axisLabel: {
            //         formatter: '{value}'
            //     }
            // },
        ],
        series: [
            {
                name: 'pass',
                type: 'bar',
                color: 'lightgreen',
                tooltip: {
                    valueFormatter: function (value) {
                        return value + ' case';
                    }
                },
                data: data.pass
            },
            {
                name: 'rejected',
                type: 'bar',
                color: 'red',
                // yAxisIndex: 1,
                tooltip: {
                    valueFormatter: function (value) {
                        return value + ' case';
                    }
                },
                data: data.rejected
            }
        ]
    };

    option && myChart.setOption(option);



}, 500)

</script>