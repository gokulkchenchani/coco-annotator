<script>
import paper from "paper";
import tool from "@/mixins/toolBar/tool";
import axios from "axios";

export default {
  name: "FilterTool",
  mixins: [tool],
  props: {
    scale: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      icon: "fa-filter",
      name: "Filter",
      cursor: "crosshair",
      settings: {
        cive_r:  0.441,
        cive_g:  0.811,
        cive_b:  0.385,
        cive_bias: 18.78745
      },
      points: []
    };
  },
  methods: {
    
  },
  computed: {
    isDisabled() {
      return this.$parent.current.annotation == -1;
    }
  },
  watch: {
    loading() {
      this.icon = this.loading ? "fa-spinner fa-spin" : "fa-filter";
    },
    disabled() {
      this.iconColor = this.disabled ? this.color.disabled : this.color.enabled;
    }
  }
};
</script>
