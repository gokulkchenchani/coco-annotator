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
    };
  },
  methods: {
    exg(){
      let canvas = this.$parent.image.raster.canvas;

      let data = new FormData();
      canvas.toBlob(blob => {
        data.append("image", blob);
        this.loading = true;

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
          .finally(() => points.forEach(point => point.remove()));
      });
    },
    exgexr(){

    },
    cive(){

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
