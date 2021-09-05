<script>
    import { push } from "svelte-spa-router";
    import Dropzone from "svelte-file-dropzone";
    import { DoubleBounce } from 'svelte-loading-spinners'
    import {apiURL} from "../config";

    let windowStatus = 0;
    let sendingStatus = 0;
    let outError = "";
    let files = {
        accepted: [],
        rejected: []
    };
    let report = apiURL + "/public/";

    let result = {};
    let stats = {};

    function handleFilesSelect(e) {
        const { acceptedFiles, fileRejections } = e.detail;
        files.accepted = [...files.accepted, ...acceptedFiles];
        files.rejected = [...files.rejected, ...fileRejections];
    }

    async function send_data(){
        let formData = new FormData();
        formData.append('in_file', files.accepted[0])
        sendingStatus = 1;
        const response = await fetch(
            apiURL + "/upload",
            {
                method: "POST",
                headers:{
                },
                body: formData
            }
            
        );
        if (response.ok === true) {
            const out = await response.json();
             console.log("Хорошо");
             console.log(out);
             result = out.result;
             stats = out.stats;
             report = apiURL + "/public/" + out.report;
             sendingStatus = 2;
        } else{
            const out = await response.json();
            console.log("Плохо");
            console.log(out);
            outError = out.detail;
            sendingStatus = 3;
        }

    }
</script>

<main class="flex">
    <div class="purpleDiv"></div>
    {#if windowStatus === 0}
        <div class="glass">
            <div class="header">
                <p class="bigText">Загрузка файлов</p>
                {#if sendingStatus === 0}
                    <p class="text">Просто оставьте здесь свои файлы, а мы сделаем все за вас</p>
                {/if}
            </div>
            {#if sendingStatus === 0}
                <div class="forDragAndDrop">
                    <Dropzone on:drop={handleFilesSelect} />
                </div>
                
                {#each files.accepted as item}
                    <p class="grayText">{item.name}</p>
                {/each}
                <div class="flex">
                    <button class="gradButtonPurple downButton" style="margin-right: auto;" on:click={send_data}>
                        ОТПРАВИТЬ
                    </button>
                </div>
            {:else if sendingStatus === 1}
                <div class="flex" style="flex-direction: column;">
                    <!-- <img src="https://i.gifer.com/origin/4d/4dc11d17f5292fd463a60aa2bbb41f6a_w200.gif" style="margin: auto;" alt="">     -->
                    <div style="width: 300px; margin:auto" class="flex">
                        <div style="width: 80px; margin-right: 10px;" class="m-c">
                            <DoubleBounce size="80" color="#498dee" unit="px" duration="4s" />
                        </div>
                        <DoubleBounce size="120" color="#498dee" unit="px" duration="4s" />
                        <div style="width: 80px; margin-left: 10px;" class="m-c">
                            <DoubleBounce size="80" color="#498dee" unit="px" duration="4s" />
                        </div>
                    </div>
                    <button class="gradButtonPurple cancelButton" style="margin-left: auto;" on:click={() => {location.reload()}}>Отмена</button>
                </div>
            {:else}
                {#if sendingStatus === 2}
                    <p class="bigText" style="color: teal; margin-top: 0;">Успешно</p>
                    <button class="gradButtonPurple flex" on:click={() => {windowStatus = 1}}>Просмотр результатов</button>
                    
                {:else}
                <p class="bigText" style="color: tomato; margin-top: 0;">Ошибка</p>
                <p class="text" style="color: tomato">{outError}</p>
                <button class="gradButtonPurple cancelButton flex" style="margin-left: auto;" on:click={() => {location.reload()}}>Отправить заново</button>
                {/if}
            {/if}
        </div>
    {:else}
        <div class="glassForResults">
            <p class="bigText">{result.name}</p>
            <div class="flex">
                <p style="margin:auto">
                    {#each result.path as step}
                        {#if step !== null}
                            <nobr class="grayText">{step} / </nobr>
                        {/if}
                    {/each}
                </p>
            </div>
            <div style="margin-bottom: 2rem; margin-top: 2rem;">
                {#each result.criteria_list as criter}
                    <p class="purpleText">{criter}</p>
                {/each}
            </div>
            <div class="flex" style="margin-bottom: 2rem; justify-content: space-between;">
                <div style="margin-top: auto;">
                    {#if new Date(stats.took * 1000).getSeconds() === 0}
                        <p class="grayText" style="text-align: left; margin-left: 2rem;">Затраченное время: {new Date(stats.took * 1000).getUTCMilliseconds()} (мл сек)</p>
                    {:else}
                        <p class="grayText" style="text-align: left; margin-left: 2rem;">Затраченное время: {new Date(stats.took * 1000).getSeconds()} (сек)</p>
                    {/if}
                    <p class="grayText" style="text-align: left; margin-left: 2rem;">Начало: {new Date(stats.startAt * 1000)}</p>
                    <p class="grayText" style="text-align: left; margin-left: 2rem;">Конец: {new Date(stats.endAt * 1000)}</p>
                </div>
                <a href={report} class="gradButtonPurple downButton">
                    <svg width="49" height="49" viewBox="0 0 49 49" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M45.9375 30.625C47.5081 30.625 48.8025 31.8072 48.9794 33.3303L49 33.6875V39.8125C49 44.7054 45.1752 48.705 40.3523 48.9844L39.8125 49H9.1875C4.2946 49 0.295038 45.1752 0.0155962 40.3523L0 39.8125V33.6875C0 31.9961 1.37113 30.625 3.0625 30.625C4.63306 30.625 5.92749 31.8072 6.1044 33.3303L6.125 33.6875V39.8125C6.125 41.3831 7.30725 42.6775 8.83035 42.8544L9.1875 42.875H39.8125C41.3831 42.875 42.6775 41.6928 42.8544 40.1697L42.875 39.8125V33.6875C42.875 31.9961 44.2461 30.625 45.9375 30.625ZM24.5 0C26.1914 0 27.5625 1.37113 27.5625 3.0625V26.2916L31.522 22.3345C32.626 21.2305 34.3631 21.1456 35.5645 22.0797L35.853 22.3345C36.957 23.4385 37.0419 25.1756 36.1078 26.377L35.853 26.6655L26.6655 35.853C25.5615 36.957 23.8244 37.0419 22.623 36.1078L22.3345 35.853L13.147 26.6655C11.951 25.4695 11.951 23.5305 13.147 22.3345C14.251 21.2305 15.9881 21.1456 17.1895 22.0797L17.478 22.3345L21.4375 26.2916V3.0625C21.4375 1.37113 22.8086 0 24.5 0Z" fill="white"/>
                    </svg>
                </a>
            </div>
            
        </div>
    {/if}
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
        padding-bottom: 1rem;
    }
    .glassForResults{
        position: absolute;
        border-radius: 30px;
        left: 20%;
        top: 10vh;
        width: 60%;
        /* height: 80vh; */
        background: linear-gradient(0deg, rgba(75, 123, 236, 0.2), rgba(75, 123, 236, 0.2)),
        linear-gradient(0deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8));
        backdrop-filter: blur(24px);
        padding-bottom: 1rem;
    }
    .bigText{
        color: white;
        font-size: 50px;
        font-family: 'Russo One', sans-serif;
        margin-bottom: 1rem;
        text-align: center;
    }
    .text{
        color: white;
        font-family: 'M PLUS 1p', sans-serif;
        font-size: 22px;
        width: 80%;
        margin: auto;
        margin-bottom: 1rem;
        line-height: 37px;
        text-align: center;
    }
    .forDragAndDrop{
        background: #FFFFFFBF;
        border-radius: 20px;
        width: 80%;
        height: 6rem;
        margin: auto;
        margin-bottom: 1rem;
        display: flex;
    }
    .grayText{
        color: rgba(83, 83, 83, 0.651);
        font-family: 'M PLUS 1p', sans-serif;
        font-size: 18px;
        line-height: 26px;
        text-align: center;
        margin: auto;
    }
    .cancelButton{
        border-radius: 100px;
        padding: 1.2rem;
        /* margin-bottom: 2rem; */
        margin-top: 1rem;
        font-size: 18px; 
    }
    .downButton{
        border-radius: 100px;
        padding: 1.2rem;
        margin-right: 2rem;
        margin-top: 1rem;
        font-size: 18px;
    }
    .purpleText{
        font-family: 'M PLUS 1p', sans-serif;
        font-size: 18px;
        line-height: 16px;
        margin-left: 1rem;
        margin-top: auto;
        margin-bottom: auto;
        cursor: default;
        color: #6373EC;
        font-weight: 600;
        text-align: center;
        margin-top: 1rem;
    }

    @media only screen and (max-width: 1600px){
        .glass{
            left: 30%;
            top: 10vh;
            width: 40%;
            /* background-color: black; */
        }
        .glassForResults{
            left: 20%;
            top: 10vh;
            width: 60%;
        }
    }
    @media only screen and (max-width: 1150px){
        .glass{
            left: 20%;
            top: 10vh;
            width: 60%;
            /* background-color: black; */
        }
        .glassForResults{
            left: 20%;
            top: 10vh;
            width: 60%;
        }
    }
</style>