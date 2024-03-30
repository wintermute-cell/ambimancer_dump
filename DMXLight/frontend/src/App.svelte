<script lang="ts">
    import { onMount } from "svelte";
    import { createScene } from "./scene";
    import ioClient from "socket.io-client";
    const io = ioClient("http://127.0.0.1:5000", {autoConnect: false});

    async function connectSocket() {
        let resp = await fetch('./simulated');
        if (resp.ok) {
            io.connect();
        }
        io.on('msg', (data) => {
            console.log(data);
        });
        io.on('fixture_signal', (data) => {
            console.log(data);
        });
    }

    let canv;
    onMount(() => {
        connectSocket();
        createScene(canv);
    });

    async function show() {
        let resp = await fetch('./run?n=show');
        if (resp.ok) {
            console.log(`success launching show`);
        }
    }
</script>

<main>
    <button on:click={show}>show</button>
    <canvas id="light-sim-viewport" bind:this={canv} />
</main>

<style>
    #light-sim-viewport {
        width: 50vw;
        height: 50vh;
    }
</style>
