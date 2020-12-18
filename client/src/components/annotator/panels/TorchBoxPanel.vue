<template>
  <div v-show="torchbox.isActive">
    <PanelButton name="Delete TrochBox" @click="torchbox.deleteTorchbox" />
    <PanelToggle name="Auto Select Color" v-model="torchbox.color.auto" />
    <PanelToggle
      v-show="torchbox.color.auto"
      name="Only Black or White"
      v-model="torchbox.color.blackOrWhite"
    />
    <PanelInputString
      name="Stroke Color"
      v-model="torchbox.polygon.pathOptions.strokeColor"
    />
  </div>
</template>

<script>
import PanelButton from "@/components/PanelButton";
import PanelToggle from "@/components/PanelToggle";
import PanelInputString from "@/components/PanelInputString";
import PanelInputNumber from "@/components/PanelInputNumber";

export default {
  name: "TrochBoxPanel",
  components: { PanelButton, PanelToggle, PanelInputString, PanelInputNumber },
  props: {
    torchbox: {
      type: Object,
      required: true
    }
  }
};
</script>
