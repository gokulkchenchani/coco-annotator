<template>
  <div v-show="fbox.isActive">
    <PanelButton name="Delete FBox" @click="fbox.deleteFbox" />
    <PanelToggle name="Auto Select Color" v-model="fbox.color.auto" />
    <PanelToggle
      v-show="fbox.color.auto"
      name="Only Black or White"
      v-model="fbox.color.blackOrWhite"
    />
    <PanelInputString
      name="Stroke Color"
      v-model="fbox.polygon.pathOptions.strokeColor"
    />
  </div>
</template>

<script>
import PanelButton from "@/components/PanelButton";
import PanelToggle from "@/components/PanelToggle";
import PanelInputString from "@/components/PanelInputString";
import PanelInputNumber from "@/components/PanelInputNumber";

export default {
  name: "FBoxPanel",
  components: { PanelButton, PanelToggle, PanelInputString, PanelInputNumber },
  props: {
    fbox: {
      type: Object,
      required: true
    }
  }
};
</script>
