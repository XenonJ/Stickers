+<template>
  <q-page class="flex flex-center">
    <div style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)">
      <el-container style="width: 800px">
        <el-button-group>
          <el-button type="primary"  style="width: 800px">
            用户详细信息
          </el-button>
        </el-button-group>

        <el-container>
        <el-row class="demo-avatar demo-basic">
        <el-col :span="12">
        <div class="demo-basic--circle">
        <div class="block"><el-avatar :size="60" :src="circleUrl"></el-avatar></div>
        <div class="block" v-for="size in sizeList" :key="size">
          <el-avatar :size="size" :src="circleUrl"></el-avatar>
        </div>
        </div>
        </el-col>  
        <el-col :span="12">
        <div>zzh&nbsp; </div>
        <div>&nbsp; </div>
        <div>0000000000</div>
        </el-col> 
        </el-row>
        </el-container>
        

        <el-container>
        <el-input
          type="textarea"
          style="width: 800px"
          placeholder="财大骚0zzh"
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

          <div>
            <el-button type="danger" plain @click="open2">退出</el-button>
          </div>
        </el-footer>

        
        
      </el-container>
    </div>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      activities: [{
          content: '上传了帖子',
          timestamp: '2022-01-01 20:46',
          size: 'large',
        }, {
          content: '上传了帖子',
          timestamp: '2018-04-03 20:46',
          color: '#0bbd87',
          size: 'large',
        }, {
          content: '上传了帖子',
          timestamp: '2018-04-03 20:46',
          size: 'large'
        }, {
          content: '上传了帖子',
          timestamp: '2018-04-03 20:46',
          size: 'large',
        }],
      value2: [0, 360],
      value3: 1,
      textarea: "",
      input1: "",
      input2: "",
      options: [
        {
          label: "/static/img/rel/right.png",
          value1: "0",
        },
        {
          label: "/static/img/rel/left.png",
          value1: "1",
        },
      ],
    };
  },
  methods: {
    addRoute1() {
      this.$router.push("./upload_word");
    },
    addRoute2() {
      this.$router.push("./upload_picture");
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

<style>
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