<template>
  <div>
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
              <div class="form" id="_form">
                  <h2>Login Form</h2>
                  <form method="post" @submit.prevent="handleSub">
                      <table>
                          <div class="inputBox">
                              <input type="text" placeholder="请输入账号" v-model="username">
                          </div>
                          <div class="inputBox" id="pass">
                              <input type="password" v-model="password" id="noo" placeholder="请输入密码">
                          </div>
                          <div class="inputBox">
                              <input type="submit" value="Login">
                          </div>
                          <p class="forget">Forget Password ?<a href="#">Click Here</a></p>
                          <p class="forget">Don't have an account ?<a :href="'/signup'">Sign up</a></p>
                      </table>
                  </form>
              </div>
          </div>
      </div>
  </section>
  </div>
</template>
<script>
export default{
  data(){
    return {
      username:'',
      password:''
    };
  },
  methods:{
    handleSub(){
      fetch('http://localhost:81/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          password:this.password,
          username:this.username
        })
      })
      .then(response => response.json())
      .then(data=>{
        if(data['username']){
          this.$router.push(`/user/${this.username}`);
        }else{
          this.$router.replace('/')
        }
      })

    }
  }
  }
</script>
<style scoped>
@import '@/assets/login.css';

</style>
