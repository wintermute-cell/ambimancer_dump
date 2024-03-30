<script lang="ts">
    import { onMount } from "svelte";

	let vw: number;
	let vh: number;
	let selectedMenuItem: HTMLDivElement;
	let menuItems: HTMLDivElement;

	onMount(() => {
		calcMenuPositions(0);
		window.addEventListener('resize', function() {
			calcMenuPositions(0);
		}, true);
	});

	function calcMenuPositions(angleOffset: number) {
		console.log(angleOffset)
		let angle = 120 + angleOffset;
		let radius = Math.max(Math.min(560 * (vw/1000), 560), 460);
		let offsetX = 550;
		for (const child of menuItems.children) {
			let x = (radius * Math.sin(angle/100)) - offsetX;
			let y = -radius * Math.cos(angle/100);
			let c = child as HTMLDivElement;
			c.style.setProperty('transform', `translate(${x}px, ${y}px)`)
			angle += 19 + (vw/1300);
		}
	}

	function menuItemMouseover(e: MouseEvent) {
		selectedMenuItem = <HTMLDivElement> e.target;
		let arr = Array.prototype.slice.call(menuItems.children)
		let idx = arr.indexOf(selectedMenuItem);
		let numItems = arr.length;
		let mid = numItems / 2;
		if (idx < mid) {
			calcMenuPositions(((mid-idx) * 4));
		} else {                     
			calcMenuPositions(((idx-mid) * -4));
		}
	}

	function menuItemMouseout(e: MouseEvent) {
		console.log('out');
	}

</script>

<svelte:head>
	<title>Ambimancer</title>
	<meta name="description" content="Ambimancer athmospheric toolkit" />
</svelte:head>

<svelte:window bind:innerHeight={vh} bind:innerWidth={vw}/>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus+SC&display=swap" rel="stylesheet">

<div id="menu">
	<div id="menu-items" bind:this={menuItems}>
<a href="#" on:mouseover={menuItemMouseover} on:mouseout={menuItemMouseout} class="menu-item"><div class="menu-item-glow"></div>Ambimancer</a>
		<a href="#" on:mouseover={menuItemMouseover} on:mouseout={menuItemMouseout} class="menu-item"><div class="menu-item-glow"></div>MpaddDoody</a>
		<a href="#" on:mouseover={menuItemMouseover} on:mouseout={menuItemMouseout} class="menu-item"><div class="menu-item-glow"></div>FeyFXFurrly</a>
		<a href="#" on:mouseover={menuItemMouseover} on:mouseout={menuItemMouseout} class="menu-item"><div class="menu-item-glow"></div>GoblinGrooves</a>
	</div>
</div>

<style>
	#menu {
		height: 100vh;
		display: flex;
		align-items: center;
		padding-left: 20em;
	}

	#menu-items:hover > .menu-item {
		opacity: 0.3;
	}

	#menu-items:hover > .menu-item:hover {
		opacity: 1;
	}

	.menu-item-glow {
		pointer-events: none;
		opacity: 0;
		position: absolute;
		width: 100%;
		height: 100%;
		left: -20px;
		transition: opacity 600ms ease;
		background-size: 100%;
		background-image: radial-gradient(
				4rem 40% at 4.5rem 52%,
				rgba(218,165,32,0.1) 0%,
				rgba(255, 255, 255, 0) 100%
			),radial-gradient(
				8rem 36% at 7rem 62%,
				rgba(218,165,32,0.1) 0%,
				rgba(255, 255, 255, 0) 100%
			)
		;
	}

	#menu-items:hover > .menu-item:hover > .menu-item-glow {
		opacity: 1;
	}

	.menu-item {
		opacity: 1;
		color: var(--fg-secondary);
		font-size: clamp(2rem, 6vw, 5rem);
		font-family: 'Marcellus SC', serif;
		position: absolute;
		left: 140px;
		transition: transform 1s, opacity 600ms ease, background-image 2s ease;
		padding-left: 2rem;

		text-decoration: none;
	}

</style>
