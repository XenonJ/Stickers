<template>
  <q-page class="absolute-center">
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
              <span class="author-name">{{ post.user_name }}</span>
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
            <el-image
              style="width: 550px"
              :src="post.picture_url"
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
            :src="this.profile_url"
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
          v-for="(item, i) in this.comments"
          :key="i"
          class="author-title reply-father"
        >
          <el-avatar
            class="header-img"
            :size="40"
            :src="item.image_url"
          ></el-avatar>
          <div class="author-info">
            <span class="author-name">{{ item.user_name }}</span>
            <span class="author-time">{{ item.comment_time }}</span>
          </div>
          <div class="icon-btn">
            <i class="el-icon-thumb" @click="dianZan2"></i>{{ item.like_num }}
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
              :src="this.profile_url"
            ></el-avatar>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import Axios from "axios";
import { axiosInstance } from "../boot/axios.js";
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
  props: {
    token: String,
    post_id: Number,
    user_name: String,
    profile_url: String,
  },

  data() {
    return {
      user: [],
      value1: true,
      btnShow: false,
      index: "0",
      post_flg: true,
      to: "",
      toId: -1,
      post: [],
      comments: [],
      replyComment: "",
    };
  },
  directives: { clickoutside },
  methods: {
    Refresh: function () {
      this.Refresh();

      Axios.get("http://127.0.0.1:8000/pages/post_detail/", {
        params: {
          post_id: this.post_id,
          token: this.token,
        },
      })
        .then((res) => {
          console.log(res);
          this.post = res.data["post"];
          this.comments = res.data["comment"];
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    dianZan() {
      if (this.post_flg) {
        Axios.post("http://127.0.0.1:8000/users/like_post", {
          params: {
            post_id: this.post_id,
            token: this.token,
          },
        });
        this.post_flg = false;
      } else {
        Axios.post("http://127.0.0.1:8000/users/rm_like_post", {
          params: {
            post_id: this.post_id,
            token: this.token,
          },
        });
        this.post_flg = true;
      }
    },
    dianZan2() {
      if (this.comments_flg) {
        Axios.post("http://127.0.0.1:8000/users/like_comment", {
          params: {
            comment_id: this.comment_id,
            token: this.token,
          },
        });
        this.comments_flg = false;
      } else {
        Axios.post("http://127.0.0.1:8000/users/rm_like_comment", {
          params: {
            comment_id: this.comment_id,
            token: this.token,
          },
        });
        this.comments_flg = true;
      }
    },
    addRoute1() {
      this.$router.push("./Info");
    },
    addRoute2() {},
    deletePost() {
      if (this.post.if_self) {
        Axios.post("http://127.0.0.1:8000/users/delete_post", {
          params: {
            post_id: this.post.post_id,
            token: this.token,
          },
        });
        this.$message({
          showClose: true,
          type: "success",
          message: "删除成功",
        });
      } else {
        this.$message({
          showClose: true,
          type: "warning",
          message: "删除失败",
        });
      }
    },

    deleteComment() {
      if (this.comments.if_self) {
        Axios.post("http://127.0.0.1:8000/users/delete_comment", {
          params: {
            comment_id: this.comments.comment_id,
            token: this.token,
          },
        });
        this.$message({
          showClose: true,
          type: "success",
          message: "删除成功",
        });
      } else {
        this.$message({
          showClose: true,
          type: "warning",
          message: "删除失败",
        });
      }
    },
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
        Axios.get("http://127.0.0.1:8000/users/comment", {
          params: {
            post_id: this.post.post_id,
            token: this.token,
            content: this.replyComment,
            if_anonymous: this.value1,
          },
        });
        this.$message({
          showClose: true,
          type: "success",
          message: "评论成功",
        });
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
.cmt {
  background-color: #F2F6FC;
  border-shadow: 2px;
}

.post-title {
  height: 60px;

  .header-img {
    display: inline-block;
    vertical-align: top;
    cursor: pointer;
    height: 50px;
    width: 50px;
  }

  .post-info {
    display: inline-block;
    width: 80%;
    height: 60px;

    >span {
      text-align: left;
      height: 25px;
      display: block;
      line-height: 20px;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    .author-name {
      color: #000;
      font-size: 18px;
      font-weight: bold;
    }

    .author-time {
      font-size: 14px;
      color: #000;
    }
  }

  .post-close {
    height: 60px;
    margin-top: 10px;
    display: inline-block;
    vertical-align: top;
  }
}

.my-reply {
  padding: 10px;

  .header-img {
    display: inline-block;
    vertical-align: top;
  }

  .reply-info {
    display: inline-block;
    margin-left: 5px;
    width: 90%;

    .reply-input {
      min-height: 20px;
      line-height: 22px;
      padding: 10px;
      color: black;
      background-color: #FFF;
      border-radius: 5px;

      &:empty:before {
        content: attr(placeholder);
      }

      &:focus:before {
        content: none;
      }

      &:focus {
        padding: 8px 8px;
        box-shadow: none;
        outline: none;
      }
    }
  }

  .reply-btn-box {
    height: 25px;
    margin: 10px 10px 10px 10px;

    .reply-btn {
      position: relative;
      float: right;
    }

    .anonymous-btn {
      position: relative;
      float: left;
      margin-top: 5px;
    }
  }
}

.my-comment-reply {
  margin-left: 50px;

  .reply-input {
    width: flex;
  }
}

.author-title:not(:last-child) {
  border-bottom: 1px solid rgba(178, 186, 194, 0.3);
}

.author-title {
  padding: 10px;

  .header-img {
    display: inline-block;
    vertical-align: top;
  }

  .author-info {
    display: inline-block;
    margin-left: 5px;
    width: 70%;
    height: 40px;
    line-height: 20px;

    >span {
      display: block;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    .author-name {
      color: #000;
      font-size: 18px;
      font-weight: bold;
    }

    .author-time {
      font-size: 14px;
    }
  }

  .icon-btn {
    width: 20%;
    padding: 0 !important;
    float: right;

    @media screen and (max-width: 1200px) {
      width: 20%;
      padding: 7px;
    }

    >span {
      cursor: pointer;
    }

    .icon-font {
      margin: 0 5px;
    }
  }

  .talk-box {
    margin: 0 50px;

    >p {
      margin: 0;
    }

    .reply {
      font-size: 16px;
      color: #000;
    }
  }

  .reply-box {
    margin: 10px 0 0 50px;
    background-color: #efefef;
  }
}
</style>
