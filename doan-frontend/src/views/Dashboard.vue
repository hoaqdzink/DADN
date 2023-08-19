<template>
  <div class="row">
    <span class="tittle">Notification: </span>
    <label class="switch">
      <input type="checkbox" :checked="buttons.notified" v-on:click="onNotified">
      <span class="slider round-notify"></span>
    </label>
  </div>

  <div class="row">
    <span class="tittle">Mode: </span>
    <button class="ui button big toggle" @click="toggleMode">{{ buttons.mode == 0 ?
      'MANUALLY' :
      'AUTOMATICALLY'
    }}</button>
  </div>
  <div class="row">
    <span class="tittle">Control: </span>
    <button class="ui button big toggle" :class="{ active: buttons.motorCtrl == 1 }" @click="toggleMotor">{{
      buttons.motorCtrl
      ==
      1 ?
      'ON' :
      'OFF'
    }}</button>
  </div>
  <div class="row">
    <span class="tittle">Motor: </span>
    <div class="round" :class="system.motor ? 'active' : 'disabled'"></div>
  </div>
  <div class="chart-container">
    <div class="chart">
      <Chart title="Temperature" unit="Celsius" :points="system.temp" />
    </div>
    <div class="chart">
      <Chart title="Humidity" unit="g.me-3" :points="system.humid" />
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue"
import HTTPService from "@/common/HTTP"
import Chart from "../components/chart.vue";

let buttons = reactive({ mode: 0, motorCtrl: 0, notified: false })
let system = reactive({ temp: [], humid: [], motor: false })
let timeOrigin = Date.now()

onMounted(async () => {
  let result = await HTTPService.getConfig()
  buttons.notified = result.data.isNotified
  let response = await HTTPService.stream()
  handleStreamData(response)
})


function handleStreamData(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  function readChunk() {
    reader.read().then(({ done, value }) => {
      if (done) {
        return;
      }

      let text = decoder.decode(value, { stream: true });
      let datas = JSON.parse(text)
      system.motor = datas.aio_feed_motor_fbk.value == "1"
      system.temp.push({ x: Date.now() - timeOrigin, y: datas.temp[0].value })
      system.humid.push({ x: Date.now() - timeOrigin, y: datas.humid[0].value })

      // Read the next chunk
      readChunk();
    });
  }

  readChunk();
}

async function toggleMode() {
  let tmp = null
  if (buttons.mode === 0) tmp = 1
  else if (buttons.mode === 1) tmp = 0
  let response = await HTTPService.add_motor_ctrl(tmp.toString())
  if (response.status == 201) buttons.mode = tmp
}

async function toggleMotor() {
  let tmp = null
  if (buttons.motorCtrl === 0) tmp = 1
  else if (buttons.motorCtrl === 1) tmp = 0
  let response = await HTTPService.add_motor_ctrl(tmp.toString())
  if (response.status == 201) buttons.motorCtrl = tmp
}

async function onNotified() {
  let isNotified = 1
  if (buttons.notified) isNotified = 0
  let response = await HTTPService.setNotified(isNotified)
  if (response.status == 204) buttons.notified = !buttons.notified
}

</script>

<style scoped>
.row {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-top: 20px;
}

span.tittle {
  display: inline-block;
}

.tittle {
  width: 200px;
  font-size: 25px;
  font-weight: 700;
}

.round {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.round.active {
  background: yellow
}

.round.disabled {
  background: #8D8D8D
}

.chart-container {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 50px;
  margin-top: 30px;
}

.chart {
  width: 1000px;
  height: 500px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked+.slider {
  background-color: #2196F3;
}

input:focus+.slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked+.slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round-notify {
  border-radius: 34px;
}

.slider.round-notify:before {
  border-radius: 50%;
}
</style>

<style>
body {
  background: var(--color-background);
}
</style>
