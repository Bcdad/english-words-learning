<template>
  <section>
      <div class="color"></div>
      <div class="color"></div>
      <div class="color"></div>
      <div class="box">
          <div class="square" style="--i:0;"></div>
          <div class="square" style="--i:1;"></div>
          <div class="square" style="--i:2;"></div>
          <div class="square" style="--i:3;"></div>
          <div class="square" style="--i:4;"></div>
          <div class="container">
              <div class="form" id="sign">
                  <h2>Login Form</h2>
                  <form  method="post" @submit.prevent="handleSub" >
                      <table>
                          <div class="inputBox">
                              <input type="text" name="Username" placeholder="请输入账号(3~20位)" id="account" v-model="account">
                          </div>
                          <div class="inputBox">
                              <input type="password" v-model="password" placeholder="请输入密码(6~20位)" id="pass1">
                          </div>
                          <div class="inputBox">
                              <input type="password" v-model="password2" placeholder="请再次输入密码" id="pass2">
                          </div>
                          <div class="inputBox">
                              <input type="submit" value="Sign Up">
                          </div>
                      </table>
                  </form>
              </div>
          </div>
      </div>
  </section>
</template>
<script>
export default{
  data(){

    return{
      account:'',
      password:'',
      password2:''
    }
  },
  methods:{
    handleSub(){
      fetch('http://localhost:81/api/v2.0', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          account: this.account,
          pass1: this.password,
          pass2: this.password2
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data['pass3'] === 'no') {
            alert('两次密码不一致')
          }
          if (data['pass4'] === 'no') {
            alert('账号或密码格式不正确')
          }
          if (data['pass5'] === 'no') {
            alert('该账号已存在')
          }
          if (data['pass4'] === 'yes' && data['pass3'] === 'yes' && data['pass5'] === 'yes') {
            alert('注册成功')
          }
        })
        .catch((error) => {
          console.error('Error', error)
        })
    }
    }
  }
</script>
<style scoped>
@import '@/assets/login.css';
</style>