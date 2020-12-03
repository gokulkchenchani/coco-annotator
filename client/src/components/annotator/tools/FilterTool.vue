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
    exg(){
      let canvas = this.$parent.image.raster.canvas;

      let data = new FormData();
      canvas.toBlob(blob => {
        data.append("image", blob);
        this.loading = true;

        axios
          .post(`/api/model/exg`, data, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(response => {
            let coco = response.data.coco || {};

            let images = coco.images || [];
            let categories = coco.categories || [];
            let annotations = coco.annotations || [];

            if (
              images.length == 0 ||
              categories.length == 0 ||
              annotations.length == 0
            ) {
              // Error
              return;
            }
            // Index categoires
            let indexedCategories = {};
            categories.forEach(category => {
              indexedCategories[category.id] = category;
            });

            annotations.forEach(annotation => {
              let keypoints = annotation.keypoints || [];
              let segmentation = annotation.segmentation || [];
              let category = indexedCategories[annotation.category_id];
              let isbbox = annotation.isbbox || false;

              this.$parent.addAnnotation(
                category.name,
                segmentation,
                keypoints,
                isbbox=isbbox
              );
            });
          })
          .catch(() => {
            this.axiosReqestError("Filter-Exg", "Could not run filter!!");
          })
          .finally(() => (this.loading = false));
      });
    },
    exgexr(){

    },
    cive(){

    },
    cive_reset(){
      this.settings.cive_r = 0.441;
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
    loading() {
      this.icon = this.loading ? "fa-spinner fa-spin" : "fa-filter";
    },
    disabled() {
      this.iconColor = this.disabled ? this.color.disabled : this.color.enabled;
    }
  }
};
</script>
