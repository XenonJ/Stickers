<template>
  <q-page class="flex flex-center" style="overflow: hidden" id="page">
    <canvas
      id="canvas"
      :width="canvasWidth"
      :height="canvasHeight"
      style="overflow: hidden"
    />
    <ArticleComment
      :token="this.token"
      :post_id="Number(this.presentPostID)"
      :profile_url="this.user.profile_url"
      :user_name="this.user.user_name"
      :picture_url="this.presentPostURL"
      v-show="showPost"
      ref="ArticleComment">
    </ArticleComment>
    <myself
      :profile_url="this.user.profile_url"
      :token="this.token"
      :user_id="183945038485"
      :user_name="this.user.user_name"
      v-show="showMyself">
    </myself>
    <others v-show="showOthers">
    </others>
    <img
      v-for="post in static_posts"
      :key="post.post_id"
      :src="post.picture_url"
      :id="post.post_id"
      v-show="false"
    >
  </q-page>
</template>

<script type="text/javascript">
import ArticleComment from 'src/pages/comment.vue';
import myself from 'src/pages/myself.vue';
import others from 'src/pages/others.vue';
import Axios from "axios";
export function create(Component, props) {
 const comp = new (Vue.extend(Component))({ propsData: props }).$mount()
 document.getElementById("page").appendChild(comp.$el)

 comp.remove = () => {
  document.body.removeChild(comp.$el)

  comp.$destroy()
 }

 return comp
}
export default {
  name: 'PageIndex',
  components:{
    ArticleComment,
    myself,
    others,
  },
  data() {
    return {
      canvasWidth: 1920,
      canvasHeight: 1080,
      ctx: {},
      showPost: false,
      showMyself: false,
      showOthers: false,
      numPost: 5,
      token: "a",
      presentPostID: 0,
      presentPostURL: "http://127.0.0.1:8000/images/a.jpg",
      static_posts: [
        {
          post_id: 0,
          x_coordinates: 12,
          y_coordinates: 12,
          rotation_angle: 12,
          picture_url: "http://127.0.0.1:8000/images/a.jpg",
          background_url: "",
        },
        {
          post_id: 1,
          x_coordinates: 1200,
          y_coordinates: 1200,
          rotation_angle: -30,
          picture_url: "http://127.0.0.1:8000/images/b.jpg",
          background_url: "",
        },
        {
          post_id: 2,
          x_coordinates: 3200,
          y_coordinates: 600,
          rotation_angle: -10,
          picture_url: "http://127.0.0.1:8000/images/c.jpg",
          background_url: "",
        },
        {
          post_id: 3,
          x_coordinates: 47,
          y_coordinates: 1100,
          rotation_angle: 15,
          picture_url: "http://127.0.0.1:8000/images/d.jpg",
          background_url: "",
        },
        {
          post_id: 4,
          x_coordinates: 1600,
          y_coordinates: 600,
          rotation_angle: -5,
          picture_url: "http://127.0.0.1:8000/images/e.jpg",
          background_url: "",
        },
        {
          post_id: 5,
          x_coordinates: 3500,
          y_coordinates: 500,
          rotation_angle: -5,
          picture_url: "http://127.0.0.1:8000/images/f.jpg",
          background_url: "",
        },
        {
          post_id: 6,
          x_coordinates: 3300,
          y_coordinates: 800,
          rotation_angle: -5,
          picture_url: "http://127.0.0.1:8000/images/g.jpg",
          background_url: "",
        },
        {
          post_id: 7,
          x_coordinates: 1600,
          y_coordinates: 1000,
          rotation_angle: -50,
          picture_url: "http://127.0.0.1:8000/images/h.jpg",
          background_url: "",
        },
      ],
      posts: [
        {
          post_id: 0,
          x_coordinates: 12,
          y_coordinates: 12,
          rotation_angle: 12,
          picture_url: "http://127.0.0.1:8000/images/1654799732.8270373IMG_1877.JPG",
          background_url: "",
        },
        {
          post_id: 1,
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
  created(){
    console.log("created");
    var _this = this;
    _this.token = _this.$route.query.token;
    console.log(_this.token);
    _this.getPosts();
  },
  mounted(){
    // console.log("mounted");
    // var _this = this;
    // _this.Refresh();
  },
  methods: {
    Refresh: function(){
      console.log("refresh");
      fabric.Object.prototype
      var _this = this;
      console.log(_this.posts);
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
    draw(canvas) {
      var _this = this;
      for(var i = 0; i < 8; i++){
        var post = _this.static_posts[i];
        console.log(post);
        var img = document.getElementById(post.post_id);
        var imageInstance = new fabric.Image(img, {
          left: post.x_coordinates,
          top: post.y_coordinates,
          angle: post.rotation_angle,
          hoverCursor: "pointer",
          selectable: false,
        });
        const num = new String(post.post_id);
        // imageInstance.on("mousedown", function(opt){
        //   if(!_this.showPost){
        //     _this.presentPostID = Number(num);
        //     // _this.$refs.ArticleComment.Refresh();
        //   }
        //   _this.showPost = !_this.showPost;
        // })
        canvas.add(imageInstance);
      }
      for(var i = 0; i < _this.posts.length; i++){
        var post = _this.posts[i];
        fabric.Image.fromURL(post.picture_url, (img)=>{
            img.set({
              left: Number(JSON.stringify(post.x_coordinates)),
              top: Number(JSON.stringify(post.y_coordinates)),
              angle: Number(JSON.stringify(post.rotation_angle)),
              hoverCursor: "pointer",
              selectable: true,
            });
            img.on("mousedown", function(opt){
              if(!_this.showPost){
                _this.presentPostURL = post.picture_url;
                // _this.$refs.ArticleComment.Refresh();
              }
              _this.showPost = !_this.showPost;
            })
            canvas.add(img);
        });
        // var img = document.getElementById(post.post_id);
        // var imageInstance = new fabric.Image(img, {
        //   left: post.x_coordinates,
        //   top: post.y_coordinates,
        //   angle: post.rotation_angle,
        //   hoverCursor: "pointer",
        //   selectable: false,
        // });
        // const num = new String(post.post_id);
        // imageInstance.on("mousedown", function(opt){
        //   if(!_this.showPost){
        //     _this.presentPostID = Number(num);
        //     _this.$refs.ArticleComment.Refresh();
        //   }
        //   _this.showPost = !_this.showPost;
        // })
        // canvas.add(imageInstance);
      }
    },
    async getPosts(){
      console.log("get post");
      await Axios
        .get("http://127.0.0.1:8000/pages/main_page/", {
            params:{
                token: this.token,
            }
        })
        .then(response => {
            var _this = this;
            _this.posts = response.data.data.posts;
            _this.user = response.data.data.user;
            console.log(_this.posts);
            _this.Refresh();
        })
        .catch(function(error){
            console.log(error);
        });
    },
    closePost(){
      this.showPost = false;
    },
    displayMyself(){
      this.showMyself = true;
    },
    closeMyself(){
      this.showMyself = false;
    }
  }
}
</script>
