<template>
  <div v-show="filter.isActive">
    <PanelToggle name="ExG" v-model="filter.settings.exg" />
    <PanelInputNumber v-show="filter.settings.exg" name="Padding"
      min="0"
      max="1000"
      step="2"
      v-model="filter.settings.exg_padding"
    />
    <PanelInputNumber v-show="filter.settings.exg" name="Threshold"
      min="0"
      max="255"
      step="1"
      v-model="filter.settings.exg_threshold"
    />
    <PanelButton v-show="filter.settings.exg" name="Apply" 
      @click="filter.exg_apply" />
    <PanelButton v-show="filter.settings.exg" name="Reset" 
      @click="filter.exg_reset" />



    <PanelToggle name="ExGExR" v-model="filter.settings.exgexr" />
    <PanelInputNumber v-show="filter.settings.exgexr" name="Const"
      min="0"
      max="10"
      step="0.001"
      v-model="filter.settings.exgexr_const"
    />
    <PanelInputNumber v-show="filter.settings.exgexr" name="Threshold"
      min="0"
      max="255"
      step="1"
      v-model="filter.settings.exgexr_threshold"
    />
    <PanelButton v-show="filter.settings.exgexr" name="Apply" 
      @click="filter.exgexr_apply" />
    <PanelButton v-show="filter.settings.exgexr" name="Reset" 
      @click="filter.exgexr_reset" />



    <PanelToggle name="CIVE" v-model="filter.settings.cive" />
    <PanelInputNumber v-show="filter.settings.cive" name="R"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_r"
    />
    <PanelInputNumber v-show="filter.settings.cive" name="G"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_g"
    />
    <PanelInputNumber v-show="filter.settings.cive" name="B"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_b"
    />
    <PanelInputNumber v-show="filter.settings.cive" name="bias"
      min="-20.0"
      max="20.0"
      step="0.001"
      v-model="filter.settings.cive_bias"
    />
    <PanelInputNumber v-show="filter.settings.cive" name="Threshold"
      min="0"
      max="255"
      step="1"
      v-model="filter.settings.cive_threshold"
    />
    <PanelButton v-show="filter.settings.cive" name="Apply" 
      @click="filter.cive_apply" />
    <PanelButton  v-show="filter.settings.cive" name="Reset" 
      @click="filter.cive_reset" />

  </div>
</template>

<script>
import PanelButton from "@/components/PanelButton";
import PanelToggle from "@/components/PanelToggle";
import PanelInputString from "@/components/PanelInputString";
import PanelInputNumber from "@/components/PanelInputNumber";

export default {
  name: "FilterPanel",
  components: { PanelButton, PanelToggle, PanelInputNumber  },
  props: {
    filter: {
      type: Object,
      required: true
    }
  }
};
</script>
