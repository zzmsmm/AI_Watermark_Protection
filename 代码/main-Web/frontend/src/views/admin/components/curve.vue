<template>

		<div class="incentivecurve">
      <el-card>
		    <div id='incentivecurveid' style="margin-left: 5%; width: 90%;height:400px;"></div>
      </el-card>
    </div>

</template>

<script>
import * as echarts from 'echarts';
export default{
	name: 'incentivecurve',
	data(){
		return {
			option :{
				color: ['#69d300'],
				tooltip: {
					trigger: 'axis',
					axisPointer: {
						type: 'cross',
						label: {
							backgroundColor: '#6a7985'
						}
					}
				},
				legend: {
					data: ['浏览量']
				},
				toolbox: {
					feature: {
						saveAsImage: {}
					}
				},
				grid: {
					left: '4%',
					right: '4%',
					bottom: '3%',
					containLabel: true
				},
				xAxis:
					{
						type: 'category',
						//boundaryGap: false,
						data: ['1', '2', '3', '4', '5', '6', '7', '8']
						//data: []
					},
				yAxis:
					{
						type: 'value'
					},
				series: [
					{
						name: '浏览量',
						type: 'line',
						stack: '总量',
						areaStyle: {},
						emphasis: {
							focus: 'series'
						},
            data: ['1', '5', '3', '2', '4', '6', '7', '8']
						//data: []
					}
				]
			},
		}
	},
	mounted(){
	this.init_echarts()
	this.draw_incentive()
	},
	watch:{
		option:{
			handler(){
				this.draw_incentive()
		},
		deep:true
		}

	},
	methods: {
		init_echarts(){
			this.myChart = echarts.init(document.getElementById('incentivecurveid'))
		},
		draw_incentive(){
			this.myChart.setOption(this.option,true)
		}
	}
}
</script>

<style>
	.incentivecurve{
		margin-left: 0%;
		margin-top: 0px;
	}
</style>
