<template>
  <q-page padding class="fixed fixed-center">
    <div style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)">
      <el-container style="width: 800px">
        <el-button-group>
          <el-button
            type="primary"
            @click="addRoute2"
            style="width: 400px"
            disabled="true"
          >
            上传图片
            <i class="el-icon-picture-outline"></i>
          </el-button>
          <el-button type="primary" @click="addRoute1" style="width: 400px"
            >上传文字 <i class="el-icon-document"></i
          ></el-button>
        </el-button-group>
        <div
          style="
            position: relative;
            top: 10px;
            left: 300px;
            right: 300px;
            width: 800px;
            height: 200px;
            border: 1px;
          "
        >
          <!-- <el-upload
            :action="api + 'upload'"
            list-type="picture-card"
            :auto-upload="false"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :fileList="this.dialogImageUrl"
            :limit="1"
          >
            <i slot="default" class="el-icon-plus"></i>
            <div slot="file" slot-scope="{ file }">
              <img
                class="el-upload-list__item-thumbnail"
                :src="file.url"
                alt=""
              />
              <span class="el-upload-list__item-actions">
                <span
                  class="el-upload-list__item-preview"
                  @click="handlePictureCardPreview(file)"
                >
                  <i class="el-icon-zoom-in"></i>
                </span>

                <span
                  class="el-upload-list__item-delete"
                  @click="handleRemove(file, fileList)"
                >
                  <i class="el-icon-delete"></i>
                </span>
              </span>
            </div>
          </el-upload> -->
          <el-upload
              class="avatar-uploader"
              action="aaa"
              ::limit="1"
              :show-file-list="false"

              :on-change="handlePictureCardPreview"
              :before-upload="beforeupload"
              accept="image/png,image/gif,image/jpg,image/jpeg">
              <img v-if="imageUrl" :src="imageUrl" class="avatar">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="" />
          </el-dialog>
        </div>
        <el-container style="height: 200px; margin-top: 10px">
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
            <div class="demo-image" style="height='200px">
              <div class="block" v-for="fit in fits" :key="fit">
                <span class="demonstration">{{ fit }}</span>
                <el-image
                  style="width: 150px; height: 200px"
                  :src="this.dialogImageUrl"
                  :fit="fill"
                ></el-image>
              </div>
              <div></div>
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

<script scoped>
import Axios from "axios";
import { axiosInstance } from "../boot/axios.js";
export default {
  props: {
    token: String,
  },
  data() {
    return {
      label: "",
      background_url: "",
      rotation_angle: "",
      if_anonymous: false,
      x_coordinate: "",
      y_coordinate: "",
      dialogImageUrl: "",
      dialogVisible: false,
      fileList: [],
      text_or_pic: false,
      formdata: new FormData(),
      imageUrl: "",
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
      background_url: "",
    };
  },
  mounted(){
    this.token = this.$route.query.token;
  },
  methods: {
    addRoute1() {
      this.$router.push("./upload_word");
    },
    addRoute2() {
      this.$router.push("./upload_picture");
    },
    handleRemove(file, fileList) {
      this.fileList = this.fileList.pop();
    },

    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },

    open1() {
      this.$confirm("确认上传?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "primary",
      })
        .then(() => {
          this.formdata.append('token', this.token);
          this.formdata.append('x_coordinate', this.x_coordinate);
          this.formdata.append('y_coordinate', this.y_coordinate);
          this.formdata.append('rotation_angle', this.rotation_angle);
          this.formdata.append('text_or_pic', false);
          this.formdata.append('background_url', this.background_url);
          this.formdata.append('if_anonymous', this.if_anonymous);
          Axios
          .post("http://127.0.0.1:8000/users/upload_post/", this.formdata)
          .then(response=>{
            if(response.status == 200){
              this.$router.push('/?token='+this.token)
            }
            else{
              this.$q.notify(response.error);
            }
          })
          .catch(function(error){
            console.log(error);
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
    handlePictureCardPreview (event) {
      var URL = null;
      if (window.createObjectURL != undefined) {
        // basic
        URL = window.createObjectURL(event.raw);
      } else if (window.URL != undefined) {
        // mozilla(firefox)
        URL = window.URL.createObjectURL(event.raw);
      } else if (window.webkitURL != undefined) {
        // webkit or chrome
        URL = window.webkitURL.createObjectURL(event.raw);
      }
      this.imageUrl = URL;
    },
    beforeupload (file) {
      if(this.formdata.has('picture')){
        this.formdata.delete('picture');
      }
      this.formdata.append('picture', file)
      return false
    },
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw);
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
  line-height: 40px;
}
.el-main {
  background-color: #ffffff;
  color: #333;
  text-align: center;
  line-height: 100px;
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
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
