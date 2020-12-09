<script>
import toastrs from "@/mixins/toastrs";
import button from "@/mixins/toolBar/button";
import axios from "axios";

export default {
  name: "FilterButton",
  mixins: [button, toastrs],
  data() {
    return {
      icon: "fa-filter",
      name: "Filter",
      cursor: "crosshair",
      settings: {
        filter_type:1,
        min_area: 50,
        exg_threshold: 30,
        exgr_const: 1.4,
        exgr_threshold: 30,
        cive_r:  0.441,
        cive_g:  0.811,
        cive_b:  0.3855,
        cive_bias: 18.78745,
        cive_threshold: 10
      }
    };
  },
  methods: {
    exg_apply() {
      this.settings.filter_type = 0;
      this.apply(0);
    },
    exg_reset(){
      this.settings.exg_threshold = 35;
    },
    exgexr_apply() {
      this.settings.filter_type = 1;
      this.apply();
    },
    exgexr_reset(){
      this.settings.exgr_const = 1.4;
      this.settings.exgr_threshold = 30;
    },
    cive_apply() {
      this.settings.filter_type = 2;
      this.apply();
    },
    cive_reset(){
      this.settings.cive_r = 0.4414;
      this.settings.cive_g = 0.811;
      this.settings.cive_b = 0.385;
      this.settings.cive_bias = 18.78745;
      this.cive_threshold = 10;
    },
    apply() {
      let currentAnnotation = this.$parent.currentAnnotation;
      let width = this.$parent.image.raster.width /2;
      let height = this.$parent.image.raster.height /2;

      axios
        .post(`/api/model/vindex/${this.$parent.image.id}`, {
          ...this.settings
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
          this.axiosReqestError("Annotator", "Could not read data from URL");
        })
        .finally(() => (this.loading = false));
    //   let canvas = this.$parent.image.raster.canvas;

    //   let data = new FormData();
    //   canvas.toBlob(blob => {
    //     data.append("image", blob);
    //     this.loading = true;

        
    //     axios
    //       .post(`/api/model/vindex`, data, {
    //         headers: {
    //           "Content-Type": "multipart/form-data"
    //         }
    //       })
    //       .then(response => {
    //         let coco = response.data.coco || {};

    //         let images = coco.images || [];
    //         let categories = coco.categories || [];
    //         let annotations = coco.annotations || [];
            
    //         if (
    //           images.length == 0 ||
    //           categories.length == 0 ||
    //           annotations.length == 0
    //         ) {
    //           // Error
    //           return;
    //         }
    //         // Index categoires
    //         let indexedCategories = {};
    //         categories.forEach(category => {
    //           indexedCategories[category.id] = category;
    //         });

    //         annotations.forEach(annotation => {
    //           let keypoints = annotation.keypoints || [];
    //           let segmentation = annotation.segmentation || [];
    //           let category = indexedCategories[annotation.category_id];
    //           let isbbox = annotation.isbbox || false;

    //           this.$parent.addAnnotation(
    //             category.name,
    //             segmentation,
    //             keypoints,
    //             isbbox=isbbox
    //           );
    //         });
    //       })
    //       .catch(() => {
    //         this.axiosReqestError("Annotator", "Could not read data from URL");
    //       })
    //       .finally(() => (this.loading = false));
    //   });
    // }
  }
  }
};
</script>