<script>
import paper from "paper";
import tool from "@/mixins/toolBar/tool";
import UndoAction from "@/undo";

import { invertColor } from "@/libs/colors";
import { BBox } from "@/libs/bbox";
import { Point } from "@/libs/bbox";
import { mapMutations } from "vuex";

import toastrs from "@/mixins/toastrs";
import axios from "axios";

import { vIndex } from "@/libs/vindex";

export default {
  name: "FBoxTool",
  mixins: [tool, toastrs],
  props: {
    scale: {
      type: Number,
      default: 1
    },
    settings: {
        type: [Object, null],
        default: null
    }
  },
  data() {
    return {
      icon: "fa-hand-pointer-o",
      name: "FBox",
      scaleFactor: 3,
      cursor: "copy",
      bbox: null,
      polygon: {
        path: null,
        guidance: true,
        pathOptions: {
          strokeColor: "black",
          strokeWidth: 1
        }
      },
      color: {
        blackOrWhite: true,
        auto: true,
        radius: 10,
        circle: null
      },
      actionTypes: Object.freeze({
        ADD_POINTS: "Added Points",
        CLOSED_POLYGON: "Closed Polygon",
        DELETE_POLYGON: "Delete Polygon"
      }),
      actionPoints: 0
    };
  },
  methods: {
    ...mapMutations(["addUndo", "removeUndos"]),
    export() {
      return {
        completeDistance: this.polygon.completeDistance,
        minDistance: this.polygon.minDistance,
        blackOrWhite: this.color.blackOrWhite,
        auto: this.color.auto,
        radius: this.color.radius,
      };
    },
    setPreferences(pref) {
      this.color.blackOrWhite = pref.blackOrWhite || this.color.blackOrWhite;
      this.color.auto = pref.auto || this.color.auto;
      this.color.radius = pref.radius || this.color.radius;
    },
    createFBox(event) {
      this.polygon.path = new paper.Path(this.polygon.pathOptions);
      this.fbox = new BBox(event.point);
      this.fbox.getPoints().forEach(point => this.polygon.path.add(point));
    },

    modifyFBox(event) {
      this.polygon.path = new paper.Path(this.polygon.pathOptions);
      this.fbox.modifyPoint(event.point);
      this.fbox.getPoints().forEach(point => this.polygon.path.add(point));
    },
    /**
     * Frees current bbox
     */
    deleteFbox() {
      if (this.polygon.path == null) return;

      this.polygon.path.remove();
      this.polygon.path = null;

      if (this.color.circle == null) return;
      this.color.circle.remove();
      this.color.circle = null;
    },
    autoStrokeColor(point) {
      if (this.color.circle == null) return;
      if (this.polygon.path == null) return;
      if (!this.color.auto) return;

      this.color.circle.position = point;
      let raster = this.$parent.image.raster;
      let color = raster.getAverageColor(this.color.circle);
      if (color) {
        this.polygon.pathOptions.strokeColor = invertColor(
          color.toCSS(true),
          this.color.blackOrWhite
        );
      }
    },
    checkAnnotationExist() {
      return (
        !!this.$parent.currentAnnotation &&
        !!this.$parent.currentAnnotation.annotation.paper_object.length
      );
    },
    onMouseDown(event) {
      if (this.polygon.path == null && this.checkAnnotationExist()) {
        this.$parent.currentCategory.createAnnotation();
      }
      if (this.polygon.path == null) {
        this.createFBox(event);
        return;
      }
      this.removeLastFBox();
      this.modifyFBox(event);

      if (this.completeFBox()) return;
    },
    onMouseMove(event) {
      if (this.polygon.path == null) return;
      if (this.polygon.path.segments.length === 0) return;
      this.autoStrokeColor(event.point);

      this.removeLastFBox();
      this.modifyFBox(event);
    },
    /**
     * Undo points
     */
    undoPoints(args) {
      if (this.polygon.path == null) return;

      let points = args.points;
      let length = this.polygon.path.segments.length;

      this.polygon.path.removeSegments(length - points, length);
    },
    /**
     * Closes current polygon and unites it with current annotaiton.
     * @returns {boolean} sucessfully closes object
     */
    completeFBox() {
      if (this.polygon.path == null) return false;

      this.polygon.path.fillColor = "black";
      this.polygon.path.closePath();

      let points = this.fbox.getPoints();

      this.apply(points)
      this.$parent.uniteCurrentAnnotation(this.polygon.path, true, true, true);

      this.polygon.path.remove();
      this.polygon.path = null;
      if (this.color.circle) {
        this.color.circle.remove();
        this.color.circle = null;
      }

      this.removeUndos(this.actionTypes.ADD_POINTS);

      return true;
    },
    removeLastFBox() {
      this.polygon.path.removeSegments();
    },
    apply(points) {
      console.log(points)
      axios
        .post(`/api/model/fbox/${this.$parent.image.id}`, {
          points: points,
          filter_type: 1,
          min_area: 50,
          exg_threshold: 30,
          exgr_const: 1.4,
          exgr_threshold: 30,
          cive_r:  0.441,
          cive_g:  0.811,
          cive_b:  0.3855,
          cive_bias: 18.78745,
          cive_threshold: 10
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
    }
  },
  computed: {
    isDisabled() {
      return this.$parent.current.annotation === -1;
    }
  },
  watch: {
    isActive(active) {
      if (active) {
        this.tool.activate();
        localStorage.setItem("editorTool", this.name);
      }
    },
    /**
     * Change width of stroke based on zoom of image
     */
    scale(newScale) {
      this.polygon.pathOptions.strokeWidth = newScale * this.scaleFactor;
      if (this.polygon.path != null)
        this.polygon.path.strokeWidth = newScale * this.scaleFactor;
    },
    "polygon.pathOptions.strokeColor"(newColor) {
      if (this.polygon.path == null) return;

      this.polygon.path.strokeColor = newColor;
    },
    "color.auto"(value) {
      if (value && this.polygon.path) {
        this.color.circle = new paper.Path.Rectangle(
          new paper.Point(0, 0),
          new paper.Size(10, 10)
        );
      }
      if (!value && this.color.circle) {
        this.color.circle.remove();
        this.color.circle = null;
      }
    }
  },
  created() {},
  mounted() {}
};
</script>
