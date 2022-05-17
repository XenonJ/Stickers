<template>
  <q-page class="flex flex-center">
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
            v-model="textarea"
            :dense="$q.screen.lt.md"
            :toolbar="[
              [
                {
                  label: $q.lang.editor.align,
                  icon: $q.iconSet.editor.align,
                  fixedLabel: true,
                  list: 'only-icons',
                  options: ['left', 'center', 'right', 'justify'],
                },
              ],
              [
                'bold',
                'italic',
                'strike',
                'underline',
                'subscript',
                'superscript',
              ],
              ['token', 'hr', 'link', 'custom_btn'],
              [
                {
                  label: $q.lang.editor.formatting,
                  icon: $q.iconSet.editor.formatting,
                  list: 'no-icons',
                  options: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code'],
                },
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
                'removeFormat',
              ],
              ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
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

        <el-container>
          <el-aside width="200px">
            <el-select
              :popper-append-to-body="false"
              v-model="value1"
              placeholder="请选择背景"
              size="medium"
            >
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
            <div class="demo-image">
              <div class="block" v-for="fit in fits" :key="fit">
                <span class="demonstration">{{ fit }}</span>
                <el-image
                  style="width: 150px; height: 200px"
                  :src="url"
                  :fit="fill"
                ></el-image>
              </div>
              <div>
                <el-slider v-model="value2" vertical height="200px" :max="360">
                </el-slider>
              </div>
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

<script>
export default {
  data() {
    return {
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

<style scoped>
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
