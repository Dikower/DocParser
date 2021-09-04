<script>
    import { push } from "svelte-spa-router";
    
    let companyType = 0;// 0 - банк, 1 - Компания
    let classForBanc = "littleButton gradButtonPurple";
    let classForComp = "littleButton whiteButton";

    function setBank(){
        companyType = 0;
        classForBanc = "littleButton gradButtonPurple";
        classForComp = "littleButton whiteButton";
    }
    function setComp(){
        companyType = 1;
        classForBanc = "littleButton whiteButton";
        classForComp = "littleButton gradButtonPurple";
    }
    function goToMainPage(){
        if(companyType === 0){
            push("/bank");
        }else{
            push("/comp");
        }
    }
</script>

<!-- <p>Authorization</p> -->
<!-- <button on:click={() => {push("/comp")}}>Company</button> -->
<!-- <button on:click={() => {push("/bank")}}>Bank</button> -->

<main class="flex">
    <!-- <div class="blackDiv"></div> -->
    <div class="purpleDiv"></div>
    <div class="glass">
        <div class="header">
            <p class="bigText">Загрузка файлов</p>
            <p class="text">Просто оставьте здесь свои файлы, а мы сделаем все за вас</p>
        </div>
        <div class="forDragAndDrop">
            <p class="grayText">Перетащите файлы сюда</p>
        </div>
        <div class="flex">
            <button class="gradButtonPurple downButton">
                ОТПРАВИТЬ
            </button>
        </div>
        
    </div>
</main>


<style>
    .purpleDiv{
        width: 100%;
        height: 100vh;
        background: radial-gradient(farthest-corner at 40px 40px, #45AAF2 0%, #4B7BEC 45.83%, #A55EEA 100%);
    }
    .glass{
        position: absolute;
        border-radius: 30px;
        left: 35%;
        top: 10vh;
        width: 30%;
        /* height: 80vh; */
        background: linear-gradient(0deg, rgba(75, 123, 236, 0.2), rgba(75, 123, 236, 0.2)),
        linear-gradient(0deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8));
        backdrop-filter: blur(24px);
    }
    .bigText{
        color: white;
        font-size: 50px;
        font-family: 'Russo One', sans-serif;
        margin-bottom: 0;
    }
    .text{
        color: white;
        font-family: 'M PLUS 1p', sans-serif;
        font-size: 22px;
        width: 65%;
        line-height: 37px;
    }
    .glass .header{
        padding-left: 3rem;
    }
    .forDragAndDrop{
        background: #FFFFFFBF;
        border-radius: 20px;
        width: 80%;
        height: 16rem;
        margin: auto;
        display: flex;
    }
    .grayText{
        color: rgba(115, 115, 115, 0.651);
        font-family: 'M PLUS 1p', sans-serif;
        font-size: 18px;
        line-height: 26px;
        margin: auto;
    }
    .downButton{
        border-radius: 100px;
        padding: 1.2rem;
        margin-bottom: 2rem;
        margin-top: 2rem;
        font-size: 18px;
    }
</style>