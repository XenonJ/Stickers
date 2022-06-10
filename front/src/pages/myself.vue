<template>
  <q-page class="flex flex-center">
    <div style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)">
      <el-container style="width: 400px">
        <el-button-group>
          <el-button type="primary"  style="width: 400px">
            用户详细信息
          </el-button>
        </el-button-group>

        <el-container>

          <div class="post-title">
            <el-avatar
              shape="circle"
              :size="size"
              :src="this.profile_url"
              class="header-img"
              @click.native="addRoute1"
            ></el-avatar>
            <div class="post-info">
              <span class="author-name">zzh &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<el-link icon="el-icon-edit" @click="Editmyself">编辑</el-link></span>
              <span class="author-time">2019111984</span>
            </div>


            <div class="post-close">
              <el-button
                size="medium"
                round
                class="el-icon-close"
                @click="open2"
              ></el-button>
            </div>
          </div>

        </el-container>


        <el-container>
        <el-input
          type="textarea"
          style="width: 400px"
          placeholder="简单介绍一下你自己吧"
          v-model="textarea"
          maxlength="50"
          show-word-limit
          rows="3"
          vertical-align:middle
          resize="none"
        >
        </el-input>
        </el-container>

        <el-container>
        <el-timeline>
        <el-timeline-item
         v-for="(activity, index) in activities"
         :key="index"
         :icon="activity.icon"
         :type="activity.type"
         :color="activity.color"
         :size="activity.size"
         :timestamp="activity.timestamp">
        {{activity.content}}
        </el-timeline-item>
        </el-timeline>
        </el-container>

      <el-footer>
     </el-footer>
      </el-container>
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
  name: "myself",
  props: {
    token: String,
    user_id: Number,
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
      replyComment: "",

      activities: [{
          content: '上传了帖子',
          timestamp: '2022-06-10 11:00',
          size: 'large',
        }, {
          content: '上传了帖子',
          timestamp: '2022-06-10 09:46',
          color: '#0bbd87',
          size: 'large',
        }, {
          content: '上传了帖子',
          timestamp: '2022-06-10 09:40',
          size: 'large'
        }, {
          content: '上传了帖子',
          timestamp: '2022-06-10 00:38',
          size: 'large',
        }],

    };
  },
  methods: {
    Refresh: function () {
      // this.Refresh();

      Axios.get("http://127.0.0.1:8000/pages/user_detail/", {
        params: {
          token: this.token,
        },
      })
        .then((res) => {
          console.log(res);
          this.post = res.data["posts"];
          this.user = res.data["user"];
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    Editmyself(){
      Axios.post("http://127.0.0.1:8000/users/show_yourself/", {
          params: {
            show_yourself: this.show_yourself,
            token: this.token,
          },
        });
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
    addRoute1() {
      this.$router.push("./Info");
    },
    addRoute2() {
      this.$router.push("./comment");
    },
    open2() {
      this.$confirm("返回主界面?", "退出", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        this.$router.push("./");
      });
    },
  },
};
</script>

<style lang="stylus" scoped>
.post-title
    width:120%
    margin-left:0px
    margin-right:0px
    padding 10px 5px 15px 20px;
    .header-img
        display inline-block
        vertical-align top
        cursor pointer

    .post-info
        display inline-block
        margin-left 10px
        width 60%
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
.el-header,
.el-footer {
  background-color: #ffffff;
  color: rgb(255, 0, 0);
  text-align: center;
  line-height: 60px;
  vertical-align: middle;
}
.el-aside {
  background-color: #ffffff;
  color: #333;
  text-align: center;
  line-height: 80px;
}
.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 80px;
  font-weight: 400;
}
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.el-radio {
  display: block;
  margin-left: 0%;
}
.el-select {
  size: small;
}
</style>
