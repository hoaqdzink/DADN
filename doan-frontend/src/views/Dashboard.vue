<template>
  <button class="ui button big toggle" @click="toggleMode">{{ buttons.mode == 0 ?
    'MANUALLY' :
    'AUTOMATICALLY'
  }}</button>
  <button class="ui button big toggle" :class="{ active: buttons.motorCtrl == 1 }" @click="toggleMotor">{{
    buttons.motorCtrl
    ==
    1 ?
    'ON' :
    'OFF'
  }}</button>
</template>

<script setup>
import { reactive } from "vue"
import HTTPService from "@/common/HTTP"
let buttons = reactive({ mode: 0, motorCtrl: 0 })

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

<style>
body {
  background: var(--color-background);
}
</style>
