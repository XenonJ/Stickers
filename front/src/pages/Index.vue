<template>
  <q-page class="flex flex-center">
    <canvas
      id="canvas"
      :width="canvasWidth"
      :height="canvasHeight"
    />
    <img src="http://127.0.0.1:8000/images/a.jpg" id="a" v-show="false">
  </q-page>
</template>

<script type="text/javascript">

export default {
  name: 'PageIndex',
  data() {
    return {
      canvasWidth: 1920,
      canvasHeight: 1080,
      ctx: {},
      posts: [
        {
          post_id: 111,
          x_coordinates: 0,
          y_coordinates: 0,
          rotation_angle: 0,
          picture_url: "http://127.0.0.1:8000/images/a.jpg",
          background_url: "",
        },
      ],
      user: {
        user_name: "",
        profile_url: "",
      },
    }
  },
  mounted(){
    var canvas = new fabric.Canvas('canvas');
    canvas.on('mouse:wheel', function(opt) {
      var delta = opt.e.deltaY;
      var zoom = canvas.getZoom();
      zoom *= 0.999 ** delta;
      if (zoom > 20) zoom = 20;
      if (zoom < 0.01) zoom = 0.01;
      canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom);
      opt.e.preventDefault();
      opt.e.stopPropagation();
    });
    canvas.on('mouse:down', function(opt) {
      var evt = opt.e;
      this.isDragging = true;
      this.selection = false;
      this.lastPosX = evt.clientX;
      this.lastPosY = evt.clientY;
    });
    canvas.on('mouse:move', function(opt) {
      if (this.isDragging) {
        var e = opt.e;
        var vpt = this.viewportTransform;
        vpt[4] += e.clientX - this.lastPosX;
        vpt[5] += e.clientY - this.lastPosY;
        this.requestRenderAll();
        this.lastPosX = e.clientX;
        this.lastPosY = e.clientY;
      }
    });
    canvas.on('mouse:up', function(opt) {
      // on mouse up we want to recalculate new interaction
      // for all objects, so we call setViewportTransform
      this.setViewportTransform(this.viewportTransform);
      this.isDragging = false;
      this.selection = true;
    });
    var img1 = document.getElementById('a');
    var imgInstance = new fabric.Image(img1, {
      left: 100,
      top: 100,
      angle: 30,
      opacity: 0.85,
    })
    imgInstance.set('selectable', false);
    canvas.add(imgInstance);
  },
  methods: {
    draw() {

    },
  }
}
</script>
