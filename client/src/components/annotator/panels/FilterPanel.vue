<template>
  <div v-show="filter.isActive">
    <PanelToggle name="ExG" v-model="filter.color.exg" />
    <PanelToggle name="ExGExR" v-model="filter.color.exgexr" />
    <PanelToggle name="CIVE" v-model="filter.color.cive" />
    <PanelInputNumber
      v-show="filter.color.cive"
      name="R"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_r"
    />
    <PanelInputNumber
      v-show="filter.color.cive"
      name="G"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_g"
    />
    <PanelInputNumber
      v-show="filter.color.cive"
      name="B"
      min="-1.0"
      max="1.0"
      step="0.001"
      v-model="filter.settings.cive_b"
    />
    <PanelInputNumber
      v-show="filter.color.cive"
      name="bias"
      min="-20.0"
      max="20.0"
      step="0.001"
      v-model="filter.settings.cive_bias"
    />
    <PanelButton 
      v-show="filter.color.cive"
      name="Reset" 
      v-model="filter.color.cive_reset" />

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
