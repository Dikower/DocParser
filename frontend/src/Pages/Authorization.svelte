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
            <p class="bigText">Вход в систему</p>
            <p class="text">Для начала работы выберите тип вашей компании</p>
        </div>
        <div class="main">
            <div class="switch flex">
                <button class={classForBanc} on:click={setBank}>Банк</button>
                <button class={classForComp} on:click={setComp}>Компания</button>
            </div>
            <div class="boxForInput" style="margin-top: 2rem;">
                {#if companyType===0}
                    <p>Логин</p>
                    <input type="text" placeholder="Введите ваш логин">
                {:else}
                    <p>Название компании</p>
                    <input type="text" placeholder="Введите название вашей компании">
                {/if}
            </div>
            <div class="boxForInput">
                <p>Пароль</p>
                <input type="text" placeholder="Введите ваш пароль">
            </div>
            <button class="gradButton gradButtonPurple" on:click={goToMainPage}>Вход</button>
        </div>
    </div>
</main>


<style>
    .blackDiv{
        position: absolute;
        left: 40%;
        background-color: #1D1D1B;
        width: 20%;
        height: 100vh;
    }
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
        width: 60%;
        line-height: 37px;
    }
    .glass .header{
        padding-left: 3rem;
    }
    .glass .main{
        padding-left: 3rem;
        padding-right: 3rem;
        display: flex;
        flex-direction: column;
    }
    .boxForInput p{
        color: white;
        margin-left: 1rem;
        font-family: 'Russo One', sans-serif;
        font-size: 22px;
        margin-bottom: 0.7rem;
    }
    .boxForInput input{
        width: 100%;
        padding: 0.9rem;
        border: none;
        outline: none;
        padding-left: 1rem;
        border-radius: 16px;
        font-family: 'M PLUS 1p', sans-serif;
        /* color: #808080; */
    }

    .gradButton{
        padding: 1rem;
        padding-left: 4rem;
        padding-right: 4rem;
        margin-top: 3rem;   
        margin-bottom: 4rem;
    }
    .switch{
        background-color: white;
        width: 300px;
        border-radius: 25px;
    }
    .whiteButton{
        background-color: white;
        margin: auto;
        border: none;
        border-radius: 25px;
        color: #A55EEA;
        font-family: 'M PLUS 1p', sans-serif;
        font-size: 22px;
    }
    .littleButton{
        padding: 0.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        font-size: 20px;
        width: 150px;
        letter-spacing: 1px;
    }
    @media only screen and (max-width: 1550px){
        .glass{
            left: 30%;
            width: 40%;
        }
    }
    @media only screen and (max-width: 1200px){
        .glass{
            left: 20%;
            width: 60%;
        }
    }
    @media only screen and (max-width: 800px){
        .glass{
            left: 10%;
            width: 80%;
        }
    }
</style>