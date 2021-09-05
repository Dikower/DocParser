<script>
    import { push } from "svelte-spa-router";
</script>

<main>
    <div style="margin-left: 3rem; width:60%">
        <div class="flex logo">
            <img src="/img/logo.svg" alt="" class="m-c">
            <img src="/img/Peach2Win.svg" alt="" class="m-c" style="margin-left: 1rem;">
        </div>
        
        <p class="bigText">Платформа парсинга документов</p>
        <p class="text" style="width:60%">Тут описывается что нужно сделать что бы получить информацию, которую мы обработаем</p>
        <button on:click={() => {push("/auth")}} class="btn-blue-border">Загрузить файлы</button>
    </div>
    <img class="imgForMen" src="/img/Group 36.png" alt="">

</main>
<style>
    
    main {
        background-color: #1D1D1B;
        display: flex;
        justify-content: space-between;
    }
    .bigText {
        color: white;
        font-size: 80px;
        font-family: 'Russo One', sans-serif;

        margin-top: 14rem;
    }
    .text {
        color: #FFFFFFA6;
        font-family: 'M PLUS 1p', sans-serif;
        font-size: 30px;
        line-height: 45px;
        margin-top: 4rem;
    }
    .imgForMen {
        height: 100vh;
    }
    .logo{
        margin-top: 2rem;
    }
    .btn-blue-border{
        border: 8px solid #A55EEA;
        border-radius: 30px;
        font-size: 30px;
        font-family: 'M PLUS 1p', sans-serif;
        padding: 1rem;
        padding-left: 4rem;
        padding-right: 4rem;
        background-color: #1D1D1B;
        color: white;

        margin-top: 5rem;
    }
    .btn-blue-border:hover{
        background-color: rgb(44, 44, 41);
    }
    @media only screen and (max-height: 1000px){
        .bigText{
            margin-top: 6rem;
        }
        .btn-blue-border{
            margin-top: 2rem;
        }
    }
    @media only screen and (max-height: 800px){
        .bigText{
            margin-top: 2rem;
        }
    }
</style>