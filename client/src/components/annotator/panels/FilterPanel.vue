<template>
  <div v-show="filter.isActive">
    <PanelToggle name="ExG" @click="filter.exg" />
    <PanelToggle name="ExGExR" @click="filter.exgexr" />
    <PanelToggle name="CIVE" @click="filter.cive" />
    <PanelInputNumber
      v-show="filter.cive"
      name="R"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_r"
    />
    <PanelInputNumber
      v-show="filter.cive"
      name="G"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_g"
    />
    <PanelInputNumber
      v-show="filter.cive"
      name="B"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_b"
    />
    <PanelInputNumber
      v-show="filter.cive"
      name="bias"
      min="-20.0"
      max="20.0"
      step="0.001"
      v-model="filter.settings.cive_bias"
    />
    <PanelButton 
      v-show="filter.cive"
      name="Reset" 
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
