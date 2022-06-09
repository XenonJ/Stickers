<template>
  <div class="page-register">
    <article class="header">
      <header>
        <el-avatar icon="el-icon-user-solid" shape="circle"></el-avatar>
        <span class="login">
          <em class="bold">Already have an account?&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</em>
          <a href="#/login">
            <el-button type="primary" size="small">login</el-button>
          </a>
        </span>
      </header>
    </article>
    <el-steps :active="active" finish-status="success" align-center>
      <el-step title="Step 1"></el-step>
      <el-step title="Step 2"></el-step>
    </el-steps>

    <section>
      <el-form
        ref="ruleForm"
        :model="ruleForm"
        :rules="rules"
        label-width="100px"
        class="demo-ruleForm"
        autocomplete="off"
      >
        <div v-if="active==0">
          <el-form-item prop="textarea">
            <el-input
              :value="ruleForm.textarea"
              type="textarea"
              :rows="10"
              :readonly="true"
            >
            </el-input>
          </el-form-item>
          <el-form-item prop="agreed">
            <el-checkbox v-model="ruleForm.agreed">Agree</el-checkbox>
          </el-form-item>
        </div>
        <div v-if="active==1">
          <el-form-item label="userid" prop="id">
            <el-input v-model="ruleForm.id" />
          </el-form-item>
          <el-form-item label="username" prop="name">
            <el-input v-model="ruleForm.name" />
          </el-form-item>
          <el-form-item label="avatar" prop="avatar">
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
              <!-- <div v-show="!dialogImageUrl" slot="tip" class="el-upload__text upload__tip">上传照片</div> -->
            </el-upload>
          </el-form-item>
          <el-form-item label="password" prop="pwd">
            <el-input v-model="ruleForm.pwd" type="password" />
          </el-form-item>
          <el-form-item label="password certification" prop="cpwd">
            <el-input v-model="ruleForm.cpwd" type="password" />
          </el-form-item>

        </div>
      </el-form>
    </section>
    <div class="footer">
      <el-button
        v-if="active>0"
        type="primary"
        icon="el-icon-arrow-left"
        @click="prev"
      >last step</el-button>
      <el-button
        v-if="active<step-1"
        type="primary"
        icon="el-icon-arrow-right"
        @click="next"
      >next step</el-button>
      <el-button
        v-if="active==step-1"
        type="primary"
        @click="register"
      >agree and register</el-button>
      <div class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import Axios from 'axios'

export default {
  data() {
    return {
      step: 2,
      active: 0,
      statusMsg: '',
      error: '',
      formdata: new FormData(),
      imageUrl: "",
      ruleForm: {
        textarea: 'please read the protical\nThe product is protected by Copyright Law. OMG retains the title to and ownership of the Product. You are licensed to use this Product on the following terms and conditions:\nLICENSE - The licensee is defined as the individual or company utilizing the Software Product. OMG hereby grants the licensee a nonexclusive license authorizing the licensee to use the enclosed Product on one computer at a time. The licensee is also permitted to distribute this product to one, and only one web server to host the Program. Please contact OMG if you require additional licenses. Use of this product by more than one individual or by anyone other than the licensee terminates, without notification, this license and the right to use this product.\nYOU MAY NOT: Distribute, rent, sub-license or otherwise make available to others the software or documentation or copies thereof, except as expressly permitted in this License without prior written consent from OMG. In the case of an authorized transfer, the transferee must agree to be bound by the terms and conditions of this License Agreement.\nRESTRICTIONS: - You may use this Product in your business as long as:\nThe software serial number and user must be registered with OMG in order to receive support or distribution rights.\nYou may not remove any proprietary notices, labels, trademarks on the software or documentation.\nYou may not modify, de-compile, disassemble, reverse engineer or translate the software.\nTERM - You may terminate your License and this Agreement at anytime by destroying all copies of the Product and Product Documentation. They will also terminate automatically if you fail to comply with any term or condition in this Agreement.\nLIMITED WARRANTY - This software and documentation are sold "as is" without any warranty as to their performance, merchantability or fitness for any particular purpose. The licensee assumes the entire risk as to the quality and performance of the software. OMG warrants that the diskettes on which the Program is furnished will be free from any defects in materials. Exclusive remedy in the event of a defect is expressly limited to the replacement of diskettes. In no event shall OMG or anyone else who has been involved in the creation, development, production, or delivery of this software be liable for any direct, incidental or consequential damages, such as, but not limited to, loss of anticipated profits, benefits, use, or data resulting from the use of this software, or arising out of any breach of warranty.',
        agreed: false,
        id: '',
        name: '',
        code: '',
        pwd: '',
        cpwd: '',
        avatar: {}
      },
      rules: {
        agreed: [{
          validator: (rule, value, callback) => {
            console.log('value:' + value)
            if (value !== true) {
              callback(new Error('please agree'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }],
        id: [{
          required: true,
          type: 'string',
          message: 'enter userid',
          trigger: 'blur'
        }],
        name: [{
          required: true,
          type: 'string',
          message: 'enter username',
          trigger: 'blur'
        }],
        code: [{
          required: true,
          type: 'string',
          message: 'enter certification',
          trigger: 'blur'
        }],
        email: [{
          required: true,
          type: 'email',
          message: 'enter email',
          trigger: 'blur'
        }],
        pwd: [{
          required: true,
          message: 'create password',
          trigger: 'blur'
        }],
        cpwd: [{
          required: true,
          message: 'certify password',
          trigger: 'blur'
        }, {
          validator: (rule, value, callback) => {
            if (value === '') {
              callback(new Error('please enter your password again'))
            } else if (value !== this.ruleForm.pwd) {
              callback(new Error('the two passwords don\'t match'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }]
      }
    }
  },
  layout: 'blank',
  methods: {
    sendMsg: function() {
      const self = this
      let namePass
      let emailPass
      if (self.timerid) {
        return false
      }
      this.$refs['ruleForm'].validateField('name', (valid) => {
        namePass = valid
      })
      self.statusMsg = ''
      if (namePass) {
        return false
      }
      this.$refs['ruleForm'].validateField('email', (valid) => {
        emailPass = valid
      })
      // 模拟验证码发送
      if (!namePass && !emailPass) {
        let mail_data = new FormData();
        mail_data.append('mail', this.ruleForm.email);
        Axios
          .post("http://127.0.0.1:8000/user/sendEmailCode/", mail_data)
        let count = 60
        self.statusMsg = `critification sent,${count--}seconds remain`
        self.timerid = setInterval(function() {
          self.statusMsg = `critification sent,${count--}seconds remain`
          if (count === 0) {
            clearInterval(self.timerid)
          }
        }, 1000)
      }
    },

    next: function() {
      if (this.active === 0) {
        this.$refs['ruleForm'].validateField('agreed', (valid) => {
          if (valid === '') {
            this.active++
          }
        })
      }
    },
    prev: function() {
      if (--this.active < 0) this.active = 0
    },

    // 模拟登录
    register: function() {
      this.formdata.append('user_id', this.ruleForm.id);
      this.formdata.append('user_name', this.ruleForm.name);
      this.formdata.append('password', this.ruleForm.pwd);
      Axios
        .post("http://127.0.0.1:8000/users/register/", this.formdata)
        .then(response=>{
          if(response.data[0].status == 200){
            this.$router.push('/login'), 2000
          }
          else{
            this.$q.notify(response.data[0].error);
          }
        })
        .catch(function(error){
          console.log(error);
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
      if(this.formdata.has('profile')){
        this.formdata.delete('profile');
      }
      this.formdata.append('profile', file)
      return false
    },
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw);
    },
  }
}
</script>

<style  rel="stylesheet/scss" lang="scss">
.page-register {
  .header {
    //border-bottom: 2px solid rgb(235, 232, 232);
    min-width: 980px;
    color: #666;

    header {
      margin: 0 auto;
      padding: 10px 0;
      width: 980px;

    .login {
        float: right;
      }

      .bold {
        font-style: normal;
      }
    }
  }

  .register {
    color: #1890ff;
  }

  a {
    color: #1890ff;
    text-decoration: none;
    background-color: transparent;
    outline: none;
    cursor: pointer;
    transition: color 0.3s;
  }

  > section {
    margin: 0 auto 30px;
    padding-top: 30px;
    width: 980px;
    min-height: 300px;
    padding-right: 550px;
    box-sizing: border-box;

    .status {
      font-size: 12px;
      margin-left: 20px;
      color: #e6a23c;
    }

    .error {
      color: red;
    }
  }

  .footer{
    text-align: center;
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
}
</style>

