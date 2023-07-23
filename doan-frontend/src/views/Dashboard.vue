<template>
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
</template>

<script setup>
import { reactive } from "vue"
import HTTPService from "@/common/HTTP"
let buttons = reactive({ mode: 0, motorCtrl: 0 })
let system = reactive({ temp: [], humid: [], motor: false })

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
</style>

<style>
body {
  background: var(--color-background);
}
</style>
