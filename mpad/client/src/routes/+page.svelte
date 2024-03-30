<script lang="ts">
    import screenfull from 'screenfull';

    async function fetchLayout() {
        const layout_response = await fetch('./get_layout');
        const layout = await layout_response.json();
        const buttons_response = await fetch('./get_buttons');
        const buttons = await buttons_response.json();
        return [layout, buttons];
    }

    let fetchedLayout = fetchLayout();
    
    function tryFullscreen() {
        if(screenfull.isEnabled) {
            screenfull.toggle();
        }
    }

    function tryReload() {
        fetchedLayout = fetchLayout()
    }

    function handleButton(button_name: string) {
        fetch(`./run_button?name=${button_name}`);
    }
</script>

<button on:click={tryFullscreen}>F</button>
<button on:click={tryReload}>R</button>
<div id="container">
    {#await fetchedLayout}
        <p>waiting...</p>
    {:then data}
        {#each data[0] as page}
            <section>
                <div class="page">
                    <div class="button-container">
                        {#each page as button_name}
                            <button 
                                class="button"
                                style="background-image: url('./get_icon?name={data[1][button_name]['icon']}');"
                                on:click={() => {handleButton(button_name)}}
                            >
                                <div class="button-name-wrapper">
                                    {data[1][button_name]['name']}
                                </div>
                            </button>
                        {/each}
                    </div>
                </div>
            </section>
        {/each}
    {:catch err}
        <p style="color: red">{err.message}</p>
    {/await}
</div>

<style>

    :root {
        --fg_primary: #fffefd;
        --fg_secondary: #E1BB80;
        --fg_tertiary: #7B6B43;
        --bg_primary: #121217;
        --bg_secondary: #7765E3;
        --bg_tertiary: #806443;
    }
    
    :global(body) {
        margin: 0;
        overflow-x: hidden;
        overflow-y: hidden;
    }

    #container {
        background-color: var(--bg_primary);
        display: flex;
        overflow-x: scroll;
        scroll-snap-type: x mandatory;	
		-webkit-overflow-scrolling: touch;
    }

    section {
        border-right: 1px solid white;
		padding: 1rem;
		min-width: 100vw;
		height: 100vh;
		scroll-snap-align: start;
		text-align: center;
		position: relative;
    }

    .button-container {
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
        justify-content: left;
    }

    .button {
        position: relative;
        display: inline-block;
        color: var(--fg_primary);
        width: 128px;
        height: 128px;
        max-width: 128px;
        max-height: 128px;
        margin: 20px;
        font-weight: 1000;
        font-size: 1.1em;
        padding: 0;
        font-family: Verdana, Arial, sans-serif;
        border-radius: 40px;
        box-shadow: 3px 4px #1f1d24,15px 15px 30px #000000e6;
        transition: all .3s;
        outline: none;
        border: 2px solid #443f3f;
    }

    .button:active {
        transform: translate(4px, 5px);
        box-shadow: none;
    }

    .button-name-wrapper {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        background: linear-gradient(to top, rgba(10, 10, 10, 0.6) 0% 28%, transparent 56% 55%);
        text-shadow: -1px -1px 0 #242424, 1px -1px 0 #242424, -1px 1px 0 #242424, 1px 1px 0 #242424;
        height: 100%;
        width: 100%;
        padding: 4px;
        box-sizing: border-box;
        border-radius: 36px;
    }
</style>
