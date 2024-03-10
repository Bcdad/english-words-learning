<template>
    <div id="container">
        <form action="/" id="form">
            <label for="text">请输入要学习的单词数</label>
            <input type="text" name="text" id="d" v-model="num">
            <input type="submit" value="确定" @click.prevent="learn">
        </form>
        <div id="content">
            <div v-for="(item, index) in study" :key="index">
                <div>{{ item.english }}</div>
                <div>{{ item.phonetic }}</div>
                <div>{{ item.chinese }}</div>
                <div>{{ item.sentence1 }}</div>
                <div>{{ item.sentence2 }}</div>
                <div v-if="index < study.length - 1" class="divider"></div>
            </div>
        </div>
    </div>
    <div><a :href="'/user/' + user" class="bottom">返回</a></div>
</template>  
<script>
export default {
    data() {
        return {
            user: this.$route.params.username,
            num: '',
            study: []
        }
    },
    methods: {
        learn() {
            fetch('http://localhost:81/api/v1.0/study', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user: this.user,
                    num: this.num
                })
            })
                .then(response => response.json())
                .then(data => {
                    this.study = data['content']
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                })
        }
    }
}
</script>
<style>
* {
    font-size: 20px;
}

#container {
    width: 600px;
    min-height: 100%;
    margin: 0 auto;
    padding-left: 100px;
    padding-right: 50px;
    background-color: rgb(202, 192, 168);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.divider {
    height: 2px;
    width: 500px;
    background-color: #0f0e0e;
    margin-left: -50px;
}

body {
    background-image: url("@/assets/background.jpeg");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: 200vh;
}

.bottom {
    position: fixed;
    bottom: 20px;
    right: 40px;
    margin: 0 auto;
    width: 100px;
    height: 30px;
    display: block;
    border-radius: 15px;
    overflow: hidden;
    text-decoration: none;
    text-align: center;
    line-height: 30px;


}

.bottom::after {
    content: '';
    width: 200px;
    height: 200px;
    position: absolute;
    background-color: #fff;
    top: -40px;
    left: -20px;
    background-image: linear-gradient(to right, #a1a09a, #cfd340, #616b07);
    z-index: -1;
    transition: all 200ms ease;
}

.bottom:hover::after {
    transform: rotate(100deg);
}

.bottom:hover {
    width: 120px;
    height: 36px;
    border-radius: 18px;
    box-shadow: 10px -10px 10px 0px #313131;
}
</style>