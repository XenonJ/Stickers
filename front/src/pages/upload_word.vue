<template>
  <q-page padding class="fixed fixed-center">
    <div style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)">
      <el-container style="width: 800px">
        <el-button-group>
          <el-button type="primary" @click="addRoute2" style="width: 400px">
            上传图片
            <i class="el-icon-picture-outline"></i>
          </el-button>
          <el-button
            type="primary"
            @click="addRoute1"
            style="width: 400px"
            disabled="true"
            >上传文字 <i class="el-icon-document"></i
          ></el-button>
        </el-button-group>

        <div class="q-pa-md q-gutter-sm">
          <q-editor
            v-model="text"
            :dense="$q.screen.lt.md"
            :toolbar="[
              [
                {
                  label: $q.lang.editor.fontSize,
                  icon: $q.iconSet.editor.fontSize,
                  fixedLabel: true,
                  fixedIcon: true,
                  list: 'no-icons',
                  options: [
                    'size-1',
                    'size-2',
                    'size-3',
                    'size-4',
                    'size-5',
                    'size-6',
                    'size-7',
                  ],
                },
                {
                  label: $q.lang.editor.defaultFont,
                  icon: $q.iconSet.editor.font,
                  fixedIcon: true,
                  list: 'no-icons',
                  options: [
                    'default_font',
                    'arial',
                    'arial_black',
                    'comic_sans',
                    'courier_new',
                    'impact',
                    'lucida_grande',
                    'times_new_roman',
                    'verdana',
                  ],
                },
              ],
              ['color_picker'],
            ]"
            :fonts="{
              arial: 'Arial',
              arial_black: 'Arial Black',
              comic_sans: 'Comic Sans MS',
              courier_new: 'Courier New',
              impact: 'Impact',
              lucida_grande: 'Lucida Grande',
              times_new_roman: 'Times New Roman',
              verdana: 'Verdana',
            }"
          />
        </div>

        <el-container style="height: 200px">
          <el-aside width="200px">
            <el-select v-model="label" placeholder="请选择背景" size="medium">
              <el-option
                v-for="item in options"
                :key="item.label"
                :label="item.label"
                :value="item.background_url"
                ><img :src="item.background_url" />
              </el-option>
            </el-select>
          </el-aside>

          <el-main>
            <div style="height:200px,width:560px">
              <div class="demo-image">
                <div class="block" v-for="fit in fits" :key="fit">
                  <span class="demonstration">{{ fit }}</span>
                  <el-image
                    style="width: 150px; height: 200px"
                    :src="url"
                    :fit="fill"
                  ></el-image>
                </div>
                <div></div>
              </div>
            </div>
          </el-main>
        </el-container>
        <el-footer>
          <div style="float: left">
            <el-switch v-model="if_anonymous" active-text="匿名"> </el-switch>
          </div>
          <div>
            <el-input
              style="width: 130px"
              placeholder="请输入x坐标"
              v-model="x_coordinate"
              type="number"
              :min="0"
            >
            </el-input>
            <el-input
              style="width: 130px"
              placeholder="请输入y坐标"
              v-model="y_coordinate"
              type="number"
              :min="0"
            >
            </el-input>
            <el-input
              style="width: 150px"
              placeholder="请输入旋转角度"
              v-model="rotation_angle"
              type="number"
              :min="0"
              :max="360"
            >
            </el-input>
          </div>
          <div>
            <el-button type="primary" plain @click="open1">上传</el-button>

            <el-button type="danger" plain @click="open2">退出</el-button>
          </div>
        </el-footer>
      </el-container>
    </div>
  </q-page>
</template>

<script>
import Axios from "axios";
import { axiosInstance } from "../boot/axios.js";
export default {
  props: {
    token: String,
  },
  data() {
    return {
      rotation_angle: "",
      if_anonymous: false,
      x_coordinate: "",
      y_coordinate: "",
      text_or_pic: true,
      text: "",
      url: "",
      label:"",
      background_url:"",
      options: [
        {
          label: "0",
          background_url: "/static/img/rel/right.png",
        },
        {
          label: "1",
          background_url: "/static/img/rel/left.png",
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
    open1() {
      this.$confirm("确认上传?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "primary",
      })
        .then(() => {
          Axios.post("http://127.0.0.1:8000/users/upload_post/", {
            params: {
              token: this.token,
              x_coordinate: this.x_coordinate,
              y_coordinate: this.y_coordinate,
              rotation_angle: this.rotation_angle,
              text_or_pic: this.text_or_pic,
              text: this.text,
              background_url: this.background_url,
              if_anonymous: this.if_anonymous,
            },
          });
          this.$message({
            type: "success",
            message: "上传成功!",
          });
        })
        .then(() => {
          this.$router.push("./");
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消上传",
          });
        });
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

<style scoped lang="scss">
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

  line-height: 40px;
}
.el-main {
  background-color: #ffffff;
  color: #333;
  text-align: center;
  line-height: 80px;
  font-weight: 400;
  border: solid 1px #dcd9d9;
  margin-right: 15px;
  margin-left: 10px;
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
  margin-left: 15px;
  margin-right: 10px;
}
</style>
