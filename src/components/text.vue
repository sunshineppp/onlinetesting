<template>
    <div class="text">
        <!-- <div id="EChart" style="width: 300px; height: 300px;"></div> -->
        <!-- <div id="EChart2" style="width: 300px; height: 300px;"></div> -->
        <div ref="EChart" style="width: 300px; height: 300px;"></div>
    </div>
</template>
 
<script>
export default {
    name: "text",
    data() {
        return {
            notProcessed: 3,
            passNumber: 5,
            totalNumber: 10
        }
    },
    methods: {
        getRenderer() {
            // console.log(this.$echarts);
            // 基于准备好的dom，初始化echarts实例
            // let EChart = this.$echarts.init(document.getElementById("EChart"));
            // let EChart2 = this.$echarts.init(document.getElementById("EChart2"));
            let EChart = this.$echarts.init(this.$refs.EChart);

            // 配置参数
            let config =
            {
                type: 'pie',
                series: [
                    {
                        value: this.notProcessed,
                        name: '未批改人数'
                    },
                    {
                        value: this.passNumber,
                        name: '合格人数'
                    },
                    {
                        value: (this.totalNumber - this.notProcessed - this.passNumber),
                        name: '不合格人数'
                    }
                ],
            }


            // 设置参数
            EChart.setOption(config);
            // EChart2.setOption(config[1]);

        },
    },
    mounted() {
        this.getRenderer();
    },
}
</script>

<style></style>