<template>
  <q-page class="flex flex-center">
    <canvas
      id="canvas"
      :width="canvasWidth"
      :height="canvasHeight"
    />
    <img
      v-for="post in posts"
      :key="post.post_id"
      :src="post.picture_url"
      :id="post.post_id"
      v-show="false"
    >
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
      numPost: 2,
      posts: [
        {
          post_id: 111,
          x_coordinates: 100,
          y_coordinates: 200,
          rotation_angle: 30,
          picture_url: "http://127.0.0.1:8000/images/a.jpg",
          background_url: "",
        },
        {
          post_id: 222,
          x_coordinates: 1200,
          y_coordinates: 600,
          rotation_angle: -30,
          picture_url: "http://127.0.0.1:8000/images/b.jpg",
          background_url: "",
        },
      ],
      user: {
        user_name: "1",
        profile_url: "",
      },
    }
  },
  mounted(){
    fabric.Object.prototype
    var _this = this;
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
      // if (opt.target) {
      //   console.log(opt.target);
      // }
      // else{
        var evt = opt.e;
        this.isDragging = true;
        this.selection = false;
        this.lastPosX = evt.clientX;
        this.lastPosY = evt.clientY;
      // }
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
    _this.draw(canvas);
  },
  methods: {
    draw(canvas) {
      var post;
      var _this = this;
      for(var i = 0; i < _this.numPost; i++){
        post = _this.posts[i];
        var img = document.getElementById(post.post_id);
        var imageInstance = new fabric.Image(img, {
          left: post.x_coordinates,
          top: post.y_coordinates,
          angle: post.rotation_angle,
          hoverCursor: "pointer",
          selectable: false,
        });
        const num = new String(post.post_id);
        imageInstance.on("mousedown", function(opt){
          console.log(num);
        })
        canvas.add(imageInstance);
      }
    },
  }
}
</script>
