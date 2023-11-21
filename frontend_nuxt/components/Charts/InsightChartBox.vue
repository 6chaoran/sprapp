<template>
    <div id="chart-box" style="height: 300px; width: 100%;"></div>
</template>

<script setup>

import * as echarts from 'echarts/core';
import {
    DatasetComponent,
    TitleComponent,
    TooltipComponent,
    GridComponent,
    TransformComponent
} from 'echarts/components';
import { BoxplotChart, ScatterChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import { data, outliers } from '~/server/chart/box';

// Create the echarts instance
setTimeout(() => {

    echarts.use([
        DatasetComponent,
        TitleComponent,
        TooltipComponent,
        GridComponent,
        TransformComponent,
        BoxplotChart,
        ScatterChart,
        CanvasRenderer,
        UniversalTransition
    ]);
    var chartDom = document.getElementById('chart-box');
    var myChart = echarts.init(chartDom);
    var option = {
        // title: [
        // {
        //     text: 'Michelson-Morley Experiment',
        //     left: 'center'
        // },
        // {
        //     text: 'upper: Q3 + 1.5 * IQR \nlower: Q1 - 1.5 * IQR',
        //     borderColor: '#999',
        //     borderWidth: 1,
        //     textStyle: {
        //         fontSize: 14
        //     },
        //     left: '10%',
        //     top: '90%'
        // }
        // ],
        dataset: [
            {
                // prettier-ignore
                source: data
            },
            {
                transform: {
                    type: 'boxplot',
                    config: {
                        itemNameFormatter: function (params) {
                            if (params.value == 1) {
                                return 'pass ' //+ params.value;
                            } else {
                                return 'reject ' //+ params.value;
                            }
                        }
                    }
                }
            },

            {
                fromDatasetIndex: 1,
                fromTransformResult: 1
            }
        ],
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'shadow'
            },
            formatter: function (param) {
                return [
                    'Upper: ' + param.data[5] + ' days',
                    'Q3: ' + param.data[4]  + ' days',
                    'Median: ' + param.data[3]  + ' days',
                    'Q1: ' + param.data[2]  + ' days',
                    'Lower: ' + param.data[1]  + ' days',
                ].join('<br/>');
            }
        },
        grid: {
            left: '15%',
            right: '15%',
            bottom: '60',
            top: '60'
        },
        yAxis: {
            type: 'category',
            boundaryGap: true,
            nameGap: 30,
            splitArea: {
                show: false
            },
            splitLine: {
                show: false
            }
        },
        xAxis: {
            type: 'value',
            name: 'day',
            splitArea: {
                show: true
            }
        },

        series: [
            {
                name: 'boxplot',
                type: 'boxplot',
                datasetIndex: 1,
                itemStyle: {
                    color: '#b8c5f2'
                },

            },
            // {
            //     name: 'Outliers',
            //     type: 'scatter',
            //     data: outliers,
            //     markPoint: {
            //         symbol: 'circle',
            //         symbolSize: 10,
            //         itemStyle: {
            //             color: 'red'
            //         },
            //         data: outliers.map(function (item) {
            //             return {
            //                 coord: item,
            //                 value: item[1]  // Use the y-value of the outlier as the markPoint value
            //             };
            //         }),
            //     },
            // }


        ]
    }

    option && myChart.setOption(option);

}, 500)

</script>