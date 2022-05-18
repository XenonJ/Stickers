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
          <el-upload
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
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="" />
          </el-dialog>
        </div>
        <el-container style="height: 200px; margin-top: 10px">
          <el-aside width="200px">
            <el-select v-model="value1" placeholder="请选择背景" size="medium">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value1"
                ><img :src="item.label" />
              </el-option>
            </el-select>
          </el-aside>

          <el-main>
            <div class="demo-image" style="height='200px">
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
          </el-main>
        </el-container>
        <el-footer>
          <div style="float: left">
            <el-switch v-model="value3" active-text="匿名"> </el-switch>
          </div>
          <div>
            <el-input
              style="width: 130px"
              placeholder="请输入x坐标"
              v-model="input1"
              clearable
            >
            </el-input>
            <el-input
              style="width: 130px"
              placeholder="请输入y坐标"
              v-model="input2"
              clearable
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
export default {
  data() {
    return {
      value2: [0, 360],
      value3: 1,
      input1: "",
      input2: "",
      dialogImageUrl: "",
      dialogVisible: false,
      fileList: [],
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
      value1: "",
    };
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
</style>
