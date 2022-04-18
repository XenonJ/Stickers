<template>
  <q-page class="flex flex-center">
    <canvas
      id="canvas"
      :width="canvasWidth"
      :height="canvasHeight"
      :style="'width:'+canvasWidth/2+'px;height:'+canvasHeight/2+'px;'"
      @mousedown="canvasDown($event)"
      @mouseup="canvasUp($event)"
      @mousemove="canvasMove($event)"
    />
  </q-page>
</template>

<script type="text/javascript">

export default {
  name: 'PageIndex',
  data() {
    return {
      canvasWidth: 1920,
      canvasHeight: 1080,
      reactPos: {
        x: 0,
        y: 0,
      },
      isMouseDown: false,
      transX: 0,
      transY: 0,
      PosX: 0,
      PosY: 0,
      ctx: {},
    }
  },
  mounted(){
    const canvas = document.querySelector('#canvas');
    this.ctx = canvas.getContext('2d');
    this.draw();
  },
  methods: {
    draw() {
      var _this = this
      var ctx = _this.ctx
      ctx.clearRect(0, 0, _this.canvasWidth, _this.canvasHeight)
      var img = new Image();

      img.onload = function(){
        ctx.drawImage(img, _this.transX + _this.PosX, _this.transY + _this.PosY);
        console.log(_this.transX, _this.transY)
      }
      img.src = 'http://127.0.0.1:8000/images/a.jpg';
    },

    canvasDown(e){
      this.isMouseDown = true;

      const {target} = e

      this.reactPos.x = e.clientX
      this.reactPos.y = e.clientY
      console.log(this.reactPos.x, this.reactPos.y)
      this.draw()
    },

    canvasMove(e){
      if(this.isMouseDown){

        const mouseX = e.clientX
        const mouseY = e.clientY

        const {x, y} = this.reactPos

        var DivX = mouseX - x
        var DivY = mouseY - y

        this.transX = DivX
        this.transY = DivY

        this.draw()

        console.log(DivX, DivY)
      }
    },

    canvasUp(e){
      const mouseX = e.clientX
      const mouseY = e.clientY

      console.log(mouseX, mouseY)

      this.PosX += this.transX
      this.PosY += this.transY
      this.transX = 0
      this.transY = 0

      this.isMouseDown = false
    },
  }
}
</script>
