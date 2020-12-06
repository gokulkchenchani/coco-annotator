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
        exg: false,
        exgexr: false,
        cive: false,
        exg_padding: 50,
        exg_threshold: 30,
        exgexr_const: 1.4,
        exgexr_threshold: 30,
        cive_r:  0.441,
        cive_g:  0.811,
        cive_b:  0.385,
        cive_bias: 18.78745
      }
    };
  },
  methods: {
    export() {
      return {
        exg: this.settings.exg
      };
    },
    exg_apply() {
    
      let currentAnnotation = this.$parent.currentAnnotation;
      let width = this.$parent.image.raster.width /2;
      let height = this.$parent.image.raster.height /2;

      axios
        .post(`/api/model/exg/${this.$parent.image.id}`, {
          ...this.settings
        })
        .then(response => {
          let segments = response.data.segmentaiton;
          let center = new paper.Point(width, height);

          let compoundPath = new paper.CompoundPath();
          for (let i = 0; i < segments.length; i++) {
            let polygon = segments[i];
            let path = new paper.Path();

            for (let j = 0; j < polygon.length; j += 2) {
              let point = new paper.Point(polygon[j], polygon[j + 1]);
              path.add(point.subtract(center));
            }
            path.closePath();
            compoundPath.addChild(path);
          }
          currentAnnotation.unite(compoundPath);
        })
        // .finally(() => points.forEach(point => point.remove()));
    },
    exg_reset(){
      this.settings.exg_padding = 50;
      this.settings.exg_threshold = 30;
    },
    exgexr_apply() {
    
      let currentAnnotation = this.$parent.currentAnnotation;
      let width = this.$parent.image.raster.width /2;
      let height = this.$parent.image.raster.height /2;

      axios
        .post(`/api/model/exgexr/${this.$parent.image.id}`, {
          ...this.settings
        })
        .then(response => {
          let segments = response.data.segmentaiton;
          let center = new paper.Point(width, height);

          let compoundPath = new paper.CompoundPath();
          for (let i = 0; i < segments.length; i++) {
            let polygon = segments[i];
            let path = new paper.Path();

            for (let j = 0; j < polygon.length; j += 2) {
              let point = new paper.Point(polygon[j], polygon[j + 1]);
              path.add(point.subtract(center));
            }
            path.closePath();
            compoundPath.addChild(path);
          }
          currentAnnotation.unite(compoundPath);
        })
        // .finally(() => points.forEach(point => point.remove()));
    },
    exgexr_reset(){
      this.settings.exgexr_const = 1.4;
      this.settings.exgexr_threshold = 30;
    },
    cive_apply() {
    
      let currentAnnotation = this.$parent.currentAnnotation;
      let width = this.$parent.image.raster.width /2;
      let height = this.$parent.image.raster.height /2;

      axios
        .post(`/api/model/cive/${this.$parent.image.id}`, {
          ...this.settings
        })
        .then(response => {
          let segments = response.data.segmentaiton;
          let center = new paper.Point(width, height);

          let compoundPath = new paper.CompoundPath();
          for (let i = 0; i < segments.length; i++) {
            let polygon = segments[i];
            let path = new paper.Path();

            for (let j = 0; j < polygon.length; j += 2) {
              let point = new paper.Point(polygon[j], polygon[j + 1]);
              path.add(point.subtract(center));
            }
            path.closePath();
            compoundPath.addChild(path);
          }
          currentAnnotation.unite(compoundPath);
        })
        // .finally(() => points.forEach(point => point.remove()));
    },
    cive_reset(){
      this.settings.cive_r = 0.4414;
      this.settings.cive_g = 0.811;
      this.settings.cive_b = 0.385;
      this.settings.cive_bias = 18.78745;
    }
  },
  computed: {
    isDisabled() {
      return this.$parent.current.annotation == -1;
    }
  },
  watch: {
  
  }
};
</script>
