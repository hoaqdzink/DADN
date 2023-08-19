<template>
    <div :id="chartId" class="fill"></div>
</template>

<script setup>
import { lightningChart, AxisScrollStrategies, ColorRGBA, Themes, AxisTickStrategies } from '@arction/lcjs'
import { onMounted, onBeforeMount, onBeforeUnmount, defineProps, watch } from 'vue';

const props = defineProps(['points', 'title', 'unit'])

let chartId = null
let chart = null
let lineSeries = null

function createChart() {
    const chart = lightningChart()
        .ChartXY({
            container: chartId.toString(),
            theme: Themes.light,
        })
        .setTitle(props.title)
    chart
        .getDefaultAxisX()
        .setTickStrategy(AxisTickStrategies.Time)
        .setScrollStrategy(AxisScrollStrategies.progressive)
        .setInterval({ start: -1 * 60 * 1000, end: 0, stopAxisAfter: false })
        .setTitle('DateTime')
    chart
        .getDefaultAxisY()
        .setTitle(props.unit)
        .setScrollStrategy(AxisScrollStrategies.progressive)
        .setInterval({ start: 0, end: 50, stopAxisAfter: false })

    lineSeries = chart
        .addLineSeries()
        .setName(props.title)
        .setStrokeStyle((style) => style.setThickness(5))
        .setMouseInteractions(false)
        .add(props.points)

    chart
        .addLegendBox()
        .add(chart)
        .setAutoDispose({
            type: 'max-width',
            maxWidth: 0.3,
        })
    return chart;
}

onBeforeMount(() => {
    chartId = Math.trunc(Math.random() * 1000000)
})

onMounted(() => {
    chart = createChart()
})

onBeforeUnmount(() => { chart.dispose() })

watch(() => props.points, (newValue) => {
    lineSeries.add(newValue);
}, { deep: true });

</script>
<style scoped>
.fill {
    height: 100%;
}
</style>