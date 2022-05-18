<template>
  <!-- <q-page class="flex flex-center"> -->
    <div class="cmt">
      <el-container>
        <el-header>
          <div class="post-title">
            <el-avatar
              shape="circle"
              :size="size"
              :src="post.header"
              class="header-img"
              @click.native="addRoute1"
            ></el-avatar>
            <div class="post-info">
              <span class="author-name">{{ post.authorName }}</span>
              <span class="author-time">{{ post.postTime }}</span>
            </div>
            

            <div class="post-close">
              <el-button
                size="medium"
                round
                class="el-icon-close"
                @click="addRoute2"
              ></el-button>
            </div>
          </div>
        </el-header>

        <el-main>
          <div class="demo-image__placeholder">
            <span class="demonstration"></span>
            <el-image
              style="width: 550px;  margin-left:50px margin-right:50px"
              :src="post.pictureUrl"
              :preview-src-list="post.previewUrl"
            ></el-image>
          </div>
          <div class="block" style="display: inline">
            <div style="float: left">
              <el-button
                size="medium"
                round
                class="el-icon-delete"
                @click.native="deletePost"
              ></el-button>
            </div>
            <div style="float: right">
              <span>
                <el-button
                  size="medium"
                  round
                  class="el-icon-thumb"
                  @click="dianZan"
                ></el-button>
                {{ post.likes }}</span
              >
            </div>
          </div>
        </el-main>

        <div v-clickoutside="hideReplyBtn" @click="inputFocus" class="my-reply">
          <el-avatar
            class="header-img"
            :size="40"
            :src="user.header"
          ></el-avatar>
          <div class="reply-info">
            <div
              tabindex="0"
              contenteditable="true"
              id="replyInput"
              spellcheck="false"
              placeholder="输入评论..."
              class="reply-input"
              @focus="showReplyBtn"
              @input="onDivInput($event)"
            ></div>
          </div>
          <div class="reply-btn-box" v-show="btnShow">
            <el-button
              class="reply-btn"
              size="medium"
              @click="sendComment"
              type="primary"
              >发表评论</el-button
            >
            <div class="anonymous-btn">
              <el-switch
                v-model="value1"
                active-color="#13ce66"
                inactive-color="#909399"
              >
              </el-switch
              ><span>匿名</span>
            </div>
          </div>
        </div></el-container
      >
      <div style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)">
        <div
          v-for="(item, i) in comments"
          :key="i"
          class="author-title reply-father"
        >
          <el-avatar
            class="header-img"
            :size="40"
            :src="item.headImg"
          ></el-avatar>
          <div class="author-info">
            <span class="author-name">{{ item.name }}</span>
            <span class="author-time">{{ item.time }}</span>
          </div>
          <div class="icon-btn">
            <i class="el-icon-thumb" @click="dianZan2"></i>{{ item.likes }}
            <i class="el-icon-delete" @click="deleteComment"></i>
          </div>
          <div class="talk-box">
            <p>
              <span class="reply">{{ item.comment }}</span>
            </p>
          </div>

          <div v-show="_inputShow(i)" class="my-reply my-comment-reply">
            <el-avatar
              class="header-img"
              :size="40"
              :src="myHeader"
            ></el-avatar>
          </div>
        </div>
      </div>
    </div>
  <!-- </q-page> -->
</template>

<script>
const clickoutside = {
  // 初始化指令
  bind(el, binding, node) {
    function documentHandler(e) {
      // 这里判断点击的元素是否是本身，是本身，则返回
      if (el.contains(e.target)) {
        return false;
      }
      // 判断指令中是否绑定了函数
      if (binding.expression) {
        // 如果绑定了函数 则调用那个函数，此处binding.value就是handleClose方法
        binding.value(e);
      }
    }
    // 给当前元素绑定个私有变量，方便在unbind中可以解除事件监听
    el.vueClickOutside = documentHandler;
    document.addEventListener("click", documentHandler);
  },
  update() {},
  unbind(el, binding) {
    // 解除事件监听
    document.removeEventListener("click", el.vueClickOutside);
    delete el.vueClickOutside;
  },
};
export default {
  name: "ArticleComment",
  data() {
    return {
      user: {
        userName: "abc",
        header: "",
        userId: 666,
      },
      value1: true,
      btnShow: false,
      index: "0",
      replyComment: "",
      myName: "Lana Del Rey",
      myHeader:
        "https://ae01.alicdn.com/kf/Hd60a3f7c06fd47ae85624badd32ce54dv.jpg",
      myId: 19870621,
      to: "",
      toId: -1,
      post: {
        header: "",
        authorName: "xxx",
        postTime: "2022年4月18日",
        likes: "28",
        flg: true,
        pictureUrl:
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
        previewUrl: [
          "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg",
        ],
      },
      comments: [
        {
          name: "Lana Del Rey",
          id: 19870621,
          headImg:
            "https://ae01.alicdn.com/kf/Hd60a3f7c06fd47ae85624badd32ce54dv.jpg",
          comment: "我发布一张新专辑Norman Fucking Rockwell,大家快来听啊",
          time: "2019年9月16日 18:43",

          likes: "15",
          inputShow: false,
          fig: true,
        },
      ],
    };
  },
  directives: { clickoutside },
  methods: {
    dianZan() {
      if (this.post.flg) {
        this.post.likes++;
        this.post.flg = false;
      } else {
        this.post.likes--;
        this.post.flg = true;
      }
    },
    dianZan2() {
      if (this.comments.flg) {
        this.comments.likes++;
        this.comments.flg = false;
      } else {
        this.comments.likes--;
        this.comments.flg = true;
      }
    },
    addRoute1() {
      this.$router.push("./Info");
    },
    addRoute2() {},
    deletePost() {},
    deleteComment() {},
    inputFocus() {
      var replyInput = document.getElementById("replyInput");
      replyInput.style.padding = "8px 8px";
      replyInput.style.border = "2px solid blue";
      replyInput.focus();
    },
    showReplyBtn() {
      this.btnShow = true;
    },
    hideReplyBtn() {
      this.btnShow = false;
      replyInput.style.padding = "10px";
      replyInput.style.border = "none";
    },
    showReplyInput(i, name, id) {
      this.comments[this.index].inputShow = false;
      this.index = i;
      this.comments[i].inputShow = true;
      this.to = name;
      this.toId = id;
    },
    _inputShow(i) {
      return this.comments[i].inputShow;
    },
    sendComment() {
      if (!this.replyComment) {
        this.$message({
          showClose: true,
          type: "warning",
          message: "评论不能为空",
        });
      } else {
        this.$message({
          showClose: true,
          type: "success",
          message: "评论成功",
        });
        let a = {};
        let input = document.getElementById("replyInput");
        let timeNow = new Date().getTime();
        let time = this.dateStr(timeNow);
        a.name = this.myName;
        a.comment = this.replyComment;
        a.headImg = this.myHeader;
        a.time = time;
        a.commentNum = 0;
        a.like = 0;
        this.comments.push(a);
        this.replyComment = "";
        input.innerHTML = "";
      }
    },

    onDivInput: function (e) {
      this.replyComment = e.target.innerHTML;
    },
    dateStr(date) {
      //获取js 时间戳
      var time = new Date().getTime();
      //去掉 js 时间戳后三位，与php 时间戳保持一致
      time = parseInt((time - date) / 1000);
      //存储转换值
      var s;
      if (time < 60 * 10) {
        //十分钟内
        return "刚刚";
      } else if (time < 60 * 60 && time >= 60 * 10) {
        //超过十分钟少于1小时
        s = Math.floor(time / 60);
        return s + "分钟前";
      } else if (time < 60 * 60 * 24 && time >= 60 * 60) {
        //超过1小时少于24小时
        s = Math.floor(time / 60 / 60);
        return s + "小时前";
      } else if (time < 60 * 60 * 24 * 30 && time >= 60 * 60 * 24) {
        //超过1天少于30天内
        s = Math.floor(time / 60 / 60 / 24);
        return s + "天前";
      } else {
        //超过30天ddd
        var date = new Date(parseInt(date));
        return (
          date.getFullYear() +
          "/" +
          (date.getMonth() + 1) +
          "/" +
          date.getDate()
        );
      }
    },
  },
};
</script>

<style lang="stylus" scoped>

.cmt
    position: fixed;
    top: 0;
    left: 0;
.post-title
    width:120%
    margin-left:-50px
    margin-right:-50px
    padding 10px 5px 15px 20px;
    .header-img
        display inline-block
        vertical-align top
        cursor pointer

    .post-info
        display inline-block
        margin-left 10px
        width 80%
        height 50px
        line-height 20px
        >span
            display block
            overflow hidden
            white-space nowrap
            text-overflow ellipsis
        .author-name
            color #000
            font-size 18px
            font-weight bold
        .author-time
            font-size 14px
            color #000
    .post-close
        display inline-block
        padding 10px
        vertical-align top



.my-reply
    padding 10px
    margin-left:-30px
    background-color #fafbfc
    .header-img
        display inline-block
        vertical-align top
    .reply-info
        display inline-block
        margin-left 5px
        width:90%
        @media screen and (max-width:1200px) {
            width 100%
        }
        .reply-input

            min-height 20px
            line-height 22px
            padding 10px
            color black
            background-color #fff
            border-radius 5px
            &:empty:before
                content attr(placeholder)
            &:focus:before
                content none
            &:focus

                padding 8px 8px
                border 2px
                box-shadow none
                outline none
    .reply-btn-box
        height 25px
        margin 10px 10px 10px 10px
        .reply-btn
            position relative
            float right

        .anonymous-btn
            position relative
            float left
            margin-top 5px

.my-comment-reply
    margin-left 50px
    .reply-input
        width flex
.author-title:not(:last-child)
    border-bottom: 1px solid rgba(178,186,194,.3)
.author-title
    padding 10px
    .header-img
        display inline-block
        vertical-align top
    .author-info
        display inline-block
        margin-left 5px
        width 60%
        height 40px
        line-height 20px
        >span
            display block

            overflow hidden
            white-space nowrap
            text-overflow ellipsis
        .author-name
            color #000
            font-size 18px
            font-weight bold
        .author-time
            font-size 14px
    .icon-btn
        width 30%
        padding 0 !important
        float right
        @media screen and (max-width : 1200px){
            width 20%
            padding 7px
        }
        >span
            cursor pointer
        .icon-font
            margin 0 5px
    .talk-box
        margin 0 50px
        >p
           margin 0
        .reply
            font-size 16px
            color #000
    .reply-box
        margin 10px 0 0 50px
        background-color #efefef
</style>
