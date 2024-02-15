<svelte:head>
  <title>TimeTracker</title>
</svelte:head>
<script>
	import { Button } from 'svelte-materialify';
	import { onMount, onDestroy } from "svelte";
	import { formatDate, sendDataToServer } from './utils'; 

	const now = new Date();
	let currentTime = formatDate(now);
	let actions = [];
	let darkMode = true;

	onMount(() => {
		document.body.classList.add("dark-mode");
		const interval = setInterval(updateTime, 1000);
		loadActions();

		onDestroy(() => clearInterval(interval));
	});

	async function loadActions() {
		try {
			const response = await fetch('http://192.168.0.10:5000/api/actions/');
			if (response.ok) {
				const data = await response.json();
				actions = data.reverse().map(item => `${formatDate(new Date(item.time))}　${item.action}`);
			} else {
				throw new Error('Failed to fetch actions');
			}
		} catch (error) {
			console.error(error);
		}
	}

	function updateTime() {
		const now = new Date();
		currentTime = formatDate(now);
	}

	function toggleTheme() {
		darkMode = !darkMode;
		document.body.classList.toggle("dark-mode", darkMode);
	}

	function recordAction(action) {
		const now = new Date();
		const actionRecord = `${formatDate(now)}　${action}`;
		actions = [actionRecord, ...actions];
		sendDataToServer({ action, time: now.toISOString() });
	}
</script>

<h3>{currentTime}</h3>

<Button on:click={toggleTheme}>{darkMode ? 'Right Mode' : 'Dark Mode'}</Button>

<div class="buttons">
	<Button on:click={() => recordAction("出勤")}>出勤</Button>
	<Button on:click={() => recordAction("休憩")}>休憩</Button>
	<Button on:click={() => recordAction("回来")}>回来</Button>
	<Button on:click={() => recordAction("退勤")}>退勤</Button>
</div>

{#each actions as action}
	<p>{action}</p>
{/each}

<style>
	:global(.dark-mode) {
		background-color: #333;
		color: white;
	}
	.buttons {
		display: flex;
		gap: 8px;
	}
</style>
